# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import functools as func

from tgit.album import AlbumListener
from tgit import album_director as director
from tgit.ui.about_dialog import AboutDialog
from tgit.ui.activity_indicator_dialog import ActivityIndicatorDialog
from tgit.ui.dialogs import Dialogs
from tgit.ui.startup_screen import StartupScreen
from tgit.ui.isni_lookup_dialog import ISNILookupDialog
from tgit.ui.new_album_page import NewAlbumPage
from tgit.ui.performer_dialog import PerformerDialog
from tgit.ui.track_list_page import TrackListPage
from tgit.ui.album_edition_page import AlbumEditionPage, make_album_edition_page
from tgit.ui.export_as_dialog import ExportAsDialog
from tgit.ui.main_window import MainWindow
from tgit.ui.message_boxes import MessageBoxes
from tgit.ui.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.settings_dialog import SettingsDialog
from tgit.ui.track_edition_page import TrackEditionPage
from tgit.ui.track_selection_dialog import TrackSelectionDialog
from tgit.ui.welcome_page import WelcomePage
from tgit.ui.album_screen import album_screen as AlbumScreen
from tgit.util import browser
# noinspection PyUnresolvedReferences
from tgit.ui import resources


def PerformerDialogController(parent, album):
    def assign_guest_performers():
        album.guest_performers = dialog.getPerformers()

    dialog = PerformerDialog(parent)
    dialog.accepted.connect(assign_guest_performers)
    dialog.display(album.guest_performers)
    dialog.open()
    return dialog


def ISNILookupDialogController(parent, album, identities):
    dialog = ISNILookupDialog(parent, identities)
    dialog.accepted.connect(lambda: director.selectISNI(dialog.selectedIdentity, album))
    dialog.open()
    return dialog


def ActivityIndicatorDialogController(parent):
    dialog = ActivityIndicatorDialog(parent)
    dialog.open()
    return dialog


def TrackEditionPageController(album, track):
    page = TrackEditionPage()
    page.metadataChanged.connect(lambda metadata: director.updateTrack(track, **metadata))

    class CancelSubscription(AlbumListener):
        def trackRemoved(self, removed, position):
            if removed == track:
                subscription.cancel()
                album.removeAlbumListener(page)
                album.removeAlbumListener(self)

    subscription = track.metadata_changed.subscribe(page.display_track)
    album.addAlbumListener(page)
    album.addAlbumListener(CancelSubscription())
    page.display(album=album, track=track)
    return page


def SettingsDialogController(notify_restart_required, preferences, parent):
    dialog = SettingsDialog(parent)

    def save_preferences():
        preferences.add(**dialog.settings)
        notify_restart_required()

    dialog.accepted.connect(save_preferences)
    dialog.add_language("en", dialog.tr("English"))
    dialog.add_language("fr", dialog.tr("French"))
    dialog.display(**preferences)
    return dialog


def create_main_window(portfolio, player, preferences, name_registry, native, confirm_exit):
    dialogs = Dialogs(native)
    messages = MessageBoxes(confirm_exit)

    def show_settings_dialog():
        return SettingsDialogController(messages.restart_required, preferences, window)

    def create_new_album_page():
        return NewAlbumPage(select_album_location=dialogs.select_album_destination,
                            select_track=dialogs.select_track,
                            check_album_exists=director.album_exists,
                            confirm_overwrite=messages.overwrite_album_confirmation,
                            on_create_album=director.create_album_into(portfolio))

    def create_welcome_page():
        return WelcomePage(select_album=dialogs.select_album_to_load,
                           show_load_error=messages.load_album_failed,
                           on_load_album=director.load_album_into(portfolio))

    def create_startup_screen():
        return StartupScreen(create_welcome_page=create_welcome_page,
                             create_new_album_page=create_new_album_page)

    def create_track_list_page(album):
        return TrackListPage(album, player,
                             select_tracks=func.partial(dialogs.select_tracks, album.type),
                             on_move_track=director.move_track_of(album),
                             on_remove_track=director.remove_track_from(album),
                             on_play_track=player.play,
                             on_stop_track=player.stop,
                             on_add_tracks=director.add_tracks_to(album))

    def create_album_page(album):
        return make_album_edition_page(preferences, show_isni_lookup_dialog, show_activity_indicator_dialog,
                                       show_performer_dialog, messages.isni_assignation_failed, album, name_registry,
                                       select_picture=dialogs.select_cover,
                                       on_select_picture=director.change_cover_of(album))

    def show_isni_lookup_dialog(album, identities):
        return ISNILookupDialogController(window, album, identities)

    def show_performer_dialog(album):
        return PerformerDialogController(window, album)

    def show_activity_indicator_dialog():
        return ActivityIndicatorDialogController(window)

    def create_album_screen(album):
        def create_track_page(track):
            return TrackEditionPageController(album, track)

        return AlbumScreen(create_track_list_page, create_album_page, create_track_page, album)

    window = MainWindow(portfolio,
                        confirm_exit=messages.confirm_exit,
                        create_startup_screen=create_startup_screen,
                        create_album_screen=create_album_screen,
                        confirm_close=messages.close_album_confirmation,
                        select_export_destination=dialogs.export,
                        select_tracks=dialogs.select_tracks,
                        select_tracks_in_folder=dialogs.add_tracks_in_folder,
                        show_save_error=messages.save_album_failed,
                        show_export_error=messages.export_failed,
                        on_close_album=director.remove_album_from(portfolio),
                        on_save_album=director.save_album(),
                        on_add_files=director.add_tracks,
                        on_export=director.export_as_csv,
                        on_settings=show_settings_dialog,
                        on_about_qt=messages.about_qt,
                        on_about=messages.about_tgit,
                        on_online_help=browser.open_)
    dialogs.parent = window
    messages.parent = window
    portfolio.album_removed.subscribe(lambda album: dialogs.clear())

    return window

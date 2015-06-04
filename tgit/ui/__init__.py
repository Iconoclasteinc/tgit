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

from PyQt5.QtWidgets import QApplication

from tgit.album import AlbumListener
from tgit import album_director as director
from tgit.ui import commands as ui_commands
from tgit.ui.activity_indicator_dialog import ActivityIndicatorDialog
from tgit.ui.dialogs import Dialogs
from tgit.ui.album_selection_dialog import AlbumSelectionDialog
from tgit.ui.isni_lookup_dialog import ISNILookupDialog
from tgit.ui.performer_dialog import PerformerDialog
from tgit.ui.album_composition_page import AlbumCompositionPage, make_album_composition_page
from tgit.ui.album_edition_page import AlbumEditionPage, make_album_edition_page
from tgit.ui.export_as_dialog import ExportAsDialog
from tgit.ui.main_window import MainWindow
from tgit.ui.message_box import restart_message_box
from tgit.ui.message_box import isni_assignation_failed_message_box
from tgit.ui.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.settings_dialog import SettingsDialog
from tgit.ui.track_edition_page import TrackEditionPage
from tgit.ui.track_selection_dialog import TrackSelectionDialog
from tgit.ui.welcome_screen import make_welcome_screen
from tgit.ui.main_window import main_window as MainWindow
from tgit.ui.album_screen import album_screen as AlbumScreen

# noinspection PyUnresolvedReferences
from tgit.ui import resources


def show(widget):
    widget.show()


def centerOnScreen(widget):
    desktop = QApplication.desktop()
    position = widget.frameGeometry()
    position.moveCenter(desktop.availableGeometry().center())
    widget.move(position.topLeft())


def activate(widget):
    from PyQt5.QtCore import QSysInfo

    if hasattr(QSysInfo, "MacintoshVersion") and QSysInfo.MacintoshVersion > QSysInfo.MV_10_8:
        # Since Maverick, menu bar does not appear until the window is manually activated, so force
        # user to activate by not raising the window
        pass
    else:
        # we can safely raise the window
        widget.raise_()

    widget.activateWindow()


def showCenteredOnScreen(widget):
    show(widget)
    centerOnScreen(widget)
    activate(widget)


def PerformerDialogController(parent, album):
    def assign_guest_performers():
        album.guestPerformers = dialog.getPerformers()

    dialog = PerformerDialog(parent)
    dialog.accepted.connect(assign_guest_performers)
    dialog.display(album.guestPerformers)
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


def SettingsDialogController(restart_notice, preferences, parent):
    dialog = SettingsDialog(parent)

    def save_preferences():
        preferences.add(**dialog.settings)
        restart_notice(parent).open()

    dialog.accepted.connect(save_preferences)
    dialog.add_language("en", dialog.tr("English"))
    dialog.add_language("fr", dialog.tr("French"))
    dialog.display(**preferences)
    dialog.show()
    return dialog


def create_main_window(portfolio, player, preferences, name_registry, use_local_isni_backend, native):
    def show_settings_dialog():
        return SettingsDialogController(restart_message_box, preferences, window)

    def create_welcome_screen():
        return make_welcome_screen(on_load_album=ui_commands.load_album_in(portfolio, dialogs),
                                   on_create_new_album=ui_commands.create_new_album_in(portfolio, dialogs),
                                   on_import_album=ui_commands.import_album_in(portfolio, dialogs))

    def create_composition_page(album):
        return make_album_composition_page(dialogs, player, album,
                                           on_move_track=director.move_track_of(album),
                                           on_remove_track=director.remove_track_from(player, album),
                                           on_play_track=director.play_or_stop(player))

    def create_album_page(album):
        return make_album_edition_page(dialogs, show_isni_lookup_dialog, show_activity_indicator_dialog,
                                       show_performer_dialog, show_isni_assignation_failed_message_box, album,
                                       name_registry, use_local_isni_backend)

    def show_isni_lookup_dialog(album, identities):
        return ISNILookupDialogController(window, album, identities)

    def show_performer_dialog(album):
        return PerformerDialogController(window, album)

    def show_activity_indicator_dialog():
        return ActivityIndicatorDialogController(window)

    def show_isni_assignation_failed_message_box(details):
        isni_assignation_failed_message_box(window, details).open()

    def create_album_screen(album):
        def create_track_page(track):
            return TrackEditionPageController(album, track)

        return AlbumScreen(create_composition_page, create_album_page, create_track_page, album)

    dialogs = Dialogs(director, native)
    window = MainWindow(portfolio,
                        on_display=create_welcome_screen,
                        on_close_album=ui_commands.close_album_and(director.remove_album_from(portfolio)),
                        on_save_album=director.export_as_yaml,
                        on_album_created=ui_commands.create_album_and(create_album_screen),
                        on_album_removed=ui_commands.remove_album_and(create_welcome_screen),
                        on_add_files=ui_commands.add_files_to(dialogs),
                        on_add_folder=ui_commands.add_folder_to(dialogs),
                        on_export=ui_commands.export_to(dialogs),
                        on_settings=show_settings_dialog)
    dialogs.parent = window
    portfolio.album_removed.subscribe(lambda album: dialogs.clear())

    return window

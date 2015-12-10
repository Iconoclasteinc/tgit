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

from PyQt5.QtCore import QLocale

from tgit import album_director as director
from tgit import export
from tgit.ui import resources
from tgit.ui.dialogs import Dialogs, MessageBoxes
from tgit.ui.dialogs.about_dialog import AboutDialog
from tgit.ui.helpers import template_file as templates
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog
from tgit.ui.startup_screen import StartupScreen
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog, make_isni_lookup_dialog
from tgit.ui.new_album_page import NewAlbumPage
from tgit.ui.dialogs.performer_dialog import PerformerDialog
from tgit.ui.track_list_page import make_track_list_page
from tgit.ui.album_edition_page import make_album_edition_page
from tgit.ui.album_screen import make_album_screen
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog
from tgit.ui.main_window import MainWindow
from tgit.ui.new_album_page import NewAlbumPage
from tgit.ui.dialogs.performer_dialog import PerformerDialog
from tgit.ui.dialogs.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.dialogs.sign_in_dialog import SignInDialog
from tgit.ui.track_edition_page import make_track_edition_page
from tgit.ui.dialogs.track_selection_dialog import TrackSelectionDialog
from tgit.ui.user_preferences_dialog import UserPreferencesDialog
from tgit.ui.welcome_page import WelcomePage
from tgit.util import browser


def UserPreferencesDialogController(notify_restart_required, preferences, parent):
    dialog = UserPreferencesDialog(parent)

    def save_preferences(prefs):
        preferences.locale = QLocale(prefs["locale"])
        notify_restart_required()

    dialog.display(preferences, save_preferences)
    return dialog


def create_main_window(session, portfolio, player, preferences, cheddar, native, confirm_exit):
    application_dialogs = Dialogs(native, lambda: window)
    messages = MessageBoxes(confirm_exit, lambda: window)

    def show_settings_dialog():
        return UserPreferencesDialogController(messages.restart_required, preferences, window)

    def create_new_album_page():
        return NewAlbumPage(select_album_location=application_dialogs.select_album_destination,
                            select_track=application_dialogs.select_track,
                            check_album_exists=director.album_exists,
                            confirm_overwrite=messages.overwrite_album_confirmation,
                            on_create_album=director.create_album_into(portfolio))

    def create_welcome_page():
        return WelcomePage(select_album=application_dialogs.select_album_to_load,
                           show_load_error=messages.load_album_failed,
                           on_load_album=director.load_album_into(portfolio))

    def create_startup_screen():
        return StartupScreen(create_welcome_page=create_welcome_page,
                             create_new_album_page=create_new_album_page)

    def create_track_list_page(album):
        return make_track_list_page(album, player,
                                    select_tracks=func.partial(application_dialogs.select_tracks, album.type),
                                    on_move_track=director.move_track_of(album),
                                    on_remove_track=director.remove_track_from(album),
                                    on_play_track=player.play,
                                    on_stop_track=player.stop,
                                    on_add_tracks=director.add_tracks_to(album))

    def create_album_page(album):
        return make_album_edition_page(album,
                                       session,
                                       select_identity=application_dialogs.select_identities_in(album),
                                       review_assignation=application_dialogs.review_isni_assignation_in(album),
                                       show_isni_assignation_failed=messages.isni_assignation_failed,
                                       show_cheddar_connection_failed=messages.cheddar_connection_failed,
                                       edit_performers=application_dialogs.edit_performers_in(album),
                                       select_picture=application_dialogs.select_cover,
                                       on_select_picture=director.change_cover_of(album),
                                       on_isni_lookup=director.lookup_isni_using(cheddar, session.current_user),
                                       on_isni_assign=director.assign_isni_using(cheddar, session.current_user, album),
                                       on_remove_picture=director.remove_album_cover_from(album),
                                       on_metadata_changed=director.update_album_from(album))

    def create_track_page_for(album):
        return lambda track: make_track_edition_page(album, track, on_track_changed=director.update_track(track))

    def create_album_screen(album):
        return make_album_screen(album, create_track_list_page, create_album_page, create_track_page_for(album))

    def export_as_soproq():
        from openpyxl import load_workbook
        return export.as_soproq_using(lambda: load_workbook(templates.load(":/templates/soproq.xlsx")),
                                      messages.warn_soproq_default_values)

    window = MainWindow(session,
                        portfolio,
                        confirm_exit=messages.confirm_exit,
                        create_startup_screen=create_startup_screen,
                        create_album_screen=create_album_screen,
                        confirm_close=messages.close_album_confirmation,
                        select_export_destination=application_dialogs.export_as_csv,
                        select_save_as_destination=application_dialogs.save_as_excel,
                        select_tracks=application_dialogs.select_tracks,
                        select_tracks_in_folder=application_dialogs.add_tracks_in_folder,
                        show_save_error=messages.save_album_failed,
                        show_export_error=messages.export_failed,
                        authenticate=application_dialogs.sign_in,
                        on_close_album=director.remove_album_from(portfolio),
                        on_save_album=director.save_album(),
                        on_add_files=director.add_tracks,
                        on_export=export.as_csv,
                        on_settings=show_settings_dialog,
                        on_sign_in=director.sign_in_using(cheddar.authenticate, session),
                        on_sign_out=director.sign_out_using(session),
                        on_about_qt=messages.about_qt,
                        on_about=messages.about_tgit,
                        on_online_help=browser.open_,
                        on_request_feature=browser.open_,
                        on_register=browser.open_,
                        on_transmit_to_soproq=export_as_soproq())

    return window

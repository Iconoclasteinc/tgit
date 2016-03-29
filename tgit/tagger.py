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

import functools

from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtWidgets import QMessageBox

from tgit import album_director as director, artwork, auth, identity, export, ui, project, project_history
from tgit.album_portfolio import AlbumPortfolio
from tgit.audio import open_media_player
from tgit.cheddar import Cheddar
from tgit.project_studio import ProjectStudio
from tgit.settings_backend import SettingsBackend
from tgit.ui.helpers import template_file as templates


def make_tagger(app):
    # todo this will eventually end up in Tagger
    settings = SettingsBackend()
    portfolio = AlbumPortfolio()
    cheddar = Cheddar(host="tagyourmusic.com", port=443, secure=True)
    player = open_media_player(portfolio)
    # todo this will eventually end up in Tagger.close()
    app.aboutToQuit.connect(cheddar.stop)
    app.aboutToQuit.connect(player.dispose)

    tagger = Tagger(settings.load_session(), portfolio, player, cheddar, settings.load_user_preferences())
    tagger.translate(app)
    return tagger


class Tagger:
    _main_window = None
    _project_history = None

    def __init__(self, session, portfolio, player, cheddar, preferences, native=True, confirm_exit=True):
        self._native = native
        self._confirm_exit = confirm_exit
        self._dialogs = ui.Dialogs(native)

        self._portfolio = portfolio
        self._session = session
        self._player = player
        self._cheddar = cheddar
        self._preferences = preferences
        self._project_studio = ProjectStudio()

    def translate(self, app):
        QLocale.setDefault(QLocale(self._preferences.locale))
        for resource in ("qtbase", "tgit"):
            translator = QTranslator(app)
            if translator.load("{0}_{1}".format(resource, self._preferences.locale), ":/"):
                app.installTranslator(translator)

    def show(self):
        self._project_history = project_history.load(self._project_studio)
        self._main_window = self._make_main_window()
        self._main_window.show()

    def _make_main_window(self):
        return ui.MainWindow(self._session,
                             self._portfolio,
                             confirm_exit=self._show_exit_confirmation_message,
                             create_startup_screen=self._startup_screen,
                             create_project_screen=self._project_screen,
                             confirm_close=self._show_close_project_confirmation_message,
                             select_export_destination=self._dialogs.export_as_csv,
                             select_save_as_destination=self._dialogs.save_as_excel,
                             select_tracks=self._dialogs.select_tracks,
                             select_tracks_in_folder=self._dialogs.add_tracks_in_folder,
                             show_save_error=self._show_save_project_failed_message,
                             show_export_error=self._show_export_project_failed_message,
                             on_close_project=director.remove_album_from(self._portfolio),
                             on_save_project=director.save_album(),
                             on_add_files=director.add_tracks,
                             on_export=export.as_csv,
                             on_settings=self._show_settings_dialog,
                             on_sign_in=self._open_sign_in_dialog,
                             on_sign_out=auth.sign_out_from(self._session),
                             on_about_qt=self._show_about_qt_message,
                             on_about=self._show_about_dialog,
                             on_online_help=ui.browser.open_,
                             on_request_feature=ui.browser.open_,
                             on_register=ui.browser.open_,
                             on_transmit_to_soproq=self._export_as_soproq())

    def _startup_screen(self):
        return ui.StartupScreen(self._make_welcome_page, self._new_project_page)

    def _project_screen(self, project_):
        return ui.make_project_screen(project_, self._project_edition_page, self._track_page_for(project_))

    def _new_project_page(self):
        return ui.make_new_project_page(select_location=self._dialogs.select_project_destination,
                                        select_track=self._dialogs.select_track,
                                        check_project_exists=director.album_exists,
                                        confirm_overwrite=self._show_overwrite_project_confirmation_message,
                                        on_create_project=director.create_album_into(self._portfolio))

    def _make_welcome_page(self):
        return ui.make_welcome_page(self._project_history,
                                    select_project=self._dialogs.select_project_to_load,
                                    show_load_error=self._show_load_project_failed_message,
                                    on_load_project=project.load(self._project_studio, self._portfolio))

    def _track_list_tab(self, project_):
        return ui.make_track_list_tab(project_,
                                      self._player,
                                      select_tracks=functools.partial(self._dialogs.select_tracks, project_.type),
                                      on_move_track=director.move_track_of(project_),
                                      on_remove_track=director.remove_track_from(project_),
                                      on_play_track=self._player.play,
                                      on_stop_track=self._player.stop,
                                      on_add_tracks=director.add_tracks_to(project_))

    @staticmethod
    def _musician_tab(project_):
        return ui.make_musician_tab(project_,
                                    on_metadata_changed=director.update_album_from(project_))

    def _project_edition_page(self, project_):
        return ui.make_project_edition_page(project_,
                                            self._session,
                                            track_list_tab=self._track_list_tab,
                                            musician_tab=self._musician_tab,
                                            on_select_artwork=self._open_artwork_selection_dialog,
                                            on_isni_changed=project_.add_isni,
                                            on_isni_local_lookup=director.lookup_isni_in(project_),
                                            on_select_identity=self._open_isni_dialog,
                                            on_remove_artwork=director.remove_album_cover_from(project_),
                                            on_metadata_changed=director.update_album_from(project_))

    @staticmethod
    def _track_page_for(project_):
        def track_page(track):
            return ui.make_track_edition_page(project_,
                                              track,
                                              on_track_changed=director.update_track(track),
                                              on_isni_local_lookup=director.lookup_isni_in(project_),
                                              on_ipi_local_lookup=director.lookup_ipi_in(project_),
                                              on_ipi_changed=director.add_ipi_to(project_))

        return track_page

    def _open_isni_dialog(self, query):
        selection = identity.IdentitySelection(self._portfolio[0], query)
        ui.make_isni_lookup_dialog(query, selection,
                                   on_lookup=identity.launch_lookup(self._cheddar, self._session, selection),
                                   on_assign=self._open_isni_review_dialog(selection),
                                   parent=self._main_window).open()

    def _open_isni_review_dialog(self, selection):
        return lambda: ui.make_isni_assignation_review_dialog(
            selection,
            on_assign=identity.launch_assignation(self._cheddar, self._session, selection),
            parent=self._main_window).open()

    def _open_sign_in_dialog(self):
        login = auth.Login(self._session)
        return ui.make_sign_in_dialog(login,
                                      on_sign_in=auth.sign_in(login, self._cheddar),
                                      parent=self._main_window).open()

    def _open_artwork_selection_dialog(self):
        artwork_selection = artwork.ArtworkSelection(self._portfolio[0], self._preferences)
        return ui.make_artwork_selection_dialog(artwork_selection,
                                                on_file_selected=artwork.load(artwork_selection),
                                                native=self._native,
                                                parent=self._main_window).open()

    def _show_settings_dialog(self):
        return ui.make_user_preferences_dialog(self._preferences, self._show_restart_required_message,
                                               on_preferences_changed=director.update_preferences(self._preferences),
                                               parent=self._main_window).show()

    def _export_as_soproq(self):
        from openpyxl import load_workbook
        return export.as_soproq_using(lambda: load_workbook(templates.load(":/templates/soproq.xlsx")),
                                      self._show_default_values_used_for_soproq_export_message)

    def _show_about_dialog(self):
        ui.make_about_dialog(self._main_window).show()

    def _show_overwrite_project_confirmation_message(self, **handlers):
        ui.messages.overwrite_project_confirmation(self._main_window, **handlers).open()

    def _show_close_project_confirmation_message(self, **handlers):
        ui.messages.close_project_confirmation(self._main_window, **handlers).open()

    def _show_load_project_failed_message(self, error):
        ui.messages.load_project_failed(self._main_window).open()

    def _show_save_project_failed_message(self, error):
        ui.messages.save_project_failed(self._main_window).open()

    def _show_export_project_failed_message(self, error):
        ui.messages.export_project_failed(self._main_window).open()

    def _show_default_values_used_for_soproq_export_message(self):
        ui.messages.default_values_used_for_soproq_export(self._main_window).open()

    def _show_restart_required_message(self):
        ui.messages.restart_required(self._main_window).open()

    def _show_about_qt_message(self):
        ui.messages.about_qt(self._main_window)

    def _show_exit_confirmation_message(self):
        if not self._confirm_exit:
            return True

        return ui.messages.quit_confirmation(self._main_window).exec() == QMessageBox.Yes

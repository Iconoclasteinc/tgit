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

from tgit import album_director as director, artwork, auth, identity, export, ui
from tgit.ui.helpers import template_file as templates
from tgit.album_portfolio import AlbumPortfolio
from tgit.audio import open_media_player
from tgit.cheddar import Cheddar
from tgit.settings_backend import SettingsBackend


def make_tagger(app):
    settings = SettingsBackend()
    portfolio = AlbumPortfolio()
    cheddar = Cheddar(host="tagyourmusic.com", port=443, secure=True)
    player = open_media_player(portfolio)

    app.lastWindowClosed.connect(cheddar.stop)
    app.lastWindowClosed.connect(player.dispose)

    return Tagger(settings.load_session(), portfolio, player, cheddar, settings.load_user_preferences())


class Tagger:
    _main_window = None

    def __init__(self, session, portfolio, player, cheddar, preferences, native=True, confirm_exit=True):
        self._preferences = preferences
        self._native = native
        self._cheddar = cheddar
        self._player = player
        self._session = session
        self._messages = ui.MessageBoxes(confirm_exit)
        self._dialogs = ui.Dialogs(native)
        self._portfolio = portfolio
        self._identity_lookup = identity.IdentityLookup()
        self._login = auth.Login(session)
        self._artwork_selection = artwork.ArtworkSelection(self._portfolio, ui.locations.Pictures)

    def show(self):
        self._main_window = ui.MainWindow(self._session,
                                          self._portfolio,
                                          confirm_exit=self._messages.confirm_exit,
                                          create_startup_screen=self._startup_screen,
                                          create_project_screen=self._project_screen,
                                          confirm_close=self._messages.close_project_confirmation,
                                          select_export_destination=self._dialogs.export_as_csv,
                                          select_save_as_destination=self._dialogs.save_as_excel,
                                          select_tracks=self._dialogs.select_tracks,
                                          select_tracks_in_folder=self._dialogs.add_tracks_in_folder,
                                          show_save_error=self._messages.save_project_failed,
                                          show_export_error=self._messages.export_failed,
                                          on_close_album=director.remove_album_from(self._portfolio),
                                          on_save_album=director.save_album(),
                                          on_add_files=director.add_tracks,
                                          on_export=export.as_csv,
                                          on_settings=self._show_settings_dialog,
                                          on_sign_in=self._show_sign_in_dialog,
                                          on_sign_out=auth.sign_out_from(self._session),
                                          on_about_qt=self._messages.about_qt,
                                          on_about=self._messages.about_tgit,
                                          on_online_help=ui.browser.open_,
                                          on_request_feature=ui.browser.open_,
                                          on_register=ui.browser.open_,
                                          on_transmit_to_soproq=self._export_as_soproq())
        self._main_window.show()

    def translate(self, app):
        QLocale.setDefault(QLocale(self._preferences.locale))
        for resource in ("qtbase", "tgit"):
            translator = QTranslator(app)
            if translator.load("{0}_{1}".format(resource, self._preferences.locale), ":/"):
                app.installTranslator(translator)

    def _startup_screen(self):
        return ui.StartupScreen(self._welcome_page, self._new_project_page)

    def _project_screen(self, album):
        return ui.make_project_screen(album, self._project_edition_page, self._track_page_for(album))

    def _new_project_page(self):
        return ui.make_new_project_page(select_location=self._dialogs.select_project_destination,
                                        select_track=self._dialogs.select_track,
                                        check_project_exists=director.album_exists,
                                        confirm_overwrite=self._messages.overwrite_project_confirmation,
                                        on_create_project=director.create_album_into(self._portfolio))

    def _welcome_page(self):
        return ui.make_welcome_page(select_project=self._dialogs.select_project_to_load,
                                    show_load_error=self._messages.load_project_failed,
                                    on_load_project=director.load_album_into(self._portfolio))

    def _track_list_tab(self, album):
        return ui.make_track_list_tab(album,
                                      self._player,
                                      select_tracks=functools.partial(self._dialogs.select_tracks, album.type),
                                      on_move_track=director.move_track_of(album),
                                      on_remove_track=director.remove_track_from(album),
                                      on_play_track=self._player.play,
                                      on_stop_track=self._player.stop,
                                      on_add_tracks=director.add_tracks_to(album))

    def _project_edition_page(self, album):
        return ui.make_project_edition_page(album,
                                            self._session,
                                            self._identity_lookup,
                                            track_list_tab=self._track_list_tab,
                                            on_select_artwork=self._show_artwork_selection_dialog,
                                            on_isni_changed=director.add_isni_to(album),
                                            on_isni_local_lookup=director.lookup_isni_in(album),
                                            on_select_identity=self._show_isni_dialog,
                                            on_remove_artwork=director.remove_album_cover_from(album),
                                            on_metadata_changed=director.update_album_from(album))

    @staticmethod
    def _track_page_for(album):
        def track_page(track):
            return ui.make_track_edition_page(album,
                                              track,
                                              on_track_changed=director.update_track(track),
                                              on_isni_local_lookup=director.lookup_isni_in(album),
                                              on_ipi_local_lookup=director.lookup_ipi_in(album),
                                              on_ipi_changed=director.add_ipi_to(album))

        return track_page

    def _show_isni_dialog(self, query):
        return ui.open_isni_lookup_dialog(query, self._identity_lookup,
                                          on_lookup=identity.launch_lookup(self._cheddar, self._session,
                                                                           self._identity_lookup),
                                          parent=self._main_window)

    def _show_sign_in_dialog(self):
        return ui.open_sign_in_dialog(self._login,
                                      on_sign_in=auth.sign_in(self._login, self._cheddar),
                                      parent=self._main_window)

    def _show_artwork_selection_dialog(self):
        return ui.open_artwork_selection_dialog(self._artwork_selection,
                                                on_file_selected=artwork.load(self._artwork_selection),
                                                native=self._native,
                                                parent=self._main_window)

    def _show_settings_dialog(self):
        return ui.open_user_preferences_dialog(self._main_window, self._preferences, self._messages.restart_required,
                                               director.update_preferences(self._preferences))

    def _export_as_soproq(self):
        from openpyxl import load_workbook
        return export.as_soproq_using(lambda: load_workbook(templates.load(":/templates/soproq.xlsx")),
                                      self._messages.warn_soproq_default_values)

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

from tgit import album_director as director
from tgit import export, auth, identity
from tgit.ui import resources, browser
from tgit.ui.dialogs import Dialogs, MessageBoxes
from tgit.ui.dialogs.sign_in_dialog import open_sign_in_dialog
from tgit.ui.helpers import template_file as templates
from tgit.ui.main_window import MainWindow
from tgit.ui.pages import Pages
from tgit.ui.user_preferences_dialog import open_user_preferences_dialog


def create_main_window(session, portfolio, player, prefs, cheddar, native, confirm_exit):
    login = auth.Login(session)
    identity_lookup = identity.IdentityLookup()

    application_dialogs = Dialogs(native, lambda: window)
    messages = MessageBoxes(confirm_exit, lambda: window)
    application_pages = Pages(application_dialogs, messages, session, portfolio, player, cheddar, identity_lookup,
                              native, lambda: window)

    def show_settings_dialog():
        return open_user_preferences_dialog(window, prefs, messages.restart_required,
                                            director.update_preferences(prefs))

    def export_as_soproq():
        from openpyxl import load_workbook
        return export.as_soproq_using(lambda: load_workbook(templates.load(":/templates/soproq.xlsx")),
                                      messages.warn_soproq_default_values)

    def show_sign_in_dialog():
        return open_sign_in_dialog(window, login, auth.sign_in(login, authenticator=cheddar))

    window = MainWindow(session,
                        portfolio,
                        confirm_exit=messages.confirm_exit,
                        create_startup_screen=application_pages.startup_screen,
                        create_project_screen=application_pages.project_screen,
                        confirm_close=messages.close_project_confirmation,
                        select_export_destination=application_dialogs.export_as_csv,
                        select_save_as_destination=application_dialogs.save_as_excel,
                        select_tracks=application_dialogs.select_tracks,
                        select_tracks_in_folder=application_dialogs.add_tracks_in_folder,
                        show_save_error=messages.save_project_failed,
                        show_export_error=messages.export_failed,
                        on_close_album=director.remove_album_from(portfolio),
                        on_save_album=director.save_album(),
                        on_add_files=director.add_tracks,
                        on_export=export.as_csv,
                        on_settings=show_settings_dialog,
                        on_sign_in=show_sign_in_dialog,
                        on_sign_out=director.sign_out_from(session),
                        on_about_qt=messages.about_qt,
                        on_about=messages.about_tgit,
                        on_online_help=browser.open_,
                        on_request_feature=browser.open_,
                        on_register=browser.open_,
                        on_transmit_to_soproq=export_as_soproq())

    return window

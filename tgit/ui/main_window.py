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

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QAction

from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.observer import Observer
from tgit.ui.rescue import rescue

StyleSheet = """
    QMessageBox[style=QMacStyle] {
        messagebox-warning-icon: url(:/images/warning.png);
    }

    #qt_msgbox_informativelabel[style=QMacStyle] {
        font: normal 11px;
        margin-bottom: 5px;
    }
"""


@Observer
class MainWindow(QMainWindow, UIFile):
    _closing = False
    _project = None

    TRACK_ACTIONS_START_INDEX = 2

    def __init__(self, session, studio, confirm_exit, show_save_error, show_export_error, create_startup_screen,
                 create_project_screen, confirm_close, select_export_destination, select_save_as_destination,
                 select_tracks, select_tracks_in_folder, **handlers):
        super().__init__()
        self._confirm_exit = confirm_exit
        self._show_save_error = show_save_error
        self._show_export_error = show_export_error
        self._create_startup_screen = create_startup_screen
        self._create_project_screen = create_project_screen
        self._confirm_close = confirm_close
        self._select_tracks_in_folder = select_tracks_in_folder
        self._select_tracks = select_tracks
        self._select_export_destination = select_export_destination
        self._select_save_as_destination = select_save_as_destination

        self._setup_ui()
        self._setup_menu_bar()
        self._setup_signals(studio, session)
        for name, handler in handlers.items():
            getattr(self, name)(handler)

        self._project_dependent_action = [
            self._add_files_action,
            self._add_folder_action,
            self._export_action,
            self._close_project_action,
            self._save_project_action
        ]

        self.display_startup_screen()
        if session.opened:
            self.user_signed_in(session.current_user)

    def enable_project_actions(self, project):
        self._navigate_menu.setEnabled(True)
        self._transmit_menu.setEnabled(True)
        for action in self._project_dependent_action:
            action.setEnabled(True)
            action.setData(project)

    def disable_project_actions(self):
        self._navigate_menu.setDisabled(True)
        self._transmit_menu.setDisabled(True)
        for action in self._project_dependent_action:
            action.setEnabled(False)
            action.setData(None)

    def display_startup_screen(self, *_):
        self._project = None
        self.disable_project_actions()
        self._clear_track_actions()
        self._change_screen(self._create_startup_screen())

    def display_project_screen(self, project):
        self._project = project
        self.enable_project_actions(project)
        self._create_track_actions()
        self._change_screen(self._create_project_screen(project))

        self.subscribe(project.track_inserted, self._rebuild_track_actions)
        self.subscribe(project.track_removed, self._rebuild_track_actions)
        self.subscribe(project.track_moved, self._rebuild_track_actions)

    def user_signed_in(self, user):
        self._sign_in_action.setVisible(False)
        self._sign_out_action.setEnabled(True)
        self._logged_user_action.setText(user.email)
        self._logged_user_action.setVisible(True)

    def user_signed_out(self, _):
        self._sign_out_action.setEnabled(False)
        self._sign_in_action.setVisible(True)
        self._logged_user_action.setVisible(False)

    def on_close_project(self, handler):
        def confirm_project_close():
            self._confirm_close(on_accept=lambda: handler(self._project))

        self._close_project_action.triggered.connect(confirm_project_close)

    def on_save_project(self, handler):
        def save_project():
            if self.focusWidget() is not None:
                self.focusWidget().clearFocus()

            with rescue(on_error=self._show_save_error):
                handler(self._project)

        self._save_project_action.triggered.connect(save_project)

    def on_export(self, on_export):
        def export(destination):
            with rescue(on_error=self._show_export_error):
                on_export(self._project, destination)

        self._export_action.triggered.connect(
            lambda *_: self._select_export_destination(export, self._project.release_name))

    def on_transmit_to_soproq(self, on_transmit_to_soproq):
        def save_as(destination):
            with rescue(on_error=self._show_export_error):
                on_transmit_to_soproq(self._project, destination)

        self._soproq_action.triggered.connect(
            lambda _: self._select_save_as_destination(save_as, self._project.release_name))

    def on_settings(self, on_settings):
        self._settings_action.triggered.connect(on_settings)

    def on_add_files(self, on_add_files):
        def add_files(*files):
            on_add_files(self._project, *files)

        self._add_files_action.triggered.connect(lambda *_: self._select_tracks(self._project.type, add_files))
        self._add_folder_action.triggered.connect(lambda *_: self._select_tracks_in_folder(self._project.type, add_files))

    def on_about(self, handler):
        self._about_action.triggered.connect(handler)

    def on_about_qt(self, handler):
        self._about_qt_action.triggered.connect(handler)

    def on_online_help(self, handler):
        self._online_help_action.triggered.connect(
            lambda _: handler(self.tr("http://blog.tagyourmusic.com/en")))

    def on_register(self, handler):
        self._register_action.triggered.connect(
            lambda _: handler(self.tr("https://tagyourmusic.com/en")))

    def on_request_feature(self, handler):
        self._request_feature_action.triggered.connect(
            lambda _: handler(self.tr("mailto:support@tagyourmusic.com?subject=[TGiT] I want more!")))

    def on_sign_in(self, handler):
        self._sign_in_action.triggered.connect(lambda _: handler())

    def on_sign_out(self, handler):
        self._sign_out_action.triggered.connect(lambda _: handler())

    def _setup_ui(self):
        self._load(":/ui/main_window.ui")
        self.setStyleSheet(StyleSheet)

    def _setup_menu_bar(self):
        self._to_project_edition_action.triggered.connect(self._to_project_edition_page)
        self._exit_action.triggered.connect(self.close)
        self._exit_action.setShortcut(QKeySequence.Quit)
        self._close_project_action.setShortcut(QKeySequence.Close)
        self._save_project_action.setShortcut(QKeySequence.Save)

    def _setup_signals(self, studio, session):
        self.subscribe(studio.on_project_closed, self.display_startup_screen)
        self.subscribe(studio.on_project_opened, self.display_project_screen)
        self.subscribe(session.user_signed_in, self.user_signed_in)
        self.subscribe(session.user_signed_out, self.user_signed_out)

    def _close_current_screen(self):
        if self.centralWidget() is not None:
            widget = self.takeCentralWidget()
            widget.close()

    def _change_screen(self, screen):
        self._close_current_screen()
        self.setCentralWidget(screen)

    def _rebuild_track_actions(self, *_):
        self._clear_track_actions()
        self._create_track_actions()

    def _create_track_actions(self):
        def format_name(track):
            return "{} - {}".format(track.track_number, track.track_title)

        def update_entry(action, track):
            action.setText(format_name(track))

        def add_entry(track):
            action = QAction(format_name(track), self)
            action.triggered.connect(lambda _: self._to_track_page(track))
            self._navigate_menu.addAction(action)
            return action

        for each_track in self._project.tracks:
            self.unsubscribe(each_track.metadata_changed)
            each_action = add_entry(each_track)
            self.subscribe(each_track.metadata_changed, lambda track: update_entry(each_action, track))

    def _clear_track_actions(self):
        for action in self._navigate_menu.actions()[self.TRACK_ACTIONS_START_INDEX:]:
            self._navigate_menu.removeAction(action)
            action.setParent(None)

    def _to_project_edition_page(self):
        self.centralWidget().to_project_edition_page()

    def _to_track_page(self, track):
        self.centralWidget().to_track_page(track.track_number - 1)

    def close(self):
        closed = super().close()
        if closed:
            self._close_current_screen()
        return closed

    def closeEvent(self, event):
        if self._should_close_immediately:
            return

        if self._confirm_exit():
            # There is an issue on MAC which results on the closeEvent being called twice when exiting the application.
            # Setting _closing to True will prevent the confirmation message to be seen twice.
            self._closing = True
        else:
            event.ignore()

    @property
    def _should_close_immediately(self):
        return self._closing or self._project is None

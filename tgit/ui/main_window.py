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

import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QAction

from tgit.ui.helpers import ui_file
from tgit.ui.observer import Observer
from tgit.ui.rescue import rescue

windows = sys.platform == "win32"
mac = sys.platform == "darwin"

StyleSheet = """
    QComboBox QAbstractItemView {
        selection-background-color:#F08450;
    }

    #activity-indicator-dialog-frame {
        border: 1px solid #DDDDDD;
    }

    QGroupBox {
        border: 1px solid #DDDDDD;
        border-bottom: 2px solid rgba(0, 0, 0, 20%);
        background-color: white;
        padding: 17px 14px 14px 0px;
        margin: 5px 8px;
        font-size: 10px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 1px;
        padding: 0 3px;
        color: #777777;
        border: 1px solid #DFDFDF;
        background-color: #F7F7F7;
     }

    #performer-dialog #form-box QPushButton#add-performer {
        background-color: #F25C0A;
        border: 2px solid #F25C0A;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 10px 10px 7px 10px;
        margin-left: 10px;
    }

    #performer-dialog #form-box QPushButton {
        background-color: #BFBFBF;
        border: 2px solid #BFBFBF;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        font-size: 10px;
        padding: 3px 10px;
    }

    #performer-dialog #form-box QPushButton:hover, #performer-dialog #form-box QPushButton:focus {
        background-color: #A6A6A6;
        border-color: #A6A6A6;
    }

    #performer-dialog #form-box QPushButton:pressed {
        border: 2px solid transparent;
    }

    #performer-dialog #form-box QPushButton#add-performer {
        font-size: 10px;
        padding: 3px 10px;
        margin: 0;
    }

    #performer-dialog #form-box QPushButton#add-performer:hover,
    #performer-dialog #form-box QPushButton#add-performer:focus {
        background-color: #D95109;
        border-color: #D95109;
    }

    #performer-dialog QPushButton#add-performer:pressed {
        border: 2px solid white;
    }

    #performer-dialog QLineEdit,
    #track-edition-page QLineEdit, #track-edition-page TextArea, #track-edition-page QComboBox,
    #track-edition-page QComboBox::drop-down, #track-edition-page QComboBox QAbstractItemView {
        background-color: #F9F9F9;
        border: 1px solid #B1B1B1;
        color: #222222;
        min-height: 20px;
    }

    #performer-dialog QLineEdit,
    #track-edition-page QLineEdit, #track-edition-page TextArea, #track-edition-page QComboBox {
        selection-background-color: #F2C1A7;
        selection-color: #222222;
    }

    #performer-dialog QLineEdit:focus,
    #track-edition-page QLineEdit:focus, #track-edition-page TextArea:focus, #track-edition-page QComboBox:focus,
    #track-edition-page QComboBox:on, #track-edition-page QComboBox::drop-down:focus,
    #track-edition-page QComboBox::drop-down:on, #track-edition-page QComboBox QAbstractItemView:focus  {
        border: 1px solid #F79D6C;
    }

    #performer-dialog QLineEdit:disabled,
    #track-edition-page QLineEdit:disabled, #track-edition-page TextArea:disabled,
    #track-edition-page QSpinBox:disabled {
        background-color: #FCFCFC;
        border-color: #E7E7E7;
        color: #C2C2C2;
    }

    #track-edition-page QComboBox:disabled, #track-edition-page QComboBox::drop-down:disabled,
    #track-edition-page QTimeEdit:disabled {
        background-color: #FCFCFC;
        border-color: #E7E7E7;
        color: #C2C2C2;
    }

    #track-edition-page QLabel {
        color: #444444;
        min-width: 175px;
    }

    #track-edition-page #content QLabel {
        min-width: 125px;
    }

    #track-edition-page QLabel:disabled {
        color: #C2C2C2;
    }

    #track-edition-page QComboBox::drop-down {
        padding: 0;
        margin: 0;
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 20px;
    }

    #track-edition-page QComboBox::down-arrow {
        image: url(:/down-arrow.png);
    }

    #track-edition-page QComboBox::down-arrow:on, #track-edition-page QComboBox::down-arrow:focus {
        image: url(:/down-arrow-on.png);
    }

    #album-banner {
        padding-left: 14px;
        max-height: 50px;
    }

    #album-banner #album-cover {
        min-width: 50px;
        max-width: 50px;
        min-height: 50px;
        max-height: 50px;
        background-color: #F9F9F9;
        border: 1px solid #B8B8B8;
        margin-right: 15px;
    }

    #album-banner QLabel {
        color: #777777;
        padding: 0;
        margin: 0;
        min-width: 0;
    }

    #album-banner QLabel[title='h2'] {
        font-size: 22px;
        min-width: 300px;
        max-width: 300px;
    }

    #album-banner QLabel[title='h3'] {
        font-size: 14px;
        min-width: 300px;
        max-width: 300px;
    }

    #track-edition-page #software-notice {
        font-size: 10px;
        margin-right: 8px;
    }

    #isni-lookup-dialog #results-exceeds-shown,
    #isni-lookup-dialog #no-result-message,
    #isni-lookup-dialog #connection-error-message {
        color: #F25C0A;
    }

    QMessageBox[style=QMacStyle] {
        messagebox-warning-icon: url(:/images/warning.png);
    }

    #qt_msgbox_informativelabel[style=QMacStyle] {
        font: normal 11px;
    }
 """

if mac:
    StyleSheet += """
        #track-edition-page QComboBox {
            padding-left: 1px;
            padding-top: 1px;
            margin-left: 3px;
            margin-right: 2px;
        }
    """


class HandlerRegistrar:
    def _register(self, **handlers):
        for name, handler in handlers.items():
            getattr(self, name)(handler)


@Observer
class MainWindow(QMainWindow, HandlerRegistrar):
    _closing = False
    _album = None

    TRACK_ACTIONS_START_INDEX = 3

    def __init__(self, portfolio, confirm_exit, show_save_error, show_export_error, create_startup_screen,
                 create_album_screen, confirm_close, select_export_destination, select_tracks, select_tracks_in_folder,
                 **handlers):
        super().__init__()
        self._confirm_exit = confirm_exit
        self._show_save_error = show_save_error
        self._show_export_error = show_export_error
        self._create_startup_screen = create_startup_screen
        self._create_album_screen = create_album_screen
        self._confirm_close = confirm_close
        self._select_tracks_in_folder = select_tracks_in_folder
        self._select_tracks = select_tracks
        self._select_export_destination = select_export_destination

        self._setup_ui()
        self._setup_menu_bar()
        self._setup_signals(portfolio)
        self._register(**handlers)

        self._album_dependent_action = [
            self.add_files_action,
            self.add_folder_action,
            self.export_action,
            self.close_album_action,
            self.save_album_action
        ]

        self.display_startup_screen()

    def enable_album_actions(self, album):
        self.navigate_menu.setEnabled(True)
        for action in self._album_dependent_action:
            action.setEnabled(True)
            action.setData(album)

    def disable_album_actions(self):
        self.navigate_menu.setDisabled(True)
        for action in self._album_dependent_action:
            action.setEnabled(False)
            action.setData(None)

    def display_startup_screen(self, *_):
        self._album = None
        self.disable_album_actions()
        self._clear_track_actions()
        self._change_screen(self._create_startup_screen())

    def display_album_screen(self, album):
        self._album = album
        self.enable_album_actions(album)
        self._create_track_actions()
        self._change_screen(self._create_album_screen(album))

        self.subscribe(album.track_inserted, self._rebuild_track_actions)
        self.subscribe(album.track_removed, self._rebuild_track_actions)

    def on_close_album(self, on_close_album):
        def confirm_album_close():
            self._confirm_close(on_accept=lambda: on_close_album(self._album))

        self.close_album_action.triggered.connect(confirm_album_close)

    def on_save_album(self, on_save_album):
        def save_album():
            if self.focusWidget() is not None:
                self.focusWidget().clearFocus()

            with rescue(on_error=self._show_save_error):
                on_save_album(self._album)

        self.save_album_action.triggered.connect(save_album)

    def on_export(self, on_export):
        def export(destination):
            with rescue(on_error=self._show_export_error):
                on_export(self._album, destination)

        self.export_action.triggered.connect(
            lambda *_: self._select_export_destination(export, self._album.release_name))

    def on_settings(self, on_settings):
        self.settings_action.triggered.connect(on_settings)

    def on_add_files(self, on_add_files):
        def add_files(*files):
            on_add_files(self._album, *files)

        self.add_files_action.triggered.connect(lambda *_: self._select_tracks(self._album.type, add_files))
        self.add_folder_action.triggered.connect(lambda *_: self._select_tracks_in_folder(self._album.type, add_files))

    def _setup_ui(self):
        ui_file.load(":/ui/main_window.ui", self)
        self.setStyleSheet(StyleSheet)

    def _setup_menu_bar(self):
        self.to_album_edition_action.triggered.connect(self._to_album_edition_page)
        self.to_track_list_action.triggered.connect(self._to_track_list_page)
        self.exit_action.triggered.connect(self.close)

        if windows:
            self.settings_action.setText(self.tr(self.settings_action.text()))

        self.exit_action.setShortcut(QKeySequence.Quit)
        self.close_album_action.setShortcut(QKeySequence.Close)
        self.save_album_action.setShortcut(QKeySequence.Save)

    def _setup_signals(self, portfolio):
        self.subscribe(portfolio.album_removed, self.display_startup_screen)
        self.subscribe(portfolio.album_created, self.display_album_screen)

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
        for track in self._album.tracks:
            self.navigate_menu.addAction(self._create_track_action(track))

    def _create_track_action(self, track):
        def format_name(number, title):
            return "{0} - {1}".format(number, title)

        def update_name(menu_item, metadata):
            menu_item.setText("{0} - {1}".format(metadata["track_number"], metadata["track_title"]))

        action = QAction(format_name(track.track_number, track.track_title), self)
        action.triggered.connect(lambda _: self._to_track_page(track.track_number))
        self.subscribe(track.metadata_changed, lambda metadata: update_name(action, metadata))

        return action

    def _clear_track_actions(self):
        for action in self.navigate_menu.actions()[self.TRACK_ACTIONS_START_INDEX:]:
            self.navigate_menu.removeAction(action)
            action.setParent(None)

    def _to_album_edition_page(self):
        self.centralWidget().show_album_edition_page()

    def _to_track_list_page(self):
        self.centralWidget().show_track_list_page()

    def _to_track_page(self, track_number):
        self.centralWidget().show_track_page(track_number)

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
        return self._closing or self._album is None

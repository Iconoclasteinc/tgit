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

from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QAction

from tgit.ui.helpers import ui_file
from tgit.ui.observer import Observer
from tgit.ui.rescue import rescue

windows = sys.platform == "win32"

StyleSheet = """
    MainWindow {
        background-color: #F6F6F6;
        margin: 0;
        padding: 0;
    }

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

    #album-edition-page QGroupBox#pictures {
        padding: 13px 14px 10px 14px;
     }

    #album-edition-page QGroupBox#pictures::title {
        background-color: transparent;
        color: transparent;
        border: none;
     }

    #album-edition-page QGroupBox#pictures #front-cover {
        min-width: 350px;
        max-width: 350px;
        min-height: 350px;
        max-height: 350px;
        background-color: #F9F9F9;
        border: 1px solid #F79D6C;
    }

    #album-edition-page QPushButton#select-picture {
        background-image: url(:/add-picture.png);
        background-repeat: no-repeat;
        background-position: left center;
        background-origin: border;
        background-color: #F25C0A;
        border: 2px solid #F25C0A;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        padding: 10px 10px 7px 34px;
    }

    #performer-dialog #form-box QPushButton#add-performer,
    #album-edition-page #album-box QPushButton,
    #album-edition-page QPushButton#remove-picture {
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

    #performer-dialog #form-box QPushButton#add-performer, #album-edition-page #album-box QPushButton {
        font-size: 10px;
        padding: 3px 10px;
        margin: 0;
    }

    #album-edition-page #album-box QPushButton:disabled {
        border-color: #ED8D58;
        background-color: #ED8D58;
    }

    #performer-dialog #form-box QPushButton#add-performer:hover,
    #performer-dialog #form-box QPushButton#add-performer:focus,
    #album-edition-page #album-box QPushButton:hover,
    #album-edition-page #album-box QPushButton:focus,
    #album-edition-page QPushButton#select-picture:hover,
    #album-edition-page QPushButton#select-picture:focus,
    #album-edition-page QPushButton#remove-picture:hover,
    #album-edition-page QPushButton#remove-picture:focus {
        background-color: #D95109;
        border-color: #D95109;
    }

    #performer-dialog QPushButton#add-performer:pressed,
    #album-edition-page #album-box QPushButton:pressed,
    #album-edition-page QPushButton#select-picture:pressed,
    #album-edition-page QPushButton#remove-picture:pressed {
        border: 2px solid white;
    }

    #performer-dialog QLineEdit,
    #album-edition-page QLineEdit, #album-edition-page TextArea, #album-edition-page QComboBox,
    #album-edition-page QComboBox::drop-down, #album-edition-page QComboBox QAbstractItemView,
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
    #album-edition-page QLineEdit:focus, #album-edition-page TextArea:focus, #album-edition-page QComboBox:focus,
    #album-edition-page QComboBox:on, #album-edition-page QComboBox::drop-down:focus,
    #album-edition-page QComboBox::drop-down:on, #album-edition-page QComboBox QAbstractItemView:focus,
    #track-edition-page QLineEdit:focus, #track-edition-page TextArea:focus, #track-edition-page QComboBox:focus,
    #track-edition-page QComboBox:on, #track-edition-page QComboBox::drop-down:focus,
    #track-edition-page QComboBox::drop-down:on, #track-edition-page QComboBox QAbstractItemView:focus  {
        border: 1px solid #F79D6C;
    }

    #performer-dialog QLineEdit:disabled,
    #album-edition-page QLineEdit:disabled, #album-edition-page TextArea:disabled,
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

    #album-edition-page QCheckBox {
        min-height: 20px;
        padding: 1px 2px 2px 2px;
    }

    QCheckBox::indicator {
        width: 14px;
        height: 14px;
        subcontrol-position: left center;
    }

    QCheckBox::indicator:unchecked {
        image: url(:/checkbox.png);
    }

    QCheckBox::indicator:unchecked:hover, QCheckBox::indicator:unchecked:focus {
        image: url(:/checkbox-hover.png);
    }

    QCheckBox::indicator:unchecked:pressed {
        image: url(:/checkbox-pressed.png);
    }

    QCheckBox::indicator:checked {
        image: url(:/checkbox-checked.png);
    }

    QCheckBox::indicator:checked:hover, QCheckBox::indicator:checked:focus {
        image: url(:/checkbox-checked-hover.png);
    }

    QCheckBox::indicator:checked:pressed {
        image: url(:/checkbox-checked-pressed.png);
    }

    #album-edition-page QLabel, #track-edition-page QLabel {
        color: #444444;
        min-width: 175px;
    }

    #track-edition-page #content QLabel {
        min-width: 125px;
    }

    #album-edition-page QLabel:disabled, #track-edition-page QLabel:disabled {
        color: #C2C2C2;
    }

    #album-edition-page QComboBox::drop-down, #track-edition-page QComboBox::drop-down {
        padding: 0;
        margin: 0;
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 20px;
    }

    #album-edition-page QComboBox::down-arrow, #track-edition-page QComboBox::down-arrow {
        image: url(:/down-arrow.png);
    }

    #album-edition-page QComboBox::down-arrow:on, #album-edition-page QComboBox::down-arrow:focus,
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

if hasattr(QtGui, "qt_mac_set_native_menubar"):
    StyleSheet += """
        #album-edition-page QComboBox, #track-edition-page QComboBox {
            padding-left: 1px;
            padding-top: 1px;
            margin-left: 3px;
            margin-right: 2px;
        }

        #album-edition-page QPushButton#lookup-isni {
            margin-right: 5px;
        }
    """


@Observer
class MainWindow(QMainWindow):
    _closing = False
    _album = None
    _on_add_files = lambda *_: None
    _on_close_album = lambda *_: None
    _on_save_album = lambda: None
    _on_export = lambda: None

    TRACK_ACTIONS_START_INDEX = 3

    def __init__(self, portfolio, confirm_exit, show_save_error, create_startup_screen, create_album_screen,
                 confirm_close, select_export_destination, select_tracks, select_tracks_in_folder, **handlers):
        super().__init__()
        self._confirm_exit = confirm_exit
        self._show_save_error = show_save_error
        self._create_startup_screen = create_startup_screen
        self._create_album_screen = create_album_screen
        self._confirm_close = confirm_close
        self._select_tracks_in_folder = select_tracks_in_folder
        self._select_tracks = select_tracks
        self._select_export_destination = select_export_destination

        self._setup_ui()
        self._setup_menu_bar()
        self._setup_signals(portfolio)

        for name, handler in handlers.items():
            getattr(self, name)(handler)

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

    def _close_current_screen(self):
        if self.centralWidget() is not None:
            widget = self.takeCentralWidget()
            widget.close()

    def _show_screen(self, screen):
        self.setCentralWidget(screen)

    def _change_screen(self, screen):
        self._close_current_screen()
        self._show_screen(screen)

    def display_album_screen(self, album):
        self._album = album
        self.enable_album_actions(album)
        self._create_track_actions()
        self._change_screen(self._create_album_screen(album))

        self.subscribe(album.track_inserted, self._rebuild_track_actions)
        self.subscribe(album.track_removed, self._rebuild_track_actions)

    def on_close_album(self, on_close_album):
        self._on_close_album = on_close_album

    def on_save_album(self, on_save_album):
        self._on_save_album = on_save_album

    def on_export(self, on_export):
        self._on_export = on_export

    def on_settings(self, on_settings):
        self.settings_action.triggered.connect(on_settings)

    def on_add_files(self, handler):
        self._on_add_files = handler

    def _setup_ui(self):
        ui_file.load(":/ui/main_window.ui", self)
        self.setStyleSheet(StyleSheet)

    def _setup_menu_bar(self):
        self.add_files_action.triggered.connect(self._add_files)
        self.add_folder_action.triggered.connect(self._add_folder)
        self.close_album_action.triggered.connect(self._confirm_album_close)
        self.save_album_action.triggered.connect(self._save_album)
        self.export_action.triggered.connect(self._choose_export_destination)
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

    def _add_files(self, *_):
        self._select_tracks(self._album.type, self._add_files_to_album)

    def _add_folder(self, *_):
        self._select_tracks_in_folder(self._album.type, self._add_files_to_album)

    def _add_files_to_album(self, *files):
        self._on_add_files(self._album, *files)

    def _rebuild_track_actions(self, *_):
        self._clear_track_actions()
        self._create_track_actions()

    def _create_track_actions(self):
        for track in self._album.tracks:
            action = QAction("{0} - {1}".format(track.track_number, track.track_title), self)
            action.triggered.connect(lambda checked, track_number=track.track_number: self._to_track_page(track_number))
            self.navigate_menu.addAction(action)

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

    def _confirm_album_close(self):
        self._confirm_close(on_accept=lambda: self._on_close_album(self._album))

    def _choose_export_destination(self):
        self._select_export_destination(lambda dest: self._on_export(self._album, dest), self._album.release_name)

    def _save_album(self):
        if self.focusWidget() is not None:
            self.focusWidget().clearFocus()

        with rescue(on_error=self._show_save_error):
            self._on_save_album(self._album)

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

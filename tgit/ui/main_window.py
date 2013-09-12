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

from PyQt4.Qt import (QDir, QRect, QMainWindow, QStatusBar, QWidget, QGridLayout,
                      QPushButton, QMenu, QMenuBar, QAction, QLabel, QLineEdit, QFileDialog)

from tgit.mp3 import MP3File

MAIN_WINDOW_NAME = "TGiT"
ADD_FILE_BUTTON_NAME = "Add File"
ALBUM_TITLE_INPUT_NAME = "Album Title"
BITRATE_INFO_NAME = "Bitrate"
DURATION_INFO_NAME = "Duration"


class MainWindow(QMainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName(MAIN_WINDOW_NAME)
        self.resize(469, 266)
        self._make_import_file_dialog()
        self.setCentralWidget(self._make_welcome_panel())
        self._make_tag_album_panel()
        self._fill_menu()
        self._make_status_bar()
        self.localize_ui()

    def _make_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def _make_welcome_panel(self):
        self._welcome_panel = QWidget()
        welcome_panel_layout = QGridLayout(self._welcome_panel)
        self._add_file_button = QPushButton(self._welcome_panel)
        self._add_file_button.setObjectName(ADD_FILE_BUTTON_NAME)
        self._add_file_button.clicked.connect(self._add_file_dialog.show)
        welcome_panel_layout.addWidget(self._add_file_button, 0, 0, 1, 1)
        return self._welcome_panel

    def _make_tag_album_panel(self):
        self._tag_album_panel = QWidget()
        tag_album_layout = QGridLayout(self._tag_album_panel)
        self._album_title_label = QLabel(self._tag_album_panel)
        tag_album_layout.addWidget(self._album_title_label, 0, 0, 1, 1)
        self._album_title_input = QLineEdit(self._tag_album_panel)
        self._album_title_input.setObjectName(ALBUM_TITLE_INPUT_NAME)
        tag_album_layout.addWidget(self._album_title_input, 0, 1, 1, 1)
        self._bitrate_label = QLabel(self._tag_album_panel)
        tag_album_layout.addWidget(self._bitrate_label, 1, 0, 1, 1)
        self._bitrate_info = QLabel(self._tag_album_panel)
        self._bitrate_info.setObjectName(BITRATE_INFO_NAME)
        tag_album_layout.addWidget(self._bitrate_info, 1, 1, 1, 1)
        self._duration_label = QLabel(self._tag_album_panel)
        tag_album_layout.addWidget(self._duration_label, 2, 0, 1, 1)
        self._duration_info = QLabel(self._tag_album_panel)
        self._duration_info.setObjectName(DURATION_INFO_NAME)
        tag_album_layout.addWidget(self._duration_info, 2, 1, 1, 1)
        return self._tag_album_panel

    def _fill_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, 469, 21))
        self._quit_menu = QMenu(menu_bar)
        self._quit_menu_item = QAction(self)
        self._quit_menu_item.triggered.connect(self.close)
        self._quit_menu.addAction(self._quit_menu_item)
        self.setMenuBar(menu_bar)
        menu_bar.addAction(self._quit_menu.menuAction())

    def _make_import_file_dialog(self):
        self._add_file_dialog = QFileDialog(self)
        self._add_file_dialog.setDirectory(QDir.homePath())
        self._add_file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        self._add_file_dialog.setModal(True)
        self._add_file_dialog.fileSelected.connect(self._import_file)

    def _show_tag_album_panel(self):
        self.setCentralWidget(self._tag_album_panel)

    def _import_file(self, filename):
        audio = MP3File(filename)
        self._album_title_input.setText(audio.album_title)
        self._bitrate_info.setText("%d kps" % audio.bitrate_in_kbps)
        self._duration_info.setText(audio.duration_as_text)
        self._show_tag_album_panel()

    def localize_ui(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._add_file_button.setText(self.tr("Add File..."))
        self._quit_menu.setTitle(self.tr("Quit"))
        self._quit_menu_item.setText(self.tr("Hit me to quit"))
        self._album_title_label.setText(self.tr("Album Title: "))
        self._bitrate_label.setText(self.tr("Bitrate: "))
        self._duration_label.setText(self.tr("Duration: "))
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

from PyQt4.Qt import (QRect, QApplication, QMainWindow, QStatusBar, QWidget, QGridLayout,
                      QPushButton, QMenu, QMenuBar, QAction, QLabel, QFileDialog)

MAIN_WINDOW_CONTEXT = "MainWindow"
MAIN_WINDOW_NAME = "TGiT"
OPEN_FILE_BUTTON_NAME = "OpenFile"
TITLE_LABEL_NAME = "Title"


class MainWindow(QMainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self._setup_ui()

    def _setup_ui(self):
        self.setObjectName(MAIN_WINDOW_NAME)
        self.resize(469, 266)
        self.setCentralWidget(self._make_main_panel())
        self._fill_menu()
        self._make_status_bar()
        self.localize_ui()

    def _make_status_bar(self):
        self.setStatusBar(QStatusBar(self))

    def _make_main_panel(self):
        main_panel = QWidget(self)
        main_panel_layout = QGridLayout(main_panel)
        self._button = QPushButton(main_panel)
        self._button.setObjectName(OPEN_FILE_BUTTON_NAME)
        self._button.clicked.connect(self.open_import_file_dialog)
        main_panel_layout.addWidget(self._button, 0, 0, 1, 1)
        self._label = QLabel(main_panel)
        self._label.setObjectName(TITLE_LABEL_NAME)
        self._label.setText("Song title")
        main_panel_layout.addWidget(self._label, 1, 0, 1, 1)
        return main_panel

    def _fill_menu(self):
        menu_bar = QMenuBar(self)
        menu_bar.setGeometry(QRect(0, 0, 469, 21))
        self._quit_menu = QMenu(menu_bar)
        self._quit_menu_item = QAction(self)
        self._quit_menu_item.triggered.connect(self.close)
        self._quit_menu.addAction(self._quit_menu_item)
        self.setMenuBar(menu_bar)
        menu_bar.addAction(self._quit_menu.menuAction())

    def open_import_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setModal(True)
        dialog.show()

    def localize_ui(self):
        self.setWindowTitle(QApplication.translate(MAIN_WINDOW_CONTEXT, "Main Window", None,
                                                   QApplication.UnicodeUTF8))
        self._button.setText(QApplication.translate(MAIN_WINDOW_CONTEXT, "Hit me ...", None,
                                                   QApplication.UnicodeUTF8))
        self._quit_menu.setTitle(QApplication.translate(MAIN_WINDOW_CONTEXT, "Quit", None,
                                                       QApplication.UnicodeUTF8))
        self._quit_menu_item.setText(QApplication.translate(MAIN_WINDOW_CONTEXT, "Hit me to quit",
                                                           None, QApplication.UnicodeUTF8))

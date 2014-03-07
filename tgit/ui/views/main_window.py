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

from PyQt4.QtGui import QMainWindow

from tgit.ui import style


class MainWindow(object):
    NAME = 'main-window'
    SIZE = (1100, 750)

    def render(self):
        self._mainWindow = self._build()
        self.translate()
        return self._mainWindow

    def show(self, view):
        self._mainWindow.setCentralWidget(view)

    def setMenuBar(self, menuBar):
        self._mainWindow.setMenuBar(menuBar)

    def _build(self):
        mainWindow = QMainWindow()
        mainWindow.setObjectName(self.NAME)
        mainWindow.setStyleSheet(style.Sheet)
        mainWindow.resize(*self.SIZE)
        return mainWindow

    def translate(self):
        self._mainWindow.setWindowTitle(self._mainWindow.tr('TGiT'))
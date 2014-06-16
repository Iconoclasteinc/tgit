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


class MainWindow(QMainWindow):
    SIZE = (1100, 744)

    def __init__(self, menuBar, welcomeScreen, albumScreen):
        QMainWindow.__init__(self)
        self.build()
        self.setMenuBar(menuBar)
        self.setCentralWidget(welcomeScreen)
        self.createAlbum = albumScreen

    def build(self):
        self.setObjectName('main-window')
        self.setStyleSheet(style.Sheet)
        self.setWindowTitle(self.tr('TGiT'))
        self.resize(*self.SIZE)

    def albumCreated(self, album):
        self.setCentralWidget(self.createAlbum(album))

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

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from tgit import album_director as director
from tgit.album import Album
from tgit.ui.helpers import ui_file


def welcome_screen(dialogs, album_portfolio):
    page = WelcomeScreen()
    page.create_new_album.connect(lambda album_type: director.create_album(album_portfolio, album_type))
    page.import_album.connect(lambda: dialogs.import_album(album_portfolio).open())
    return page


# We have to inherit from QFrame and not QWidget if we want a background without reimplementing QWidget.paintEvent
class WelcomeScreen(QtWidgets.QFrame):
    create_new_album = pyqtSignal(str)
    import_album = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        ui_file.load(":/ui/welcome_screen.ui", self)

        self.import_album_button.clicked.connect(lambda: self.import_album.emit())
        self.new_mp3_album_button.clicked.connect(lambda: self.create_new_album.emit(Album.Type.MP3))
        self.new_flac_album_button.clicked.connect(lambda: self.create_new_album.emit(Album.Type.FLAC))

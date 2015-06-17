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

from PyQt5.QtWidgets import QFrame

from tgit.album import Album
from tgit.ui.helpers import ui_file

def welcome_page(select_album, **handlers):
    screen = WelcomePage(select_album=select_album)
    for name, handler in handlers.items():
        getattr(screen, name)(handler)

    return screen


class WelcomePage(QFrame):
    def __init__(self, *, select_album, parent=None):
        super().__init__(parent)
        self._select_album = select_album
        ui_file.load(":/ui/welcome_page.ui", self)

    def on_create_album(self, on_create_album):
        self.new_mp3_album_button.clicked.connect(lambda: on_create_album(Album.Type.MP3))
        self.new_flac_album_button.clicked.connect(lambda: on_create_album(Album.Type.FLAC))

    def on_load_album(self, on_load_album):
        self.load_album_button.clicked.connect(lambda: self._select_album(on_load_album))

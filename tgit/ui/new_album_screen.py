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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame

from tgit.album import Album
from tgit.ui.helpers import ui_file


def make_new_album_screen(of_type, on_create_album, on_select_album_location, on_select_track_location):
    page = NewAlbumScreen(of_type)
    page.create_album.connect(on_create_album)
    page.select_album_location.connect(lambda: on_select_album_location(page.change_album_location))
    page.select_track_location.connect(lambda: on_select_track_location(page.change_track_location))
    return page


class AlbumCreationProperties:
    def __init__(self, type_, album_location, track_location=None):
        self.album_location = album_location
        self.track_location = track_location
        self.type = type_


class NewAlbumScreen(QFrame):
    select_album_location = pyqtSignal()
    select_track_location = pyqtSignal()
    create_album = pyqtSignal(AlbumCreationProperties)

    def __init__(self, of_type=Album.Type.FLAC):
        super().__init__()
        self.of_type = of_type

        ui_file.load(":/ui/new_album_screen.ui", self)

        self.continue_button.clicked.connect(self.on_create_album)
        self.browse_album_location_button.clicked.connect(self.select_album_location.emit)
        self.browse_track_location_button.clicked.connect(self.select_track_location.emit)

    def on_create_album(self):
        self.create_album.emit(
            AlbumCreationProperties(self.of_type, self.album_location.text(), self.track_location.text()))

    def change_album_location(self, destination):
        self.album_location.setText(destination)

    def change_track_location(self, destination):
        self.track_location.setText(destination)

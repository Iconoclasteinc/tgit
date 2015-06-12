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


def make_new_album_screen(of_type, on_create_album, on_select_album_location, on_select_track_location):
    page = NewAlbumScreen(of_type=of_type)
    page.on_create_album(on_create_album)
    page.on_select_album_location(lambda: on_select_album_location(page.change_album_location))
    page.on_select_track_location(lambda: on_select_track_location(page.change_track_location))
    return page


class AlbumCreationProperties:
    def __init__(self, type_, album_name, album_location, track_location=None):
        self.album_name = album_name
        self.album_location = album_location
        self.track_location = track_location
        self.type = type_

    @property
    def album_full_path(self):
        return "{0}/{1}.tgit".format(self.album_location, self.album_name)


class NewAlbumScreen(QFrame):
    def __init__(self, parent=None, of_type=Album.Type.FLAC):
        super().__init__(parent)
        self.of_type = of_type

        ui_file.load(":/ui/new_album_screen.ui", self)

        self.album_location.textChanged.connect(self._toggle_create_button)
        self.album_name.textChanged.connect(self._toggle_create_button)

    def on_create_album(self, on_create_album):
        self.continue_button.clicked.connect(lambda: on_create_album(
            AlbumCreationProperties(self.of_type, self.album_name.text(), self.album_location.text(),
                                    self.track_location.text())))

    def on_select_album_location(self, on_select_album_location):
        self.browse_album_location_button.clicked.connect(on_select_album_location)

    def on_select_track_location(self, on_select_track_location):
        self.browse_track_location_button.clicked.connect(on_select_track_location)

    def change_album_location(self, destination):
        self.album_location.setText(destination)

    def change_track_location(self, destination):
        self.track_location.setText(destination)

    def _toggle_create_button(self, text):
        self.continue_button.setDisabled(self._should_disable_continue_button())

    def _should_disable_continue_button(self):
        return self.album_location.text() == "" and self.album_name.text() == ""

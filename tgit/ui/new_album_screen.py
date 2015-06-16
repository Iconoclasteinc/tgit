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


def make_new_album_screen(of_type, on_create_album, on_import_album, on_select_album_location, on_select_track_location):
    page = NewAlbumScreen(of_type=of_type)
    page.on_create_album(on_create_album)
    page.on_import_album(on_import_album)
    page.on_select_album_location(lambda: on_select_album_location(page.change_album_location))
    page.on_select_track_location(lambda: on_select_track_location(page.change_track_location))
    return page


class NewAlbumScreen(QFrame):
    def __init__(self, parent=None, of_type=Album.Type.FLAC):
        super().__init__(parent)
        self._of_type = of_type
        self._on_create_album = lambda properties: None
        self._on_import_album = lambda properties: None

        ui_file.load(":/ui/new_album_screen.ui", self)

        self.album_location.textChanged.connect(lambda text: self._toggle_create_button())
        self.album_name.textChanged.connect(lambda text: self._toggle_create_button())
        self.continue_button.clicked.connect(self._create_album)

    def on_create_album(self, on_create_album):
        self._on_create_album = on_create_album

    def on_import_album(self, on_import_album):
        self._on_import_album = on_import_album

    def on_select_album_location(self, on_select_album_location):
        self.browse_album_location_button.clicked.connect(on_select_album_location)

    def on_select_track_location(self, on_select_track_location):
        self.browse_track_location_button.clicked.connect(on_select_track_location)

    def change_album_location(self, destination):
        self.album_location.setText(destination)

    def change_track_location(self, destination):
        self.track_location.setText(destination)

    def _toggle_create_button(self):
        self.continue_button.setDisabled(self._should_disable_continue_button())

    def _should_disable_continue_button(self):
        return self.album_location.text() == "" or self.album_name.text() == ""

    def _create_album(self):
        properties = dict(type=self._of_type, album_name=self.album_name.text(),
                          album_location=self.album_location.text())

        track_location = self.track_location.text()
        if not track_location:
            self._on_create_album(properties)
        else:
            properties["track_location"] = track_location
            self._on_import_album(properties)

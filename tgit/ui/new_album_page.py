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

from tgit.ui.helpers import ui_file


def new_album_page(select_album_location, select_track_location, **handlers):
    page = NewAlbumPage(select_album_destination=select_album_location, select_track_location=select_track_location)
    for name, handler in handlers.items():
        getattr(page, name)(handler)

    return page


class NewAlbumPage(QFrame):
    def __init__(self, *, parent=None, select_album_destination, select_track_location):
        super().__init__(parent)
        self._of_type = None
        self._on_create_album = lambda properties: None
        self._on_import_album = lambda properties: None

        ui_file.load(":/ui/new_album_page.ui", self)

        self.album_location.textChanged.connect(lambda text: self._toggle_create_button())
        self.album_name.textChanged.connect(lambda text: self._toggle_create_button())
        self.browse_album_location_button.clicked.connect(lambda: select_album_destination(self.album_location.setText))
        self.browse_track_location_button.clicked.connect(lambda: select_track_location(self.track_location.setText))
        self.continue_button.clicked.connect(self._create_album)

    def on_create_album(self, on_create_album):
        self._on_create_album = on_create_album

    def on_import_album(self, on_import_album):
        self._on_import_album = on_import_album

    def set_type(self, type_):
        self._of_type = type_

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

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
import os

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QFrame, QLineEdit

from tgit.album import Album
from tgit.ui.helpers import ui_file


def new_album_page(select_album_location, select_track_location, **handlers):
    page = NewAlbumPage(select_album_destination=select_album_location, select_track_location=select_track_location)
    for name, handler in handlers.items():
        getattr(page, name)(handler)

    return page


class NewAlbumPage(QFrame):
    _on_create_album = lambda *_: None
    _on_import_album = lambda *_: None

    def __init__(self, *, parent=None, select_album_destination, select_track_location):
        super().__init__(parent)

        ui_file.load(":/ui/new_album_page.ui", self)
        self.addAction(self.cancel_creation_action)
        self.addAction(self.create_album_action)
        self.album_location.textChanged.connect(lambda: self._toggle_create_button())
        self.album_name.textChanged.connect(lambda: self._toggle_create_button())
        self.browse_album_location_button.clicked.connect(lambda: select_album_destination(self.album_location.setText))
        self.browse_track_location_button.clicked.connect(lambda: select_track_location(self.track_location.setText))
        self.create_album_action.triggered.connect(self._create_album)
        self.cancel_creation_action.triggered.connect(self._clear_form)
        self._disable_mac_focus_frame()

    def on_create_album(self, on_create_album):
        self._on_create_album = on_create_album

    def on_import_album(self, on_import_album):
        self._on_import_album = on_import_album

    def on_cancel_creation(self, on_cancel_creation):
        self.cancel_creation_action.triggered.connect(on_cancel_creation)

    def _toggle_create_button(self):
        disable_continue_button = self._should_disable_continue_button()
        self.create_button.setDisabled(disable_continue_button)
        self.create_album_action.setDisabled(disable_continue_button)

    def _should_disable_continue_button(self):
        return self.album_location.text() == "" or self.album_name.text() == ""

    def _album_filename(self):
        return os.path.join(self.album_location.text(), self.album_name.text(), self.album_name.text() + ".tgit")

    def _album_type(self):
        return Album.Type.FLAC if self._flac_button.isChecked() else Album.Type.MP3

    def _create_album(self):
        if not self.track_location.text():
            self._on_create_album(self._album_type(), self._album_filename())
        else:
            self._on_import_album(self._album_type(), self._album_filename(), self.track_location.text())

    def _clear_form(self):
        self._flac_button.setChecked(True)
        self.album_name.setText("")
        self.album_location.setText("")
        self.track_location.setText("")

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QLineEdit):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

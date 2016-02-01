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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLineEdit

from tgit.album import Album
from tgit.ui import locations
from tgit.ui.helpers.ui_file import UIFile


def make_new_album_page(select_album_location, select_track, check_album_exists, confirm_overwrite, **handlers):
    page = NewAlbumPage(select_album_location=select_album_location,
                        select_track=select_track,
                        check_album_exists=check_album_exists,
                        confirm_overwrite=confirm_overwrite)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

    return page


class NewAlbumPage(QFrame, UIFile):
    def __init__(self, select_album_location, select_track, check_album_exists, confirm_overwrite):
        super().__init__()
        self._confirm_overwrite = confirm_overwrite
        self._album_exists = check_album_exists
        self._setup_ui(select_album_location, select_track)

    def _setup_ui(self, select_album_destination, select_track_location):
        self._load(":/ui/new_album_page.ui")
        self.addAction(self._cancel_creation_action)
        self.addAction(self._create_album_action)
        self._album_location.textChanged.connect(self._toggle_create_button)
        self._album_name.textChanged.connect(self._toggle_create_button)
        self._browse_album_location_button.clicked.connect(
            lambda: select_album_destination(self._album_location.setText))
        self._browse_track_location_button.clicked.connect(
            lambda: select_track_location(self._album_type(), self._track_location.setText))
        self._disable_mac_focus_frame()

    def on_create_album(self, on_create_album):
        def create_album():
            on_create_album(self._album_type(), self._album_name.text(), self._album_location.text(),
                            self._track_location.text())

        def check_album_exists():
            if self._album_exists(self._album_name.text(), self._album_location.text()):
                self._confirm_overwrite(on_accept=create_album)
            else:
                create_album()

        self._create_album_action.triggered.connect(check_album_exists)

    def on_cancel_creation(self, on_cancel_creation):
        self._cancel_creation_action.triggered.connect(on_cancel_creation)

    def _toggle_create_button(self):
        self._create_button.setEnabled(self._can_create())
        self._create_album_action.setEnabled(self._can_create())

    def _can_create(self):
        return self._album_location.text() != "" and self._album_name.text() != ""

    def _album_type(self):
        return Album.Type.FLAC if self._flac_button.isChecked() else Album.Type.MP3

    def showEvent(self, event):
        self._mp3_button.setChecked(True)
        self._album_name.setText(self.tr("untitled"))
        self._album_name.setFocus()
        self._album_name.selectAll()
        self._album_location.setText(locations.Documents)
        self._track_location.setText("")

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QLineEdit):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

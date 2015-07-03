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
from tgit.ui import locations
from tgit.ui.helpers.ui_file import UIFile


class NewAlbumPage(QFrame, UIFile):
    _on_create_album = lambda *_: None
    _on_import_album = lambda *_: None

    def __init__(self, select_album_location, select_track, check_album_exists, confirm_overwrite, **handlers):
        super().__init__()
        self._album_exists = check_album_exists
        self._setup_ui(select_album_location, select_track, confirm_overwrite)
        self._register_event_handlers(handlers)

    def _register_event_handlers(self, handlers):
        for name, handler in handlers.items():
            getattr(self, name)(handler)

    def _setup_ui(self, select_album_destination, select_track_location, confirm_overwrite):
        self._load(":/ui/new_album_page.ui")
        self.addAction(self.cancel_creation_action)
        self.addAction(self.create_album_action)
        self.album_location.textChanged.connect(lambda: self._toggle_create_button())
        self.album_name.textChanged.connect(lambda: self._toggle_create_button())
        self.browse_album_location_button.clicked.connect(lambda: select_album_destination(self.album_location.setText))
        self.browse_track_location_button.clicked.connect(lambda: select_track_location(self.track_location.setText))
        self.create_album_action.triggered.connect(lambda: self._create_album(confirm_overwrite))
        self._disable_mac_focus_frame()

    def on_create_album(self, on_create_album):
        self._on_create_album = on_create_album

    def on_import_album(self, on_import_album):
        self._on_import_album = on_import_album

    def on_cancel_creation(self, on_cancel_creation):
        self.cancel_creation_action.triggered.connect(on_cancel_creation)

    def _toggle_create_button(self):
        self.create_button.setEnabled(self._can_continue())
        self.create_album_action.setEnabled(self._can_continue())

    def _can_continue(self):
        return self.album_location.text() != "" and self.album_name.text() != ""

    def _album_type(self):
        return Album.Type.FLAC if self._flac_button.isChecked() else Album.Type.MP3

    def _album_filename(self):
        return os.path.join(self.album_location.text(), self.album_name.text(), self.album_name.text() + ".tgit")

    def _create_album(self, confirm_overwrite):
        def create_or_import_album():
            if not self.track_location.text():
                self._on_create_album(self._album_type(), self._album_filename())
            else:
                self._on_import_album(self._album_type(), self._album_filename(), self.track_location.text())

        if self._album_exists(self._album_filename()):
            confirm_overwrite(on_accept=create_or_import_album)
        else:
            create_or_import_album()

    def showEvent(self, event):
        self._flac_button.setChecked(True)
        self.album_name.setText(self.tr("untitled"))
        self.album_name.setFocus()
        self.album_name.selectAll()
        self.album_location.setText(locations.Documents)
        self.track_location.setText("")

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QLineEdit):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

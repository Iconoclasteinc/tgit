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
from tgit.ui import locations
from tgit.ui.helpers.ui_file import UIFile


def make_new_project_page(select_location, select_track, check_project_exists, confirm_overwrite, **handlers):
    page = NewProjectPage(select_location=select_location,
                          select_track=select_track,
                          check_project_exists=check_project_exists,
                          confirm_overwrite=confirm_overwrite)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

    return page


class NewProjectPage(QFrame, UIFile):
    def __init__(self, select_location, select_track, check_project_exists, confirm_overwrite):
        super().__init__()
        self._confirm_overwrite = confirm_overwrite
        self._project_exists = check_project_exists
        self._setup_ui(select_location, select_track)

    def _setup_ui(self, select_destination, select_track_location):
        self._load(":/ui/new_album_page.ui")
        self.addAction(self._cancel_creation_action)
        self.addAction(self._create_project_action)
        self._location.textChanged.connect(self._toggle_create_button)
        self._name.textChanged.connect(self._toggle_create_button)
        self._browse_location_button.clicked.connect(
            lambda: select_destination(self._location.setText))
        self._browse_track_location_button.clicked.connect(
            lambda: select_track_location(self._type(), self._track_location.setText))

    def on_create_project(self, on_create_project):
        def create_project():
            on_create_project(self._type(), self._name.text(), self._location.text(),
                              self._track_location.text())

        def check_project_exists():
            if self._project_exists(self._name.text(), self._location.text()):
                self._confirm_overwrite(on_accept=create_project)
            else:
                create_project()

        self._create_project_action.triggered.connect(check_project_exists)

    def on_cancel_creation(self, on_cancel_creation):
        self._cancel_creation_action.triggered.connect(on_cancel_creation)

    def _toggle_create_button(self):
        self._create_button.setEnabled(self._can_create())
        self._create_project_action.setEnabled(self._can_create())

    def _can_create(self):
        return self._location.text() != "" and self._name.text() != ""

    def _type(self):
        return Album.Type.FLAC if self._flac_button.isChecked() else Album.Type.MP3

    def showEvent(self, event):
        self._mp3_button.setChecked(True)
        self._name.setText(self.tr("untitled"))
        self._name.setFocus()
        self._name.selectAll()
        self._location.setText(locations.Documents)
        self._track_location.setText("")

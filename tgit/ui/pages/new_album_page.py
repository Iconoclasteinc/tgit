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
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFrame, QDialogButtonBox

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
    _project_type = Album.Type.FLAC

    def __init__(self, select_location, select_track, check_project_exists, confirm_overwrite):
        super().__init__()
        self._confirm_overwrite = confirm_overwrite
        self._project_exists = check_project_exists
        self._setup_ui(select_location, select_track)

    def _setup_ui(self, select_destination, select_track_location):
        self._load(":/ui/new_album_page.ui")
        self._create_button().setText(self.tr("Create"))
        self._create_button().setShortcut(QKeySequence(Qt.Key_Return))
        self._cancel_button().setShortcut(QKeySequence(Qt.Key_Escape))
        self._location.textChanged.connect(self._toggle_create_button)
        self._name.textChanged.connect(self._toggle_create_button)
        self._browse_location_button.clicked.connect(lambda: select_destination(self._location.setText))
        self._select_reference_track_button.clicked.connect(
                lambda: select_track_location(self.project_type, self._reference_track.setText))

    def _create_button(self):
        return self._action_buttons.button(QDialogButtonBox.Ok)

    def _cancel_button(self):
        return self._action_buttons.button(QDialogButtonBox.Cancel)

    def on_create_project(self, on_create_project):
        def create_project():
            on_create_project(self.project_type, self._name.text(), self._location.text(), self._reference_track.text())

        def confirm_project_creation():
            if self._project_exists(self._name.text(), self._location.text()):
                self._confirm_overwrite(on_accept=create_project)
            else:
                create_project()

        self._action_buttons.accepted.connect(confirm_project_creation)

    def on_cancel_creation(self, on_cancel_creation):
        self._action_buttons.rejected.connect(on_cancel_creation)

    def _toggle_create_button(self):
        self._create_button().setEnabled(self._can_create())

    def _can_create(self):
        return self._location.text() != "" and self._name.text() != ""

    @property
    def project_type(self):
        return self._project_type

    @project_type.setter
    def project_type(self, project_type):
        self._project_type = project_type
        self._title.setText(self.tr("New {} Project".format(project_type.upper())))

    def showEvent(self, event):
        self._name.setText(self.tr("untitled"))
        self._name.setFocus()
        self._name.selectAll()
        self._location.setText(locations.Documents)
        self._reference_track.setText("")
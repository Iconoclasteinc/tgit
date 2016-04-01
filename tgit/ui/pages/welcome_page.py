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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QListWidgetItem

import tgit
from tgit.album import Album
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.rescue import rescue


def make_welcome_page(project_history, select_project, show_load_error, **handlers):
    page = WelcomePage(select_project=select_project, show_load_error=show_load_error)
    page.display_project_history(project_history)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

    subscription = project_history.history_changed.subscribe(lambda: page.display_project_history(project_history))
    page.closed.connect(subscription.cancel)
    return page


@Closeable
class WelcomePage(QFrame, UIFile):
    closed = pyqtSignal()
    on_open_project = pyqtSignal(str)

    def __init__(self, select_project, show_load_error):
        super().__init__()
        self._select_project = select_project
        self._show_load_error = show_load_error
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/welcome_page.ui")
        self._version.setText(tgit.__version__)
        self._recent_projects_list.currentItemChanged.connect(
            lambda item: self._open_project_button.setEnabled(item is not None))

    @property
    def _selected_project(self):
        return self._recent_projects_list.currentItem().text()

    def on_create_project(self, on_create_project):
        self._new_mp3_project_button.clicked.connect(lambda _: on_create_project(Album.Type.MP3))
        self._new_flac_project_button.clicked.connect(lambda _: on_create_project(Album.Type.FLAC))

    def on_load_project(self, on_load_project):
        def try_loading_project(filename):
            with rescue(on_error=self._show_load_error):
                on_load_project(filename)

        self._load_project_button.clicked.connect(lambda: self._select_project(try_loading_project))
        self._open_project_button.clicked.connect(lambda checked: try_loading_project(self._selected_project))

    def display_project_history(self, project_history):
        self._clear_project_history()
        self._populate_project_history(project_history)

    def _clear_project_history(self):
        for index in reversed(range(self._recent_projects_list.count())):
            self._recent_projects_list.takeItem(index)

    def _populate_project_history(self, project_history):
        for recent_project in project_history:
            item = QListWidgetItem(os.path.normpath(recent_project.filename))
            self._recent_projects_list.addItem(item)

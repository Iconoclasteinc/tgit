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

from PyQt5.QtWidgets import QStackedWidget


class StartupScreen(QStackedWidget):
    def __init__(self, create_welcome_page, create_new_project_page):
        super().__init__()
        self._welcome_page = create_welcome_page()
        self._new_project_page = create_new_project_page()

        self._welcome_page.on_create_project(self._move_to_new_project_page)
        self._new_project_page.on_cancel_creation(self._move_to_welcome_page)

        self.addWidget(self._welcome_page)
        self.addWidget(self._new_project_page)

    def _move_to_new_project_page(self, project_type):
        self._new_project_page.project_type = project_type
        self.setCurrentWidget(self._new_project_page)

    def _move_to_welcome_page(self):
        self.setCurrentWidget(self._welcome_page)

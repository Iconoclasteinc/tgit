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

from ._screen_driver import ScreenDriver
from .new_project_page_driver import new_project_page
from .welcome_page_driver import welcome_page


class StartupScreenDriver(ScreenDriver):
    def shows_welcome_page(self):
        welcome_page(self).is_showing_on_screen()

    def create_project(self):
        welcome_page(self).new_project(of_type="mp3")
        new_project_page(self).is_showing_on_screen()
        new_project_page(self).has_reset_form()

    def cancel_creation(self):
        self.create_project()
        new_project_page(self).cancel_creation()
        welcome_page(self).is_showing_on_screen()

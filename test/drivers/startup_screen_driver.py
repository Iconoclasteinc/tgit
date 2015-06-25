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
from test.drivers import welcome_page
from test.drivers.new_album_page_driver import new_album_page


class StartupScreenDriver(ScreenDriver):
    def shows_welcome_page(self):
        welcome_page(self).is_showing_on_screen()

    def create_album(self):
        welcome_page(self).new_album()
        new_album_page(self).is_showing_on_screen()
        new_album_page(self).has_reset_form()

    def cancel_creation(self):
        self.create_album()
        new_album_page(self).cancel_creation()
        welcome_page(self).is_showing_on_screen()

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
from test.drivers.new_album_screen_driver import new_album_page
from tgit.album import Album


class StartupScreenDriver(ScreenDriver):
    def shows_welcome_page(self):
        welcome_page(self).is_showing_on_screen()

    def creates_album(self, of_type):
        welcome_page(self).new_album(of_type)
        new_album_page(self).is_showing_on_screen()

    def cancels_creation(self):
        welcome_page(self).new_album(of_type=Album.Type.MP3)
        new_album_page(self).cancel_creation()
        welcome_page(self).is_showing_on_screen()

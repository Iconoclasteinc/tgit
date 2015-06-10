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

from cute.matchers import named
from ._screen_driver import ScreenDriver
from tgit.ui.new_album_screen import NewAlbumScreen


def new_album_screen(parent):
    return NewAlbumScreenDriver.find_single(parent, NewAlbumScreen, named("new_album_screen"))


class NewAlbumScreenDriver(ScreenDriver):
    def create_empty_album(self, location):
        self.lineEdit(named("album_file_location")).change_text(location)
        self.button(named("continue_button")).click()

    def select_album(self):
        self.button(named("browse_album_file_location_button")).click()

    def has_album_location(self, destination):
        self.lineEdit(named("album_file_location")).has_text(destination)

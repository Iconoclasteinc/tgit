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
from tgit.ui.new_album_page import NewAlbumPage


def new_album_page(parent):
    return NewAlbumPageDriver.find_single(parent, NewAlbumPage, named("new_album_page"))


class NewAlbumPageDriver(ScreenDriver):
    def create_empty_album(self, album_name, album_path):
        self.lineEdit(named("album_name")).change_text(album_name)
        self.lineEdit(named("album_location")).change_text(album_path)
        self.button(named("create_button")).click()

    def import_album(self, album_name, album_path, track_path):
        self.lineEdit(named("album_name")).change_text(album_name)
        self.lineEdit(named("album_location")).change_text(album_path)
        self.lineEdit(named("track_location")).change_text(track_path)
        self.button(named("create_button")).click()

    def cancel_creation(self):
        self.button(named("cancel_button")).click()

    def select_album(self):
        self.button(named("browse_album_location_button")).click()

    def select_track(self):
        self.button(named("browse_track_location_button")).click()

    def has_album_location(self, destination):
        self.lineEdit(named("album_location")).has_text(destination)

    def has_track_location(self, destination):
        self.lineEdit(named("track_location")).has_text(destination)

    def creation_is_disabled(self):
        self.button(named("create_button")).is_disabled()

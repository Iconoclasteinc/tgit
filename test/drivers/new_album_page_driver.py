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

from hamcrest import ends_with

from cute import gestures
from cute.matchers import named
from tgit.ui.pages.new_album_page import NewAlbumPage
from ._screen_driver import ScreenDriver


def new_album_page(parent):
    return NewAlbumPageDriver.find_single(parent, NewAlbumPage, named("new_album_page"))


class NewAlbumPageDriver(ScreenDriver):
    def create_album(self, of_type, album_name, album_location, import_from="", using_shortcut=False):
        self.select_album_type(of_type)
        self.enter_album_name(album_name)
        self.enter_album_location(album_location)
        self.enter_track_location(import_from)

        if using_shortcut:
            self.perform(gestures.enter())
        else:
            self.button(named("create_button")).click()

    def select_album_type(self, of_type):
        self.radio(named("_{}_button".format(of_type))).click()

    def enter_album_name(self, album_name):
        self.lineEdit(named("album_name")).replace_all_text(album_name)

    def enter_album_location(self, album_location):
        self.lineEdit(named("album_location")).replace_all_text(album_location)

    def enter_track_location(self, import_from):
        self.lineEdit(named("track_location")).replace_all_text(import_from)

    def cancel_creation(self, of_type="flac", album_name="", album_location="", import_from="", using_shortcut=False):
        self.select_album_type(of_type)
        self.enter_album_name(album_name)
        self.enter_album_location(album_location)
        self.enter_track_location(import_from)

        if using_shortcut:
            self.perform(gestures.unselect())
        else:
            self.button(named("cancel_button")).click()

    def select_album(self):
        self.button(named("browse_album_location_button")).click()

    def select_track(self):
        self.button(named("browse_track_location_button")).click()

    def has_selected_flac(self):
        self.radio(named("_flac_button")).is_checked()

    def has_album_name(self, name):
        self.lineEdit(named("album_name")).has_text(name)

    def has_album_location(self, destination):
        self.lineEdit(named("album_location")).has_text(destination)

    def has_track_location(self, destination):
        self.lineEdit(named("track_location")).has_text(destination)

    def creation_is_disabled(self):
        self.button(named("create_button")).is_disabled()

    def has_reset_form(self):
        self.has_selected_flac()
        self.has_album_name("untitled")
        self.has_album_location(ends_with("Documents"))
        self.has_track_location("")

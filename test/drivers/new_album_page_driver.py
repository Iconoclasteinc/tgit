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
from tgit.ui.pages.new_album_page import NewProjectPage
from ._screen_driver import ScreenDriver


def new_project_page(parent):
    return NewProjectPageDriver.find_single(parent, NewProjectPage, named("new_project_page"))


class NewProjectPageDriver(ScreenDriver):
    def create_project(self, of_type, name, location, import_from="", using_shortcut=False):
        self.select_project_type(of_type)
        self.enter_name(name)
        self.enter_location(location)
        self.enter_track_location(import_from)

        if using_shortcut:
            self.perform(gestures.enter())
        else:
            self.button(named("_create_button")).click()

    def select_project_type(self, of_type):
        self.radio(named("_{}_button".format(of_type))).click()

    def enter_name(self, album_name):
        self.lineEdit(named("_name")).replace_all_text(album_name)

    def enter_location(self, album_location):
        self.lineEdit(named("_location")).replace_all_text(album_location)

    def enter_track_location(self, import_from):
        self.lineEdit(named("_track_location")).replace_all_text(import_from)

    def cancel_creation(self, of_type="flac", name="", location="", import_from="", using_shortcut=False):
        self.select_project_type(of_type)
        self.enter_name(name)
        self.enter_location(location)
        self.enter_track_location(import_from)

        if using_shortcut:
            self.perform(gestures.unselect())
        else:
            self.button(named("_cancel_button")).click()

    def select_project(self):
        self.button(named("_browse_location_button")).click()

    def select_track(self):
        self.button(named("_browse_track_location_button")).click()

    def has_selected_mp3(self):
        self.radio(named("_mp3_button")).is_checked()

    def has_name(self, name):
        self.lineEdit(named("_name")).has_text(name)

    def has_location(self, destination):
        self.lineEdit(named("_location")).has_text(destination)

    def has_track_location(self, destination):
        self.lineEdit(named("_track_location")).has_text(destination)

    def creation_is_disabled(self):
        self.button(named("_create_button")).is_disabled()

    def has_reset_form(self):
        self.has_selected_mp3()
        self.has_name("untitled")
        self.has_location(ends_with("Documents"))
        self.has_track_location("")

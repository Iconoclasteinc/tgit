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
from hamcrest import starts_with

from cute.matchers import named, with_text
from cute.widgets import window, QDialogDriver
from ._screen_driver import ScreenDriver
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog


def isni_lookup_dialog(parent):
    return IsniLookupDialogDriver(window(ISNILookupDialog, named("isni_lookup_dialog")), parent.prober,
                                  parent.gesture_performer)


class IsniLookupDialogDriver(QDialogDriver, ScreenDriver):
    def change_query(self, query):
        self.lineEdit(named("_lookup_criteria")).change_text(query)

    def lookup(self, query):
        self.change_query(query)
        self.button(named("_lookup_button")).click()

    def displays_result(self, index, full_name, date_of_birth, date_of_death, work):
        self.radio(named("_identity_" + str(index))).has_text(
            "{} ({}-{}) - {}".format(full_name, date_of_birth, date_of_death, work))

    def select_identity(self, name):
        self.radio(with_text(starts_with(name))).click()

    def has_ok_button_disabled(self):
        self._button_box().ok_button().is_enabled(enabled=False)

    def has_lookup_button_enabled(self, enabled=True):
        self.button(named("_lookup_button")).is_enabled(enabled=enabled)

    def select_first_identity(self):
        self.radio(named("_identity_0")).click()

    def accept(self):
        self._button_box().click_ok()

    def displays_no_result_message(self):
        self.label(named("_no_result_message")).has_text("Your query yielded no result")

    def displays_connection_error_message(self):
        self.label(named("_connection_error_message")).has_text(
            "Could not connect to the ISNI database. Please retry later.")

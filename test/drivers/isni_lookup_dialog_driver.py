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

from cute.matchers import named, with_list_item_text
from cute.widgets import window, QDialogDriver
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog
from ._screen_driver import ScreenDriver


def isni_lookup_dialog(parent):
    return IsniLookupDialogDriver(window(ISNILookupDialog, named("isni_lookup_dialog")), parent.prober,
                                  parent.gesture_performer)


class IsniLookupDialogDriver(QDialogDriver, ScreenDriver):
    def change_query(self, query):
        self.lineEdit(named("_lookup_criteria")).replace_all_text(query)

    def lookup(self, query):
        self.is_active()
        self.change_query(query)
        self.button(named("_lookup_button")).click()

    def shows_results_list(self, enabled=True):
        self.results_list.is_enabled(enabled)

    def displays_result(self, full_name, date_of_birth, date_of_death, work):
        self.results_list.is_enabled()
        self.results_list.has_item(
                with_list_item_text("{} ({}-{}) - {}".format(full_name, date_of_birth, date_of_death, work)))

    def select_identity(self, name):
        self.is_active()
        self.results_list.select_item(with_list_item_text(starts_with(name)))

    def has_ok_button_disabled(self):
        self._button_box().ok_button().is_disabled()

    def has_lookup_button_enabled(self, enabled=True):
        self.button(named("_lookup_button")).is_enabled(enabled=enabled)

    def accept(self):
        self._button_box().click_ok()

    def shows_no_result_message(self, visible=True):
        if visible:
            self.label(named("_no_result_message")).is_showing_on_screen()
        else:
            self.label(named("_no_result_message")).is_hidden()

    def shows_connection_error_message(self, visible=True):
        if visible:
            self.label(named("_connection_error_message")).is_showing_on_screen()
        else:
            self.label(named("_connection_error_message")).is_hidden()

    @property
    def results_list(self):
        return self.list_view(named("_result_container"))

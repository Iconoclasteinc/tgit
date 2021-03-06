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

from cute.matchers import named, with_item_text, StateMatcher
from cute.widgets import window, QDialogDriver, WidgetDriver
from tgit.ui.dialogs.isni_lookup_dialog import ISNILookupDialog
from tgit.ui.widgets.progress_indicator import QProgressIndicator
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
            with_item_text("{} ({}-{}) - {}".format(full_name, date_of_birth, date_of_death, work)))

    def displays_no_message(self):
        self.label(named("_result_message")).is_hidden()

    def displays_refine_query_message(self, total_count, visible=True):
        result_message = self.label(named("_result_message"))
        if visible:
            result_message.is_showing_on_screen()
            result_message.has_text("Your search yielded {} results. Please refine your search.".format(total_count))
        else:
            result_message.is_hidden()

    def select_identity(self, name):
        self.is_active()
        self.results_list.select_item(with_item_text(starts_with(name)))

    def assign(self):
        self.assignation_button.click()

    def has_ok_button_disabled(self):
        self.ok_button().is_disabled()

    def shows_assignation_button(self, enabled=True):
        self.assignation_button.is_enabled(enabled)

    def has_lookup_button_enabled(self, enabled=True):
        self.button(named("_lookup_button")).is_enabled(enabled=enabled)

    def accept(self):
        self.click_ok()

    def shows_no_result_message(self, visible=True):
        result_message = self.label(named("_result_message"))
        if visible:
            result_message.is_showing_on_screen()
            result_message.has_text("Your query yielded no result.")
        else:
            result_message.is_hidden()

    def shows_connection_error_message(self, visible=True):
        if visible:
            self.label(named("_connection_error_message")).is_showing_on_screen()
        else:
            self.label(named("_connection_error_message")).is_hidden()

    def shows_permission_denied_message(self, visible=True):
        if visible:
            self.label(named("_permission_denied_message")).is_showing_on_screen()
        else:
            self.label(named("_permission_denied_message")).is_hidden()

    def is_showing_progress_indicator(self):
        self.progress_indicator.is_(running())

    def has_stopped_progress_indicator(self):
        self.progress_indicator.is_(stopped())

    @property
    def progress_indicator(self):
        return WidgetDriver.find_single(self, QProgressIndicator, named("_progress_indicator"))

    @property
    def results_list(self):
        return self.list_view(named("_result_container"))

    @property
    def assignation_button(self):
        return self.button(named("_assignation_button"))


def running():
    return StateMatcher(QProgressIndicator.isRunning, "running", "stopped")


def stopped():
    return StateMatcher(QProgressIndicator.isStopped, "stopped", "running")

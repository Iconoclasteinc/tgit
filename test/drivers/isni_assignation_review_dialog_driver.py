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
from PyQt5.QtWidgets import QWidget

from cute.matchers import named, with_item_text, StateMatcher
from cute.widgets import window, QDialogDriver, WidgetDriver
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog
from ._screen_driver import ScreenDriver
from tgit.ui.widgets.progress_indicator import QProgressIndicator


def isni_assignation_review_dialog(parent):
    return IsniAssignationReviewDialogDriver(window(ISNIAssignationReviewDialog), parent.prober,
                                             parent.gesture_performer)


class IsniAssignationReviewDialogDriver(QDialogDriver, ScreenDriver):
    def select_individual(self):
        self.radio(named("_individual_button")).click()

    def select_organization(self):
        self.radio(named("_organization_button")).click()

    def has_works(self, *works):
        for work in works:
            self._works_list.has_item(with_item_text(work))

    def shows_main_artist_section(self):
        self._main_artist_section.is_showing_on_screen()

    def hides_main_artist_section(self):
        self._main_artist_section.is_hidden()

    def is_showing_progress_indicator(self):
        self.progress_indicator.is_(running())

    def has_stopped_progress_indicator(self):
        self.progress_indicator.is_(stopped())

    def has_ok_button_disabled(self):
        self.ok_button().is_disabled()

    def has_ok_button_enabled(self):
        self.ok_button().is_enabled()

    def shows_connection_error_message(self, visible=True):
        if visible:
            self.label(named("_connection_error_message")).is_showing_on_screen()
        else:
            self.label(named("_connection_error_message")).is_hidden()

    def shows_insufficient_error_message(self, visible=True):
        if visible:
            self.label(named("_insufficient_error_message")).is_showing_on_screen()
        else:
            self.label(named("_insufficient_error_message")).is_hidden()

    @property
    def progress_indicator(self):
        return WidgetDriver.find_single(self, QProgressIndicator, named("_progress_indicator"))

    @property
    def _works_list(self):
        return self.list_view(named("_works"))

    @property
    def _main_artist_section(self):
        return WidgetDriver.find_single(self, QWidget, named("_main_artist_box"))


def running():
    return StateMatcher(QProgressIndicator.isRunning, "running", "stopped")


def stopped():
    return StateMatcher(QProgressIndicator.isStopped, "stopped", "running")

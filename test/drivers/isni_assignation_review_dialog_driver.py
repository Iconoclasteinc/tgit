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
from PyQt5.QtWidgets import QListView, QWidget

from cute.matchers import named, with_list_item_text
from cute.widgets import window, QDialogDriver, QListViewDriver, WidgetDriver
from tgit.ui.dialogs.isni_assignation_review_dialog import ISNIAssignationReviewDialog
from ._screen_driver import ScreenDriver


def isni_assignation_review_dialog(parent):
    return IsniAssignationReviewDialogDriver(
        window(ISNIAssignationReviewDialog, named("isni_assignation_review_dialog")),
        parent.prober,
        parent.gesture_performer)


class IsniAssignationReviewDialogDriver(QDialogDriver, ScreenDriver):
    def select_individual(self):
        self.radio(named("_individual_button")).click()

    def select_organization(self):
        self.radio(named("_organization_button")).click()

    def has_work(self, work):
        QListViewDriver.find_single(self, QListView).has_item(with_list_item_text(work))

    def shows_main_artist_section(self):
        self.lead_performer_section.is_showing_on_screen()

    def hides_main_artist_section(self):
        self.lead_performer_section.is_hidden()

    @property
    def lead_performer_section(self):
        return WidgetDriver.find_single(self, QWidget, named("_lead_performer_box"))

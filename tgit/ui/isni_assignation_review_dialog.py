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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from tgit.ui.helpers.ui_file import UIFile
from tgit.identity import Identity


class ISNIAssignationReviewDialog(QDialog, UIFile):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/isni_assignation_review_dialog.ui")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._individual_button.setAttribute(Qt.WA_MacShowFocusRect, False)
        self._organization_button.setAttribute(Qt.WA_MacShowFocusRect, False)

    @property
    def _type(self):
        return Identity.INDIVIDUAL if self._individual_button.isChecked() else Identity.ORGANIZATION

    def review(self, on_review, *works):
        self._works.addItems([work.track_title for work in works])
        self.accepted.connect(lambda: on_review(self._type))
        self.open()

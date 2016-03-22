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

from tgit.identity import IdentityCard
from tgit.ui.helpers.ui_file import UIFile


def make_isni_assignation_review_dialog(titles, on_review, parent=None, main_artist_section_visible=False,
                                        delete_on_close=True):
    dialog = ISNIAssignationReviewDialog(parent, main_artist_section_visible, delete_on_close)
    dialog.review(on_review, *titles)
    return dialog


class ISNIAssignationReviewDialog(QDialog, UIFile):
    def __init__(self, parent, main_artist_section_visible, delete_on_close):
        super().__init__(parent)
        self._main_artist_section_visible = main_artist_section_visible
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/isni_assignation_review_dialog.ui")
        self._lead_performer_box.setVisible(self._main_artist_section_visible )

    @property
    def _type(self):
        return IdentityCard.INDIVIDUAL if self._individual_button.isChecked() else IdentityCard.ORGANIZATION

    def review(self, on_review, *works):
        def on_accept():
            if self._main_artist_section_visible:
                on_review(self._type)
            else:
                on_review()

        self._works.addItems([work.track_title for work in works])
        self.accepted.connect(on_accept)

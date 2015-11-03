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
from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit

from tgit.ui.helpers.ui_file import UIFile

INSTRUMENT_COLUMN_INDEX = 0
PERFORMER_COLUMN_INDEX = 1
REMOVE_BUTTON_COLUMN_INDEX = 2
FIRST_PERFORMER_ROW_INDEX = 1


def _build_line_edit(content, name):
    edit = QLineEdit(content)
    edit.setMinimumWidth(200)
    edit.setObjectName(name)
    edit.setAttribute(Qt.WA_MacShowFocusRect, False)
    return edit


class PerformerDialog(QDialog, UIFile):
    def __init__(self, album, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui(album.guest_performers)

    def _setup_ui(self, performers):
        self._load(":ui/performers_dialog.ui")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._add_performer.clicked.connect(self._add_performer_row)
        self._build_performers_table(performers)

    def _build_performers_table(self, performers):
        if len(performers) > 0:
            for performer in performers:
                self._build_performer_row(performer)
        else:
            self._build_performer_row()

    def _add_performer_row(self):
        self._build_performer_row()

    def _get_performers(self):
        performers = []
        for row_index in range(FIRST_PERFORMER_ROW_INDEX, self._performers_table.layout().rowCount()):
            performer = self._get_performer_from(row_index)
            if performer is not None:
                performers.append(performer)

        return performers

    def _get_performer_from(self, row_index):
        if self._row_is_empty(row_index):
            return None

        layout = self._performers_table.layout()
        name = layout.itemAtPosition(row_index, PERFORMER_COLUMN_INDEX).widget().text()
        instrument = layout.itemAtPosition(row_index, INSTRUMENT_COLUMN_INDEX).widget().text()

        if instrument.strip() != "" and name.strip() != "":
            return instrument, name
        return None

    def _row_is_empty(self, index):
        return self._performers_table.layout().itemAtPosition(index, PERFORMER_COLUMN_INDEX) is None

    def edit(self, on_edit):
        self._action_buttons.accepted.connect(lambda: on_edit(self._get_performers()))
        self.open()

    def _build_performer_row(self, performer=(None, None)):
        layout = self._performers_table.layout()
        index = layout.rowCount()

        instrument, name = performer
        layout.addWidget(_build_line_edit(name, "performer_{0}".format(index)), index, PERFORMER_COLUMN_INDEX)
        layout.addWidget(_build_line_edit(instrument, "instrument_{0}".format(index)), index, INSTRUMENT_COLUMN_INDEX)
        if index > FIRST_PERFORMER_ROW_INDEX:
            layout.addWidget(self._build_remove_line_button(index), index, REMOVE_BUTTON_COLUMN_INDEX)

    def _build_remove_line_button(self, index):
        button = QPushButton()
        button.setObjectName("remove_performer_{0}".format(index))
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedSize(20, 20)
        button.clicked.connect(lambda: self._remove_row(index))
        return button

    def _remove_row(self, row_index):
        layout = self._performers_table.layout()
        for col_index in range(self._performers_table.layout().columnCount()):
            widget = layout.itemAtPosition(row_index, col_index).widget()
            layout.removeWidget(widget)
            widget.close()

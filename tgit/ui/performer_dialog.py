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

import sys
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QHBoxLayout, \
    QWidget

from tgit.ui.helpers.ui_file import UIFile

mac = sys.platform == "darwin"

PERFORMER_COLUMN_INDEX = 0
INSTRUMENT_COLUMN_INDEX = 1


def _get_spacer_width():
    return 39 if mac else 30


def _get_performer_from(row_layout):
    instrument = row_layout.itemAt(PERFORMER_COLUMN_INDEX).widget().text()
    name = row_layout.itemAt(INSTRUMENT_COLUMN_INDEX).widget().text()

    if instrument.strip() != "" and name.strip() != "":
        return instrument, name
    return None


def _build_line_edit(content, name):
    edit = QLineEdit(content)
    edit.setObjectName(name)
    return edit


class PerformerDialog(QDialog, UIFile):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":ui/performers_dialog.ui")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._add_performer.clicked.connect(self._add_performer_row)

    def _add_performer_row(self):
        self._performers_table.addWidget(self._build_performer_row(index=self._performers_table.count()))

    def display(self, performers):
        if len(performers) > 0:
            for index, performer in enumerate(performers):
                self._performers_table.addWidget(self._build_performer_row(performer, index))
        else:
            self._performers_table.addWidget(self._build_performer_row())

    def _build_performer_row(self, performer=(None, None), index=0):
        instrument, name = performer

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(_build_line_edit(instrument, "instrument_{0}".format(index)))
        layout.addWidget(_build_line_edit(name, "performer_{0}".format(index)))

        if index > 0:
            layout.addWidget(self._build_remove_line_button(index))
        else:
            layout.addSpacing(_get_spacer_width())

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _build_remove_line_button(self, index):
        button = QPushButton()
        button.setObjectName("remove_performer_{0}".format(index))
        button.setText("-")
        button.clicked.connect(lambda: self._remove_row(button.parentWidget()))
        return button

    @property
    def performers(self):
        performers = []
        for i in range(self._performers_table.count()):
            performer = _get_performer_from(self._performers_table.itemAt(i).widget().layout())
            if performer is not None:
                performers.append(performer)
        return performers

    def _remove_row(self, row):
        layout = row.layout()
        for index in reversed(range(layout.count())):
            layout.takeAt(index).widget().close()
        row.close()
        self._performers_table.removeWidget(row)

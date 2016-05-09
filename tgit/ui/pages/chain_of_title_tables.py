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
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QComboBox

from tgit.signal import signal
from tgit.ui.pages.chain_of_title_tables_models import AuthorsComposersColumns, PublishersColumns, affiliations


class Table:
    _columns = Enum

    def __init__(self, table):
        self._table = table
        self._setup_header()

    def _value_of_cell(self, row, col):
        item = self._table.item(row, col)
        return item.text() if item else ""

    def _clear(self):
        while self._table.rowCount() > 0:
            self._table.removeRow(0)

    def _count(self):
        return self._table.rowCount()

    def _setup_header(self):
        header = self._table.horizontalHeader()
        for column in self._columns:
            header.resizeSection(column.position, column.width)
            header.setSectionResizeMode(column.position, column.resize_mode)


class ContributorsTable(Table):
    on_contributor_changed = signal(dict)


class AuthorsComposersTable(ContributorsTable):
    _columns = AuthorsComposersColumns

    def __init__(self, table):
        super().__init__(table)
        table.cellChanged.connect(lambda row, _: self._contributor_changed(row))

    def display(self, chain_of_title):
        self._clear()
        publishers = [name for name in chain_of_title.contributors["publishers"].keys()]
        authors_composers = chain_of_title.contributors["authors_composers"].values()

        for contributor in authors_composers:
            self._add_contributor(contributor, publishers)

    def _add_contributor(self, contributor, publishers):
        row = self._count()
        self._table.insertRow(self._count())

        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item.setText(contributor["name"])
        self._table.setItem(row, 0, item)

        combo = QComboBox()
        combo.addItem("")
        combo.addItems(affiliations)
        combo.currentIndexChanged.connect(lambda _: self._contributor_changed(row))
        combo.setCurrentText(contributor.get("affiliation"))
        self._table.setCellWidget(row, 1, combo)

        combo = QComboBox()
        combo.addItem("")
        combo.addItems(publishers)
        combo.currentIndexChanged.connect(lambda _: self._contributor_changed(row))
        combo.setCurrentText(contributor.get("publisher"))
        self._table.setCellWidget(row, 2, combo)

        item = QTableWidgetItem()
        item.setText(contributor.get("share"))
        self._table.setItem(row, 3, item)

    def _contributor_changed(self, row):
        self.on_contributor_changed.emit(dict(name=(self._value_of_cell(row, 0)),
                                              affiliation=(self._value_of_combo_in_cell(row, 1)),
                                              publisher=(self._value_of_combo_in_cell(row, 2)),
                                              share=(self._value_of_cell(row, 3))))

    def _value_of_combo_in_cell(self, row, col):
        combo = self._table.cellWidget(row, col)
        return combo.currentText() if combo else ""


class PublishersTable(ContributorsTable):
    _columns = PublishersColumns

    def __init__(self, table):
        super().__init__(table)
        table.cellChanged.connect(lambda row, _: self._contributor_changed(row))

    def display(self, chain_of_title):
        self._clear()

        for contributor in chain_of_title.contributors["publishers"].values():
            self._add_contributor(contributor)

    def _add_contributor(self, contributor):
        row = self._count()
        self._table.insertRow(row)

        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item.setText(contributor["name"])
        self._table.setItem(row, 0, item)

        item = QTableWidgetItem()
        item.setText(contributor.get("share"))
        self._table.setItem(row, 1, item)

    def _contributor_changed(self, row):
        self.on_contributor_changed.emit(dict(name=(self._value_of_cell(row, 0)),
                                              share=(self._value_of_cell(row, 1))))

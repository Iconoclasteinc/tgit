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
from collections import namedtuple
from enum import Enum

from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtWidgets import QHeaderView

from tgit import platforms
from tgit.ui.pages.contributors_table_model import Contributor, Cell

Column = namedtuple("Column", ["position", "length", "resize_mode"])


class Columns(Enum):
    name = Column(0, 200, QHeaderView.Stretch)
    role = Column(1, 160 if platforms.mac else 120, QHeaderView.Fixed)
    ipi = Column(2, 105 if platforms.mac else 80, QHeaderView.Fixed)
    isni = Column(3, 160 if platforms.mac else 140, QHeaderView.Fixed)

    @classmethod
    def at(cls, col):
        return list([column.value for _, column in cls.__members__.items()])[col]

    @classmethod
    def position(cls, col):
        return cls(col).value.position

    def __len__(self):
        return self.__members__.items()


class ContributorsTable(QObject):
    on_contributors_changed = pyqtSignal(list)
    on_contributor_selected = pyqtSignal()
    on_ipi_changed = pyqtSignal(str, str)

    def __init__(self, table, lookup_ipi, lookup_isni):
        super().__init__()
        self._lookup_isni = lookup_isni
        self._lookup_ipi = lookup_ipi
        self._table = table
        self._contributors = []

        self._table.itemSelectionChanged.connect(self.on_contributor_selected.emit)
        self._table.cellChanged.connect(self._contributor_changed)
        self._setup_header()

    def _setup_header(self):
        header = self._table.horizontalHeader()
        for col in range(len(Columns)):
            header.resizeSection(col, Columns.at(col).length)
            header.setSectionResizeMode(col, Columns.at(col).resize_mode)

    def add_row(self):
        contributor = Contributor()
        self._contributors.append(contributor)
        self._create_row(self._table.rowCount(), contributor)

    def remove_row(self):
        row = self._table.currentRow()
        self._contributors.pop(row)
        self._table.removeRow(row)
        self.on_contributors_changed.emit(self._contributors)

    def display(self, track):
        isnis = track.album.isnis or {}
        ipis = track.album.ipis or {}

        self._contributors = []
        self._add_contributor(track.lyricist or [], self.tr("Author"), ipis, isnis)
        self._add_contributor(track.composer or [], self.tr("Composer"), ipis, isnis)
        self._add_contributor(track.publisher or [], self.tr("Publisher"), ipis, isnis)

        self._display_table()

    def update_identifiers(self, ipis, isnis):
        for contributor in self._contributors:
            contributor.ipi = ipis.get(contributor.name)
            contributor.isni = isnis.get(contributor.name)

        for row in range(self._table.rowCount()):
            self._table.item(row, Columns.position(Columns.ipi)).setText(self._contributors[row].ipi)
            self._table.item(row, Columns.position(Columns.isni)).setText(self._contributors[row].isni)

    def _contributor_changed(self, row, column):
        self._table.item(row, column).value_changed()

    def _add_contributor(self, contributors, role, ipis, isnis):
        for name in contributors:
            self._contributors.append(Contributor(name, role, ipis.get(name), isnis.get(name)))

    def _display_table(self):
        self._clear_table()
        for row, contributor in enumerate(self._contributors):
            self._create_row(row, contributor)

    def _clear_table(self):
        while self._table.rowCount() > 0:
            self._table.removeRow(0)

    def _create_row(self, row, contributor):
        def on_contributor_changed():
            self.on_contributors_changed.emit(self._contributors)

        ipi = Cell.IPI(contributor, self.on_ipi_changed.emit)
        isni = Cell.ISNI(contributor)
        name = Cell.Name(contributor, ipi, isni, self._lookup_ipi, self._lookup_isni, on_contributor_changed)
        role = Cell.Role(contributor, on_contributor_changed)
        self._table.insertRow(row)
        self._table.setItem(row, Columns.position(Columns.name), name)
        self._table.setItem(row, Columns.position(Columns.ipi), ipi)
        self._table.setItem(row, Columns.position(Columns.isni), isni)
        self._table.setCellWidget(row, Columns.position(Columns.role), role)

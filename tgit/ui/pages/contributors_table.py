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

from PyQt5.QtCore import QObject, pyqtSignal

from tgit.ui.pages.chain_of_title_tables import Table
from tgit.ui.pages.contributors_table_model import Contributor, Cell, ContributorsColumns


class ContributorsTable(QObject, Table):
    on_contributors_changed = pyqtSignal(list)
    on_contributor_selected = pyqtSignal()
    on_ipi_changed = pyqtSignal(str, str)

    _columns = ContributorsColumns

    def __init__(self, table, lookup_ipi, lookup_isni):
        super().__init__(table=table)
        self._lookup_isni = lookup_isni
        self._lookup_ipi = lookup_ipi
        self._contributors = []

        self._table.itemSelectionChanged.connect(self.on_contributor_selected.emit)
        self._table.cellChanged.connect(lambda row, column: self._table.item(row, column).value_changed())
        self._setup_header()

    def add_row(self):
        contributor = Contributor()
        self._contributors.append(contributor)
        self._create_row(self._count(), contributor)

    def remove_row(self):
        row = self._table.currentRow()
        self._contributors.pop(row)
        self._table.removeRow(row)
        self.on_contributors_changed.emit(self._contributors)

    def display(self, track):
        self._contributors = []
        self._add_contributor(track.lyricist, Contributor.AUTHOR, track.album.ipis, track.album.isnis)
        self._add_contributor(track.composer, Contributor.COMPOSER, track.album.ipis, track.album.isnis)
        self._add_contributor(track.publisher, Contributor.PUBLISHER, track.album.ipis, track.album.isnis)

        self._display_table()

    def update_identifiers(self, ipis, isnis):
        for contributor in self._contributors:
            contributor.ipi = ipis.get(contributor.name)
            contributor.isni = isnis.get(contributor.name)

        for row in range(self._count()):
            self._table.item(row, ContributorsColumns.ipi.position).setText(self._contributors[row].ipi)
            self._table.item(row, ContributorsColumns.isni.position).setText(self._contributors[row].isni)

    def _add_contributor(self, contributors, role, ipis, isnis):
        for name in contributors:
            self._contributors.append(Contributor(name, self.tr(role), ipis.get(name, ""), isnis.get(name, "")))

    def _display_table(self):
        self._clear()
        for row, contributor in enumerate(self._contributors):
            self._create_row(row, contributor)

    def _create_row(self, row, contributor):
        def contributor_changed(*_):
            if contributor.name and contributor.role:
                self.on_contributors_changed.emit(self._contributors)

        name = Cell.Name(contributor)
        ipi = Cell.IPI(contributor, self._lookup_ipi)
        isni = Cell.ISNI(contributor, self._lookup_isni)
        role = Cell.Role(contributor, self._roles)

        name.on_name_changed.subscribe(contributor_changed)
        name.on_name_changed.subscribe(ipi.name_changed)
        name.on_name_changed.subscribe(isni.name_changed)
        ipi.on_ipi_changed.subscribe(self.on_ipi_changed.emit)
        role.on_role_changed.connect(contributor_changed)

        self._table.insertRow(row)
        self._table.setItem(row, ContributorsColumns.name.position, name)
        self._table.setItem(row, ContributorsColumns.ipi.position, ipi)
        self._table.setItem(row, ContributorsColumns.isni.position, isni)
        self._table.setCellWidget(row, ContributorsColumns.role.position, role)

    @property
    def _roles(self):
        return ["", self.tr(Contributor.AUTHOR), self.tr(Contributor.COMPOSER), self.tr(Contributor.PUBLISHER)]

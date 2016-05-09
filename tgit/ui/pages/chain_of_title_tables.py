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

from tgit.signal import signal
from tgit.ui.pages.chain_of_title_tables_models import AuthorsComposersColumns, PublishersColumns, affiliations, \
    AuthorComposer, Cell, Contributor


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

    def __init__(self, table):
        super().__init__(table)
        self._contributors = []

    def _emit_contributor_changed(self, contributor):
        values = dict(name=contributor.name, share=contributor.share)
        if isinstance(contributor, AuthorComposer):
            values["affiliation"] = contributor.affiliation
            values["publisher"] = contributor.publisher

        self.on_contributor_changed.emit(values)


class AuthorsComposersTable(ContributorsTable):
    _columns = AuthorsComposersColumns

    def __init__(self, table):
        super().__init__(table)
        table.cellChanged.connect(lambda row, column: self._table.item(row, column).value_changed())

    def display(self, chain_of_title):
        self._contributors = []
        for contributor in chain_of_title.contributors["authors_composers"].values():
            self._contributors.append(AuthorComposer(**contributor))

        self._display_table([name for name in chain_of_title.contributors["publishers"].keys()])

    def _display_table(self, publishers):
        self._clear()
        for row, contributor in enumerate(self._contributors):
            self._create_row(row, contributor, publishers)

    def _create_row(self, row, contributor, publishers):
        name = Cell.Name(contributor)
        affiliation = Cell.Affiliation(contributor, affiliations)
        publisher = Cell.Publisher(contributor, publishers)
        share = Cell.Share(contributor)

        affiliation.on_affiliation_changed.connect(self._emit_contributor_changed)
        publisher.on_publisher_changed.connect(self._emit_contributor_changed)
        share.on_share_changed.subscribe(self._emit_contributor_changed)

        self._table.insertRow(row)
        self._table.setItem(row, AuthorsComposersColumns.name.position, name)
        self._table.setCellWidget(row, AuthorsComposersColumns.affiliation.position, affiliation)
        self._table.setCellWidget(row, AuthorsComposersColumns.publisher.position, publisher)
        self._table.setItem(row, AuthorsComposersColumns.share.position, share)


class PublishersTable(ContributorsTable):
    _columns = PublishersColumns

    def __init__(self, table):
        super().__init__(table)
        table.cellChanged.connect(lambda row, column: self._table.item(row, column).value_changed())

    def display(self, chain_of_title):
        self._contributors = []
        for contributor in chain_of_title.contributors["publishers"].values():
            self._contributors.append(Contributor(**contributor))

        self._display_table()

    def _display_table(self):
        self._clear()
        for row, contributor in enumerate(self._contributors):
            self._create_row(row, contributor)

    def _create_row(self, row, contributor):
        name = Cell.Name(contributor)
        share = Cell.Share(contributor)

        share.on_share_changed.subscribe(self._emit_contributor_changed)

        self._table.insertRow(row)
        self._table.setItem(row, PublishersColumns.name.position, name)
        self._table.setItem(row, PublishersColumns.share.position, share)

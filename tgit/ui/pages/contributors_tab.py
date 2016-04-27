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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHeaderView

from tgit.album import AlbumListener
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.pages.contributors_tab_model import Cell, Contributor


def make_contributors_tab(project, track, on_metadata_changed, on_isni_local_lookup, on_ipi_local_lookup,
                          on_ipi_changed):
    tab = ContributorsTab(on_isni_local_lookup, on_ipi_local_lookup)
    tab.display(track)
    tab.on_metadata_changed.connect(lambda metadata: on_metadata_changed(**metadata))
    tab.on_ipi_changed.connect(on_ipi_changed)

    # todo when we have proper signals on album, we can get rid of that
    project.addAlbumListener(tab)
    tab.closed.connect(lambda: project.removeAlbumListener(tab))

    return tab


@Closeable
class ContributorsTab(QWidget, UIFile, AlbumListener):
    NAME_CELL_INDEX = 0
    ROLE_CELL_INDEX = 1
    IPI_CELL_INDEX = 2
    ISNI_CELL_INDEX = 3

    closed = pyqtSignal()
    on_metadata_changed = pyqtSignal(dict)
    on_ipi_changed = pyqtSignal(str, str)

    def __init__(self, on_isni_local_lookup, on_ipi_local_lookup):
        super().__init__()
        self._lookup_ipi = on_ipi_local_lookup
        self._lookup_isni = on_isni_local_lookup
        self._contributors = []
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/contributors_tab.ui")
        self._add_button.clicked.connect(self._add_row)
        self._remove_button.clicked.connect(self._remove_row)
        self._contributors_table.itemSelectionChanged.connect(self._update_actions)
        self._contributors_table.cellChanged.connect(self._contributor_changed)
        self._setup_header()

    def _setup_header(self):
        header = self._contributors_table.horizontalHeader()
        header.resizeSection(self.NAME_CELL_INDEX, 200)
        header.setSectionResizeMode(self.NAME_CELL_INDEX, QHeaderView.Stretch)
        header.resizeSection(self.ROLE_CELL_INDEX, 120)
        header.setSectionResizeMode(self.ROLE_CELL_INDEX, QHeaderView.Fixed)
        header.resizeSection(self.IPI_CELL_INDEX, 61)
        header.setSectionResizeMode(self.IPI_CELL_INDEX, QHeaderView.Fixed)
        header.resizeSection(self.ISNI_CELL_INDEX, 103)
        header.setSectionResizeMode(self.ISNI_CELL_INDEX, QHeaderView.Fixed)

    def display(self, track):
        isnis = track.album.isnis or {}
        ipis = track.album.ipis or {}
        lyricists = track.lyricist or []
        composers = track.composer or []
        publishers = track.publisher or []

        self._contributors = []
        for name in lyricists:
            self._contributors.append(Contributor(name, self.tr("Author"), ipis.get(name), isnis.get(name)))

        for name in composers:
            self._contributors.append(Contributor(name, self.tr("Composer"), ipis.get(name), isnis.get(name)))

        for name in publishers:
            self._contributors.append(Contributor(name, self.tr("Publisher"), ipis.get(name), isnis.get(name)))

        self._refresh_table_display()

    def _display_project(self, project):
        isnis = project.isnis or {}
        ipis = project.ipis or {}

        for contributor in self._contributors:
            contributor.ipi = ipis.get(contributor.name)
            contributor.isni = isnis.get(contributor.name)

        self._refresh_table_display()

    def albumStateChanged(self, project):
        self._display_project(project)

    def _add_row(self):
        self._contributors.append(Contributor())
        self._refresh_table_display()

    def _remove_row(self):
        self._contributors.pop(self._contributors_table.currentRow())
        self._refresh_table_display()

        if len(self._contributors) == 0:
            self._remove_button.setEnabled(False)

        self._metadata_changed()

    def _update_actions(self):
        self._remove_button.setEnabled(True)

    def _refresh_table_display(self):
        self._clear_table()
        for row, contributor in enumerate(self._contributors):
            self._create_row(row, contributor)

    def _clear_table(self):
        while self._contributors_table.rowCount() > 0:
            self._contributors_table.removeRow(0)

    def _create_row(self, row, contributor):
        ipi = Cell.IPI(contributor, self.on_ipi_changed.emit)
        isni = Cell.ISNI(contributor)
        name = Cell.Name(contributor, ipi, isni, self._lookup_ipi, self._lookup_isni, self._metadata_changed)
        role = Cell.Role(contributor, self._metadata_changed)
        self._contributors_table.insertRow(row)
        self._contributors_table.setItem(row, self.NAME_CELL_INDEX, name)
        self._contributors_table.setItem(row, self.IPI_CELL_INDEX, ipi)
        self._contributors_table.setItem(row, self.ISNI_CELL_INDEX, isni)
        self._contributors_table.setCellWidget(row, self.ROLE_CELL_INDEX, role)

    def _contributor_changed(self, row, column):
        self._contributors_table.item(row, column).value_changed()

    def _metadata_changed(self):
        metadata = dict(lyricist=[], composer=[], publisher=[])
        for contributor in self._contributors:
            if contributor.role == self.tr("Author"):
                metadata["lyricist"].append(contributor.name)

            if contributor.role == self.tr("Composer"):
                metadata["composer"].append(contributor.name)

            if contributor.role == self.tr("Publisher"):
                metadata["publisher"].append(contributor.name)

        self.on_metadata_changed.emit(metadata)

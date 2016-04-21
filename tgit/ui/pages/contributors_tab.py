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
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QTableWidgetItem

from tgit.album import AlbumListener
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile


def make_contributors_tab(project, track, on_metadata_changed, on_isni_local_lookup, on_ipi_local_lookup):
    tab = ContributorsTab(on_isni_local_lookup, on_ipi_local_lookup)
    tab.display(project, track)
    tab.on_metadata_changed.connect(lambda metadata: on_metadata_changed(**metadata))

    subscription = track.metadata_changed.subscribe(tab.display_track)
    tab.closed.connect(lambda: subscription.cancel())
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

    _contributors = []

    class Contributor:
        name = ""
        role = ""
        ipi = ""
        isni = ""

    def __init__(self, on_isni_local_lookup, on_ipi_local_lookup):
        super().__init__()
        self._on_ipi_local_lookup = on_ipi_local_lookup
        self._on_isni_local_lookup = on_isni_local_lookup

        self._load(":/ui/contributors_tab.ui")
        self._add_button.clicked.connect(self._add_row)
        self._remove_button.clicked.connect(self._remove_row)
        self._contributors_table.itemSelectionChanged.connect(self._update_actions)
        self._contributors_table.cellChanged.connect(self._contributor_changed)

    def display(self, project, track):
        self._display_project(project)
        self.display_track(track)

    def display_track(self, track):
        pass

    def _display_project(self, project):
        pass

    def albumStateChanged(self, project):
        self._display_project(project)

    def _add_row(self):
        self._contributors.append(self.Contributor())
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
        while self._contributors_table.rowCount() > 0:
            self._contributors_table.removeRow(0)

        for contributor in self._contributors:
            index = self._contributors_table.rowCount()
            self._contributors_table.insertRow(index)

            item = QTableWidgetItem()
            item.setText(contributor.name)
            self._contributors_table.setItem(index, self.NAME_CELL_INDEX, item)

            combo = QComboBox()
            combo.addItems(["", self.tr("Author"), self.tr("Composer"), self.tr("Publisher")])
            combo.setCurrentText(contributor.role)
            combo.currentIndexChanged.connect(lambda _: self._contributor_changed(index, 1))
            self._contributors_table.setCellWidget(index, self.ROLE_CELL_INDEX, combo)

            item = QTableWidgetItem()
            item.setText(contributor.ipi)
            self._contributors_table.setItem(index, self.IPI_CELL_INDEX, item)

            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setText(contributor.isni)
            self._contributors_table.setItem(index, self.ISNI_CELL_INDEX, item)

    def _contributor_changed(self, row, column):
        item = self._contributors_table.item(row, column)
        new_value = item.text() if item else ""

        if column == self.NAME_CELL_INDEX and self._contributors[row].name != new_value:
            self._contributors[row].isni = self._on_isni_local_lookup(new_value)
            self._contributors[row].ipi = self._on_ipi_local_lookup(new_value)
            self._contributors[row].name = new_value
            self._contributors_table.item(row, self.ISNI_CELL_INDEX).setText(self._contributors[row].isni)
            self._contributors_table.item(row, self.IPI_CELL_INDEX).setText(self._contributors[row].ipi)

        if column == self.IPI_CELL_INDEX and self._contributors[row].ipi != new_value:
            self._contributors[row].ipi = new_value

        if column == self.ISNI_CELL_INDEX and self._contributors[row].isni != new_value:
            self._contributors[row].isni = new_value

        if column == self.ROLE_CELL_INDEX:
            index = self._contributors_table.model().index(row, self.ROLE_CELL_INDEX)
            role_combo = self._contributors_table.indexWidget(index)
            if role_combo:
                self._contributors[row].role = role_combo.currentText()

        self._metadata_changed()

    def _metadata_changed(self):
        lyricist = None
        for contributor in self._contributors:
            if contributor.role == self.tr("Author"):
                lyricist = contributor
                break

        self.on_metadata_changed.emit(dict(lyricist=lyricist.name if lyricist else ""))
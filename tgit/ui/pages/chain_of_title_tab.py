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
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QComboBox

from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile


def make_chain_of_title_tab(track, chain_of_title, on_contributor_changed):
    tab = ChainOfTitleTab()
    tab.display(track)

    tab.on_contributor_changed.connect(lambda contributor: on_contributor_changed(**contributor))

    subscription = track.chain_of_title_changed.subscribe(tab.display)
    tab.closed.connect(lambda: subscription.cancel())

    return tab


@Closeable
class ChainOfTitleTab(QWidget, UIFile):
    closed = pyqtSignal()
    on_contributor_changed = pyqtSignal(dict)
    on_publisher_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._load(":/ui/chain_of_title_tab.ui")
        self._contributors_table.cellChanged.connect(lambda row, _: self._contributor_changed(row))
        self._publishers_table.cellChanged.connect(lambda row, _: self._publisher_changed(row))

    def display(self, track):
        lyricists = track.lyricist or []
        composers = track.composer or []
        publishers = track.publisher or []

        self._clear_table(self._contributors_table)
        self._clear_table(self._publishers_table)

        chain_of_title = track.chain_of_title
        for name in chain_of_title.keys():
            if name in lyricists or name in composers:
                self._create_contributor_row(self._contributors_table.rowCount(), chain_of_title[name], publishers)
            else:
                self._create_publisher_row(self._publishers_table.rowCount(), chain_of_title[name])

    @staticmethod
    def _clear_table(table):
        while table.rowCount() > 0:
            table.removeRow(0)

    def _create_contributor_row(self, row, contributor, publishers):
        self._contributors_table.insertRow(row)

        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item.setText(contributor["name"])
        self._contributors_table.setItem(row, 0, item)

        combo = QComboBox()
        combo.addItem("")
        combo.addItems(affiliations)
        combo.currentIndexChanged.connect(lambda _: self._contributor_changed(row))
        combo.setCurrentText(contributor.get("affiliation"))
        self._contributors_table.setCellWidget(row, 1, combo)

        combo = QComboBox()
        combo.addItem("")
        combo.addItems(publishers)
        combo.currentIndexChanged.connect(lambda _: self._contributor_changed(row))
        combo.setCurrentText(contributor.get("publisher"))
        self._contributors_table.setCellWidget(row, 2, combo)

        item = QTableWidgetItem()
        item.setText(contributor.get("share"))
        self._contributors_table.setItem(row, 3, item)

    def _create_publisher_row(self, row, contributor):
        self._publishers_table.insertRow(row)

        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item.setText(contributor["name"])
        self._publishers_table.setItem(row, 0, item)

        item = QTableWidgetItem()
        item.setText(contributor.get("share"))
        self._publishers_table.setItem(row, 1, item)

    def _contributor_changed(self, row):
        self.on_contributor_changed.emit(dict(name=(self._value_of_cell(self._contributors_table, row, 0)),
                                              affiliation=(self._value_of_combo_in_cell(row, 1)),
                                              publisher=(self._value_of_combo_in_cell(row, 2)),
                                              share=(self._value_of_cell(self._contributors_table, row, 3))))

    def _publisher_changed(self, row):
        self.on_contributor_changed.emit(dict(name=(self._value_of_cell(self._publishers_table, row, 0)),
                                              share=(self._value_of_cell(self._publishers_table, row, 1))))

    @staticmethod
    def _value_of_cell(table, row, col):
        item = table.item(row, col)
        return item.text() if item else ""

    def _value_of_combo_in_cell(self, row, col):
        combo = self._contributors_table.cellWidget(row, col)
        return combo.currentText() if combo else ""


affiliations = ["SOCAN", "ASCAP", "BMI"]

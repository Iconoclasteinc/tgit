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
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile


def make_chain_of_title_tab(chain):
    tab = ChainOfTitleTab()
    tab.display(chain)

    return tab


@Closeable
class ChainOfTitleTab(QWidget, UIFile):
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._load(":/ui/chain_of_title_tab.ui")

    def display(self, chain):
        for row in range(len(chain.contributors)):
            self._create_row(row, self._contributors_table, chain.contributors[row])

        for row in range(len(chain.publishers)):
            self._create_row(row, self._publishers_table, chain.publishers[row])

    @staticmethod
    def _create_row(row, table, contributor):
        table.insertRow(row)

        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item.setText(contributor.name)
        table.setItem(row, 0, item)

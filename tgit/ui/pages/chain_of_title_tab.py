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
from PyQt5.QtWidgets import QWidget

from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.pages.chain_of_title_tables import AuthorsComposersTable, PublishersTable


def make_chain_of_title_tab(chain_of_title, on_contributor_changed):
    tab = ChainOfTitleTab()
    tab.display(chain_of_title)

    tab.on_contributor_changed.connect(lambda contributor: on_contributor_changed(**contributor))

    subscription = chain_of_title.changed.subscribe(tab.display)
    tab.closed.connect(lambda: subscription.cancel())

    return tab


@Closeable
class ChainOfTitleTab(QWidget, UIFile):
    closed = pyqtSignal()
    on_contributor_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._load(":/ui/chain_of_title_tab.ui")

        self._authors_composers_table = AuthorsComposersTable(self._contributors_table)
        self._authors_composers_table.on_contributor_changed.subscribe(self.on_contributor_changed.emit)

        self._publishers_table_ = PublishersTable(self._publishers_table)
        self._publishers_table_.on_contributor_changed.subscribe(self.on_contributor_changed.emit)

    def display(self, chain_of_title):
        self._authors_composers_table.display(chain_of_title)
        self._publishers_table_.display(chain_of_title)

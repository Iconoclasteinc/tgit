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

import functools as func

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QVBoxLayout, QPushButton, QTableView, QHBoxLayout,
                         QItemDelegate, QHeaderView)

from tgit.announcer import Announcer
from tgit.audio.player import PlayerListener
from tgit.ui.album_table_model import AlbumTableModel, Columns
from tgit.ui import constants as ui


class PlayButtonDelegate(QItemDelegate):
    def __init__(self, view):
        QItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QPushButton(self.tr('Play'))
            button.setObjectName(ui.PLAY_BUTTON_NAME)
            button.clicked.connect(func.partial(index.model().togglePlay,
                                                index.model().trackAt(index.row())))
            button.setCheckable(True)
            self.parent().setIndexWidget(index, button)

        self.parent().indexWidget(index).setChecked(index.model().data(index))


class RemoveButtonDelegate(QItemDelegate):
    def __init__(self, view):
        QItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QPushButton(self.tr('Remove'))
            button.setObjectName(ui.REMOVE_BUTTON_NAME)
            button.clicked.connect(func.partial(index.model().remove,
                                                index.model().trackAt(index.row())))
            self.parent().setIndexWidget(index, button)


class TrackListPage(QWidget, PlayerListener):
    COLUMNS_WIDTHS = [300, 210, 200, 70, 70, 121, 105]

    def __init__(self, album, player, parent=None):
        QWidget.__init__(self, parent)
        self._tracks = AlbumTableModel(album, player, self)
        self._requestListeners = Announcer()

        self.setObjectName(ui.TRACK_LIST_PAGE_NAME)
        self._build()
        self.localize()

    def addRequestListener(self, listener):
        self._requestListeners.addListener(listener)

    def _build(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._addTrackTable(self._layout)
        self._addButtons(self._layout)

    def _resizeColumns(self):
        for index, width in enumerate(self.COLUMNS_WIDTHS):
            self._table.horizontalHeader().resizeSection(index, width)

    def _addTrackTable(self, layout):
        self._table = QTableView()
        self._table.setObjectName(ui.TRACK_TABLE_NAME)
        self._table.setModel(self._tracks)
        self._table.setItemDelegateForColumn(Columns.index(Columns.play),
                                             PlayButtonDelegate(self._table))
        self._table.setItemDelegateForColumn(Columns.index(Columns.remove),
                                             RemoveButtonDelegate(self._table))
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableView.NoEditTriggers)
        self._table.setSelectionMode(QTableView.NoSelection)
        self._table.setShowGrid(False)
        self._table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self._table.verticalHeader().setResizeMode(QHeaderView.Fixed)
        self._table.verticalHeader().setMovable(True)
        self._table.verticalHeader().sectionMoved.connect(self._tracks.move)
        self._resizeColumns()
        layout.addWidget(self._table)

    def _addButtons(self, layout):
        buttonLayout = QHBoxLayout()
        self._addButton = QPushButton()
        self._addButton.setObjectName(ui.ADD_FILES_BUTTON_NAME)
        self._addButton.clicked.connect(self._selectFiles)
        buttonLayout.addWidget(self._addButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def _selectFiles(self):
        self._requestListeners.selectFiles()

    def localize(self):
        self._addButton.setText(self.tr('Add Files...'))
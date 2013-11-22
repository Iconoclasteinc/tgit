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

from PyQt4.QtCore import Qt, QModelIndex, QAbstractItemModel
from PyQt4.QtGui import (QWidget, QVBoxLayout, QTableView, QHBoxLayout,
                         QStyledItemDelegate, QHeaderView, QLabel, QToolButton)

from tgit.announcer import Announcer
from tgit.audio.player import PlayerListener
from tgit.ui.album_table_model import AlbumTableModel, Columns
from tgit.ui import constants as ui


class PlayButtonDelegate(QStyledItemDelegate):
    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QToolButton()
            button.setObjectName(ui.PLAY_BUTTON_NAME)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(func.partial(index.model().togglePlay,
                                                index.model().trackAt(index.row())))
            button.setCheckable(True)
            self.parent().setIndexWidget(index, button)

        self.parent().indexWidget(index).setChecked(index.model().data(index))

        # This is awful, I need to paint a button and react to mouse events instead of
        #  using a real button
        class WackyHack(QModelIndex):
            def model(self):
                class FakeModel(QAbstractItemModel):
                    def data(self, index):
                        return ''

                return FakeModel()

        # We need to call the super implementation to style the column according to the stylesheet
        super(PlayButtonDelegate, self).paint(painter, option, WackyHack())


class RemoveButtonDelegate(QStyledItemDelegate):
    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QToolButton()
            button.setObjectName(ui.REMOVE_BUTTON_NAME)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(func.partial(index.model().remove,
                                                index.model().trackAt(index.row())))
            self.parent().setIndexWidget(index, button)

        super(RemoveButtonDelegate, self).paint(painter, option, index)


class TrackListPage(QWidget, PlayerListener):
    COLUMNS_WIDTHS = [375, 291, 175, 70, 70, 30, 30]

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
        layout = QVBoxLayout()
        layout.addWidget(self._makeHeader())
        layout.addWidget(self._makeTrackTable())
        self.setLayout(layout)

    def _makeHeader(self):
        header = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QLabel(self.tr('Organize tracks in album.')))
        layout.addStretch()
        self._addButton = QToolButton()
        self._addButton.setObjectName(ui.ADD_BUTTON_NAME)
        self._addButton.clicked.connect(self._selectFiles)
        self._addButton.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self._addButton)
        header.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        return header

    def _makeTrackTable(self):
        table = QTableView()
        table.setObjectName(ui.TRACK_TABLE_NAME)
        table.setModel(self._tracks)
        table.setItemDelegateForColumn(Columns.index(Columns.play), PlayButtonDelegate(table))
        table.setItemDelegateForColumn(Columns.index(Columns.remove), RemoveButtonDelegate(table))
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionMode(QTableView.NoSelection)
        table.setShowGrid(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        table.horizontalHeader().setResizeMode(Columns.index(Columns.play), QHeaderView.Fixed)
        table.horizontalHeader().setResizeMode(Columns.index(Columns.remove), QHeaderView.Fixed)
        table.verticalHeader().setResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setMovable(True)
        table.verticalHeader().sectionMoved.connect(self._tracks.move)
        self._resizeColumns(table)

        return table

    def _resizeColumns(self, table):
        for index, width in enumerate(self.COLUMNS_WIDTHS):
            table.horizontalHeader().resizeSection(index, width)

    def _selectFiles(self):
        self._requestListeners.selectFiles()

    def localize(self):
        self._addButton.setText(self.tr('ADD'))
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

from PyQt4.QtCore import Qt, QModelIndex, QAbstractItemModel, pyqtSignal
from PyQt4.QtGui import (QWidget, QVBoxLayout, QTableView, QHBoxLayout,
                         QStyledItemDelegate, QHeaderView, QLabel, QToolButton, QFrame, QPalette)

from tgit.announcer import Announcer
from tgit.ui.views.album_composition_model import Columns, Row
from tgit.ui import style


def albumCompositionPage(listener):
    page = AlbumCompositionPage()
    page.announceTo(listener)
    return page


class PlayButtonDelegate(QStyledItemDelegate):
    play = pyqtSignal(Row)

    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QToolButton()
            button.setObjectName(AlbumCompositionPage.PLAY_BUTTON_NAME)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(func.partial(self.play.emit, index.model().trackAt(index.row())))
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
        QStyledItemDelegate.paint(self, painter, option, WackyHack())


class RemoveButtonDelegate(QStyledItemDelegate):
    remove = pyqtSignal(Row)

    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QToolButton()
            button.setObjectName(AlbumCompositionPage.REMOVE_BUTTON_NAME)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(func.partial(self.remove.emit, index.model().trackAt(index.row())))
            self.parent().setIndexWidget(index, button)

        QStyledItemDelegate.paint(self, painter, option, index)


class AlbumCompositionPage(object):
    NAME = 'album-composition-page'

    TRACK_TABLE_NAME = 'track-list'
    ADD_BUTTON_NAME = 'add-tracks'
    PLAY_BUTTON_NAME = 'play-track'
    REMOVE_BUTTON_NAME = 'remove-track'

    def __init__(self):
        self._announce = Announcer()

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def render(self, album):
        self._widget = self._build(album)
        self.translate()
        return self._widget

    def _build(self, album):
        widget = QWidget()
        widget.setObjectName(self.NAME)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self._makeHeader())
        layout.addWidget(self._makeTableFrame(self._makeTrackTable(album)))
        return widget

    def _makeHeader(self):
        header = QWidget()
        layout = QHBoxLayout()
        header.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self._helpLabel = QLabel()
        layout.addWidget(self._helpLabel)
        layout.addStretch()
        self._addButton = QToolButton()
        self._addButton.setObjectName(self.ADD_BUTTON_NAME)
        self._addButton.clicked.connect(lambda pressed: self._announce.addTracksToAlbum())
        self._addButton.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self._addButton)

        return header

    def _makeTableFrame(self, table):
        frame = QFrame()
        frame.setFrameStyle(style.TABLE_BORDER_STYLE)
        frame.setAutoFillBackground(True)
        palette = frame.palette()
        palette.setColor(QPalette.Background, style.TABLE_BACKGROUND_COLOR)
        palette.setColor(QPalette.WindowText, style.TABLE_BORDER_COLOR)
        frame.setPalette(palette)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        frame.setLayout(layout)

        layout.addWidget(table)
        return frame

    def _makeTrackTable(self, album):
        table = QTableView()
        table.setFrameStyle(QFrame.NoFrame)
        table.setObjectName(self.TRACK_TABLE_NAME)
        table.setModel(album)
        playDelegate = PlayButtonDelegate(table)
        playDelegate.play.connect(self._announce.playTrack)
        table.setItemDelegateForColumn(Columns.index(Columns.play), playDelegate)
        removeDelegate = RemoveButtonDelegate(table)
        removeDelegate.remove.connect(self._announce.removeTrack)
        table.setItemDelegateForColumn(Columns.index(Columns.remove), removeDelegate)
        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionMode(QTableView.NoSelection)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        table.horizontalHeader().setResizeMode(Columns.index(Columns.play), QHeaderView.Fixed)
        table.horizontalHeader().setResizeMode(Columns.index(Columns.remove), QHeaderView.Fixed)
        table.verticalHeader().setResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setMovable(True)
        table.verticalHeader().sectionMoved.connect(lambda index, from_, to: self._announce.moveTrack(from_, to))
        self._resizeColumns(table)

        return table

    def _resizeColumns(self, table):
        for index, width in enumerate(style.TABLE_COLUMNS_WIDTHS):
            table.horizontalHeader().resizeSection(index, width)

    def translate(self):
        self._addButton.setText(self.tr('ADD'))
        self._helpLabel.setText(self.tr('Organize tracks in album.'))

    def tr(self, text):
        return self._widget.tr(text)

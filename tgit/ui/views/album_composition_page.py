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
from PyQt4.QtGui import QWidget, QTableView, QStyledItemDelegate, QHeaderView, QToolButton, QFrame, QPalette, QColor
from tgit.track import Track

from tgit.ui.views.album_composition_model import Columns, AlbumCompositionModel
from tgit.ui.widgets import form


class PlayButtonDelegate(QStyledItemDelegate):
    clicked = pyqtSignal(Track)

    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QToolButton()
            button.setObjectName('play-track')
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(func.partial(self.clicked.emit, index.model().trackAt(index.row())))
            button.setCheckable(True)
            self.parent().setIndexWidget(index, button)

        self.parent().indexWidget(index).setChecked(index.model().data(index))

        # This is awful, I need to paint a button and react to mouse events instead of
        #  using a real button
        class UglyHack(QModelIndex):
            def model(self):
                class FakeModel(QAbstractItemModel):
                    def data(self, index):
                        return ''

                return FakeModel()

        # We need to call the super implementation to style the column according to the stylesheet
        QStyledItemDelegate.paint(self, painter, option, UglyHack())


class RemoveButtonDelegate(QStyledItemDelegate):
    clicked = pyqtSignal(Track)

    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button = QToolButton()
            button.setObjectName('remove-track')
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(func.partial(self.clicked.emit, index.model().trackAt(index.row())))
            self.parent().setIndexWidget(index, button)

        QStyledItemDelegate.paint(self, painter, option, index)


LIGHT_GRAY = QColor.fromRgb(0xDDDDDD)


class AlbumCompositionPage(QWidget):
    # Using stylesheets on the table corrupts the display of the button widgets in the
    # cells, at least on OSX. So we have to style programmatically
    COLUMNS_WIDTHS = [345, 205, 215, 85, 65, 30, 30]

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName('album-composition-page')
        self.render()

    def bind(self, **handlers):
        if 'play' in handlers:
            self.play.clicked.connect(handlers['play'])
        if 'add' in handlers:
            self.addButton.clicked.connect(lambda pressed: handlers['add']())
        if 'remove' in handlers:
            self.remove.clicked.connect(handlers['remove'])
        if 'trackMoved' in handlers:
            self.table.verticalHeader().sectionMoved.connect(
                lambda _, from_, to: handlers['trackMoved'](self.table.model().trackAt(from_), to))

    def render(self):
        layout = form.column()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.makeHeader())
        self.table = self.makeTrackTable()
        self.play = self.makePlayButton(self.table)
        self.remove = self.makeRemoveButton(self.table)
        layout.addWidget(self.makeTableFrame(self.table))
        self.setLayout(layout)

    def makeHeader(self):
        header = QWidget()
        row = form.row()
        help = form.label()
        help.setText(self.tr('Organize tracks in album.'))
        row.addWidget(help)
        row.addStretch()
        self.addButton = form.button('add-tracks')
        self.addButton.setText(self.tr('ADD'))
        row.addWidget(self.addButton)
        header.setLayout(row)

        return header

    def makeTableFrame(self, table):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        frame.setAutoFillBackground(True)
        palette = frame.palette()
        palette.setColor(QPalette.Background, Qt.white)
        palette.setColor(QPalette.WindowText, LIGHT_GRAY)
        frame.setPalette(palette)
        layout = form.column()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(table)
        frame.setLayout(layout)

        return frame

    def makeTrackTable(self):
        table = QTableView()
        table.setFrameStyle(QFrame.NoFrame)
        table.setObjectName('track-list')
        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionMode(QTableView.NoSelection)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        table.verticalHeader().setResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setMovable(True)
        table.horizontalHeader().setResizeMode(Columns.index(Columns.play), QHeaderView.Fixed)
        table.horizontalHeader().setResizeMode(Columns.index(Columns.remove), QHeaderView.Fixed)
        return table

    def makePlayButton(self, table):
        button = PlayButtonDelegate(table)
        table.setItemDelegateForColumn(Columns.index(Columns.play), button)
        return button

    def makeRemoveButton(self, table):
        button = RemoveButtonDelegate(table)
        table.setItemDelegateForColumn(Columns.index(Columns.remove), button)
        return button

    def display(self, player, album):
        self.table.setModel(AlbumCompositionModel(album, player))
        for index, width in enumerate(self.COLUMNS_WIDTHS):
            self.table.horizontalHeader().resizeSection(index, width)
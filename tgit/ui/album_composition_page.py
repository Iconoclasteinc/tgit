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

from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel, pyqtSignal, QPoint
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QTableView, QStyledItemDelegate, QHeaderView, QToolButton, QFrame, QAction, QMenu

from tgit.track import Track
from tgit.ui.album_composition_model import Columns, AlbumCompositionModel
from tgit.ui.helpers import form


class PlayButtonDelegate(QStyledItemDelegate):
    clicked = pyqtSignal(Track)

    def __init__(self, view):
        QStyledItemDelegate.__init__(self, view)

    def paint(self, painter, option, index):
        play_button = self.parent().indexWidget(index)
        if not play_button:
            play_button = QToolButton()
            play_button.setObjectName('play-track')
            play_button.setCursor(Qt.PointingHandCursor)
            play_button.clicked.connect(func.partial(self.clicked.emit, index.model().trackAt(index.row())))
            play_button.setCheckable(True)
            _, playable = index.model().data(index)
            play_button.setEnabled(playable)
            if not playable:
                play_button.setToolTip(self.tr('FLAC playback is not supported on your platform'))
            self.parent().setIndexWidget(index, play_button)

        playing, _ = index.model().data(index)
        play_button.setChecked(playing)

        # This is awful, we need to remove the widgets from the table
        class UglyHack(QModelIndex):
            def model(self):
                class FakeModel(QAbstractItemModel):
                    def data(self, index):
                        return ''

                return FakeModel()

        # We need to call the super implementation to style the column according to the stylesheet
        QStyledItemDelegate.paint(self, painter, option, UglyHack())


LIGHT_GRAY = QColor.fromRgb(0xDDDDDD)


class AlbumCompositionPage(QWidget):
    playTrack = pyqtSignal(Track)
    remove_track = pyqtSignal(Track)
    addTracks = pyqtSignal()
    trackMoved = pyqtSignal(Track, int)

    # Using stylesheets on the table corrupts the display of the button widgets in the
    # cells, at least on OSX. So we have to style programmatically
    COLUMNS_WIDTHS = [345, 225, 225, 85, 65, 30, 30]

    def __init__(self):
        super().__init__()
        self.build()

    def build(self):
        self.setObjectName('album-composition-page')
        layout = form.column()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.makeHeader())
        self.table = self.makeTrackTable()
        self._add_context_menu()
        layout.addWidget(self.makeTableFrame(self.table))
        self.setLayout(layout)

    def makeHeader(self):
        header = QWidget()
        row = form.row()
        help = form.label()
        help.setText(self.tr("Organize the release's tracks."))
        row.addWidget(help)
        row.addStretch()
        addButton = form.button('add-tracks', self.tr('ADD'))
        addButton.clicked.connect(lambda pressed: self.addTracks.emit())
        row.addWidget(addButton)
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
        table.setSelectionMode(QTableView.SingleSelection)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setSectionsMovable(True)
        table.verticalHeader().sectionMoved.connect(
            lambda _, from_, to: self.trackMoved.emit(table.model().trackAt(from_), to))
        table.setItemDelegateForColumn(Columns.index(Columns.play), self.makePlayButton(table))
        table.setStyleSheet("""
            QTableView {
                alternate-background-color: #F9F7F7;
                selection-background-color: #F25C0A
            }

            QTableView::item {
                border-bottom: 1px solid #F7C3B7;
            }

            QHeaderView {
                background-color: white;
            }

            QHeaderView::section {
                background-color: transparent;
            }

            QHeaderView::section:horizontal {
                text-align: left;
                font-weight: bold;
                font-size: 13px;
                padding: 21px 0 18px 5px;
                border-top: 1px solid #F7C3B7;
                border-bottom: 1px solid #F7C3B7;
                border-right: 1px solid  #F2F2F2;
                min-height: 15px;
            }

            QHeaderView::section:vertical {
                padding: 4px 7px;
                border-bottom: 1px solid #F7C3B7;
                border-right: 1px solid #F7C3B7;
                border-left: none;
                border-top: none;
            }

            QTableCornerButton::section:vertical {
                background-color: white;
                border-top: 1px solid #F7C3B7;
                border-bottom: 1px solid #F7C3B7;
                border-right: 1px solid  #F2F2F2;
            }
        """)
        return table

    def _add_context_menu(self):
        # We don't want the menu to block so we can't use the ActionsContextMenu policy
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        context_menu = QMenu(self.table)
        context_menu.setObjectName("context_menu")
        remove_action = QAction(self.tr("Delete"), self.table)
        remove_action.setObjectName("delete_action")
        remove_action.triggered.connect(lambda checked: self._signal_remove_track(self.table.selectedIndexes()))
        context_menu.addAction(remove_action)

        def open_menu(pos):
            context_menu.popup(self._global_position(pos))

        self.table.customContextMenuRequested.connect(open_menu)
        remove_action.setShortcut(Qt.Key_Delete)
        # For the shortcut to work, it needs to be part of the action list of the table
        self.table.addAction(remove_action)

    def _global_position(self, pos):
        left_margin, top_margin = self.table.verticalHeader().width(), self.table.horizontalHeader().height()
        position_in_table = QPoint(pos.x() + left_margin, pos.y() + top_margin)
        return self.table.mapToGlobal(position_in_table)

    def _signal_remove_track(self, selection):
        if selection:
            self.remove_track.emit(self.table.model().trackAt(selection[0].row()))

    def makePlayButton(self, table):
        button = PlayButtonDelegate(table)
        button.clicked.connect(self.playTrack.emit)
        return button

    def resizeColumns(self):
        for index, width in enumerate(self.COLUMNS_WIDTHS):
            self.table.horizontalHeader().resizeSection(index, width)
        self.table.horizontalHeader().setSectionResizeMode(Columns.index(Columns.play), QHeaderView.Fixed)

    def display(self, player, album):
        self.table.setModel(AlbumCompositionModel(album, player))
        self.resizeColumns()
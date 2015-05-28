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

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView, QFrame, QAction, QMenu
from tgit.album import Album

from tgit.track import Track
from tgit.ui.album_composition_model import AlbumCompositionModel
from tgit.ui.helpers import form
from tgit.ui.observer import Observer

LIGHT_GRAY = QColor.fromRgb(0xDDDDDD)


@Observer
class AlbumCompositionPage(QWidget):
    play_track = pyqtSignal(Track)
    remove_track = pyqtSignal(Track)
    move_track = pyqtSignal(Track, int)
    addTracks = pyqtSignal()

    # Using stylesheets on the table corrupts the display of the button widgets in the
    # cells, at least on OSX. So we have to style programmatically
    COLUMNS_WIDTHS = [345, 255, 255, 85, 65, 30]

    _playing_track = None

    def __init__(self, player):
        super().__init__()

        self.subscribe(player.playing, self._on_playing_track)
        self.subscribe(player.stopped, self._on_stopped_track)

        self.build()

    def _on_playing_track(self, track):
        self._playing_track = track

    def _on_stopped_track(self, track):
        self._playing_track = None

    def build(self):
        self.setObjectName('album-composition-page')
        layout = form.column()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.makeHeader())
        self.table = self.makeTrackTable()
        self._make_context_menu()
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
        table.verticalHeader().sectionMoved.connect(self._signal_move_track)
        table.verticalHeader().sectionMoved.connect(lambda _, from_, to: self._select_row(to))
        table.setStyleSheet("""
            QTableView::item {
                border-bottom: 1px solid #F7C3B7;
            }

            QTableView::item::alternate {
                background-color:#F9F7F7;
            }

            QTableView::item::selected {
                background-color:#F25C0A;
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

    def _signal_move_track(self, _, from_, to):
        self.move_track.emit(self.table.model().trackAt(from_), to)

    def _select_row(self, row):
        self.table.setCurrentIndex(self.table.model().index(row, 0))

    def _is_selected(self, track):
        return self.selected_track == track

    def _update_context_menu(self):
        play_action_text = "Stop" if self._is_selected(self._playing_track) else "Play"
        self._play_action.setText('{0} "{1}"'.format(self.tr(play_action_text), self.selected_track.track_title))
        self._play_action.setDisabled(self.selected_track.type == Album.Type.FLAC)

    def _make_context_menu(self):
        # We don't want the menu to block so we can't use the ActionsContextMenu policy
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._context_menu = QMenu(self.table)
        self._context_menu.setObjectName("context_menu")

        remove_action = QAction(self.tr("Remove"), self.table)
        remove_action.setObjectName("remove_action")
        remove_action.setShortcut(Qt.Key_Delete)
        remove_action.triggered.connect(lambda checked: self._signal_remove_track())
        self._context_menu.addAction(remove_action)
        self.table.addAction(remove_action)

        self._play_action = QAction(self.table)
        self._play_action.setObjectName("play_action")
        self._play_action.triggered.connect(lambda checked: self._signal_play_track())
        self._context_menu.addAction(self._play_action)
        self.table.addAction(self._play_action)

        self.table.customContextMenuRequested.connect(self._open_context_menu)

    def _open_context_menu(self, pos):
        if self.selected_row is not None:
            self._update_context_menu()
            self._context_menu.popup(self._map_to_global(pos))

    def _map_to_global(self, pos):
        return self.table.mapToGlobal(self._map_to_table(pos))

    def _map_to_table(self, pos):
        left_margin, top_margin = self.table.verticalHeader().width(), self.table.horizontalHeader().height()
        return QPoint(pos.x() + left_margin, pos.y() + top_margin)

    @property
    def selected_row(self):
        current_selection = self.table.selectedIndexes()
        if current_selection:
            return current_selection[0].row()
        else:
            return None

    @property
    def selected_track(self):
        return self._track_at(self.selected_row)

    def _track_at(self, row):
        return self.table.model().trackAt(row) if row is not None else None

    def _signal_remove_track(self):
        if self.selected_track is not None:
            self.remove_track.emit(self.selected_track)

    def _signal_play_track(self):
        if self.selected_track is not None:
            self.play_track.emit(self.selected_track)

    def display(self, album):
        self.table.setModel(AlbumCompositionModel(album))
        for index, width in enumerate(self.COLUMNS_WIDTHS):
            self.table.horizontalHeader().resizeSection(index, width)
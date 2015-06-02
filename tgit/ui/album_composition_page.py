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
from enum import Enum

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView, QFrame, QAction, QMenu, QTableWidget, QTableWidgetItem
from tgit.album import Album, AlbumListener

from tgit.track import Track
from tgit.ui.album_composition_model import AlbumCompositionModel
from tgit.ui.helpers import form, formatting
from tgit.ui.observer import Observer

LIGHT_GRAY = QColor.fromRgb(0xDDDDDD)


@Observer
class AlbumCompositionPage(QWidget, AlbumListener):
    play_track = pyqtSignal(Track)
    remove_track = pyqtSignal(Track)
    move_track = pyqtSignal(Track, int)
    addTracks = pyqtSignal()

    HEADERS = ('Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration')
    # Using stylesheets on the table corrupts the display of the button widgets in the
    # cells, at least on OSX. So we have to style programmatically
    COLUMNS_WIDTHS = [345, 255, 255, 85, 85]

    _playing_track = None

    def __init__(self, album, player):
        super().__init__()

        self.subscribe(album.track_inserted, self._insert_track)
        self.subscribe(player.playing, self._on_playing_track)
        self.subscribe(player.stopped, self._on_stopped_track)

        # todo when we have proper signals on album, we can get rid of that
        album.addAlbumListener(self)

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
        self._table_view = self.makeTrackTableView()
        self._table = self.makeTrackTable()
        self._make_context_menu()
        layout.addWidget(self.makeTableFrame(self._table))
        layout.addWidget(self.makeTableFrame(self._table_view))
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
        table = QTableWidget()
        table.setFrameStyle(QFrame.NoFrame)
        table.setObjectName('track_list')
        table.setColumnCount(len(self.HEADERS))
        table.setHorizontalHeaderLabels([self.tr(header) for header in self.HEADERS])
        return table

    def _display_album(self, album):
        for index, track in enumerate(album.tracks):
            self._display_track(index, track)

    albumStateChanged = _display_album

    def _insert_track(self, index, track):
        self._table.insertRow(index)
        self._display_track(index, track)

    def _display_track(self, index, track):
        Row(index, track).display(self._table)

    def makeTrackTableView(self):
        table = QTableView()
        table.setFrameStyle(QFrame.NoFrame)
        table.setObjectName('track-list-view')
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
        self.move_track.emit(self._table_view.model().trackAt(from_), to)

    def _select_row(self, row):
        self._table_view.setCurrentIndex(self._table_view.model().index(row, 0))

    def _is_selected(self, track):
        return self.selected_track == track

    def _update_context_menu(self):
        play_action_text = "Stop" if self._is_selected(self._playing_track) else "Play"
        self._play_action.setText('{0} "{1}"'.format(self.tr(play_action_text), self.selected_track.track_title))
        self._play_action.setDisabled(self.selected_track.type == Album.Type.FLAC)

    def _make_context_menu(self):
        # We don't want the menu to block so we can't use the ActionsContextMenu policy
        self._table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._context_menu = QMenu(self._table_view)
        self._context_menu.setObjectName("context_menu")

        remove_action = QAction(self.tr("Remove"), self._table_view)
        remove_action.setObjectName("remove_action")
        remove_action.setShortcut(Qt.Key_Delete)
        remove_action.triggered.connect(lambda checked: self._signal_remove_track())
        self._context_menu.addAction(remove_action)
        self._table_view.addAction(remove_action)

        self._play_action = QAction(self._table_view)
        self._play_action.setObjectName("play_action")
        self._play_action.triggered.connect(lambda checked: self._signal_play_track())
        self._context_menu.addAction(self._play_action)
        self._table_view.addAction(self._play_action)

        self._table_view.customContextMenuRequested.connect(self._open_context_menu)

    def _open_context_menu(self, pos):
        if self.selected_row is not None:
            self._update_context_menu()
            self._context_menu.popup(self._map_to_global(pos))

    def _map_to_global(self, pos):
        return self._table_view.mapToGlobal(self._map_to_table(pos))

    def _map_to_table(self, pos):
        left_margin, top_margin = self._table_view.verticalHeader().width(), self._table_view.horizontalHeader().height()
        return QPoint(pos.x() + left_margin, pos.y() + top_margin)

    @property
    def selected_row(self):
        current_selection = self._table_view.selectedIndexes()
        if current_selection:
            return current_selection[0].row()
        else:
            return None

    @property
    def selected_track(self):
        return self._track_at(self.selected_row)

    def _track_at(self, row):
        return self._table_view.model().trackAt(row) if row is not None else None

    def _signal_remove_track(self):
        if self.selected_track is not None:
            self.remove_track.emit(self.selected_track)

    def _signal_play_track(self):
        if self.selected_track is not None:
            self.play_track.emit(self.selected_track)

    def display(self, album):
        self._table_view.setModel(AlbumCompositionModel(album))
        for index, width in enumerate(self.COLUMNS_WIDTHS):
            self._table_view.horizontalHeader().resizeSection(index, width)


class Columns(Enum):
    __LEFT_ALIGNED__ = Qt.AlignLeft | Qt.AlignVCenter
    __RIGHT_ALIGNED__ = Qt.AlignRight | Qt.AlignVCenter

    track_title = (lambda track: track.track_title, __LEFT_ALIGNED__)
    lead_performer = (lambda track: track.lead_performer, __LEFT_ALIGNED__)
    release_name = (lambda track: track.album.release_name, __LEFT_ALIGNED__)
    bitrate = (lambda track: "{0} kbps".format(formatting.in_kbps(track.bitrate)), __RIGHT_ALIGNED__)
    duration = (lambda track: formatting.to_duration(track.duration), __RIGHT_ALIGNED__)

    def __init__(self, value, alignement=__LEFT_ALIGNED__):
        self._value = value
        self._alignement = alignement

    def item(self, track):
        item = QTableWidgetItem(self._value(track))
        item.setTextAlignment(self._alignement)
        return item


class Row:
    def __init__(self, index, track):
        self.index = index
        self.track = track

    def display(self, table):
        for index, column in enumerate(Columns):
            table.setItem(self.index, index, column.item(self.track))
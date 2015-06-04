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
from tgit.ui.helpers import form, formatting
from tgit.ui.observer import Observer

STYLE_SHEET = """
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
        """

LIGHT_GRAY = QColor.fromRgb(0xDDDDDD)
HEADERS = ('Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration')
COLUMNS_WIDTHS = [345, 255, 255, 85, 65]


def make_album_composition_page(dialogs, player, album, *, on_remove_track, on_play_track, on_move_track):
    page = AlbumCompositionPage(album, player)
    page.add_tracks.connect(lambda: dialogs.add_tracks(album).open())
    page.move_track.connect(on_move_track)
    page.play_track.connect(on_play_track)
    page.remove_track.connect(on_remove_track)
    return page


@Observer
class AlbumCompositionPage(QWidget, AlbumListener):
    play_track = pyqtSignal(Track)
    remove_track = pyqtSignal(Track)
    move_track = pyqtSignal(Track, int)
    add_tracks = pyqtSignal()

    _track_currently_playing = None

    def __init__(self, album, player):
        super().__init__()

        self._tracks = []

        self.subscribe(album.track_inserted, self._insert_row)
        self.subscribe(album.track_removed, self._remove_row)
        self.subscribe(player.playing, lambda track: self._mark_playing_track(track))
        self.subscribe(player.stopped, lambda track: self._mark_playing_track(None))
        # todo when we have proper signals on album, we can get rid of that
        album.addAlbumListener(self)

        self.build()

    def build(self):
        self.setObjectName('album-composition-page')
        layout = form.column()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.make_header())
        self._table = self.make_track_table()
        self._context_menu = self._make_context_menu(self._table)
        layout.addWidget(self._make_table_frame(self._table))
        self.setLayout(layout)

    def make_header(self):
        header = QWidget()
        row = form.row()
        help = form.label()
        help.setText(self.tr("Organize the release's tracks."))
        row.addWidget(help)
        row.addStretch()
        addButton = form.button('add-tracks', self.tr('ADD'))
        addButton.clicked.connect(lambda pressed: self.add_tracks.emit())
        row.addWidget(addButton)
        header.setLayout(row)

        return header

    def make_track_table(self):
        table = QTableWidget()
        table.setFrameStyle(QFrame.NoFrame)
        table.setObjectName('track_list')
        table.setStyleSheet(STYLE_SHEET)
        table.setColumnCount(len(HEADERS))
        table.setHorizontalHeaderLabels([self.tr(header) for header in HEADERS])
        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionMode(QTableView.SingleSelection)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        for index, width in enumerate(COLUMNS_WIDTHS):
            table.horizontalHeader().resizeSection(index, width)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setSectionsMovable(True)
        table.verticalHeader().sectionMoved.connect(self._signal_move_track)
        table.verticalHeader().sectionMoved.connect(lambda _, from_, to: self._select_row(to))
        # We don't want the menu to block so we can't use the ActionsContextMenu policy
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self._open_context_menu)
        return table

    def _make_context_menu(self, table):
        context_menu = QMenu(table)
        context_menu.setObjectName("context_menu")

        remove_action = QAction(self.tr("Remove"), table)
        remove_action.setObjectName("remove_action")
        remove_action.setShortcut(Qt.Key_Delete)
        remove_action.triggered.connect(lambda checked: self._signal_remove_track())
        context_menu.addAction(remove_action)
        table.addAction(remove_action)

        self._play_action = QAction(table)
        self._play_action.setObjectName("play_action")
        self._play_action.triggered.connect(lambda checked: self._signal_play_track())
        context_menu.addAction(self._play_action)
        table.addAction(self._play_action)

        return context_menu

    def _make_table_frame(self, table):
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

    def _mark_playing_track(self, track):
        self._track_currently_playing = track

    def _select_row(self, row):
        self._table.selectRow(row)

    def _open_context_menu(self, pos):
        if self.selected_row is not None:
            self._update_context_menu()
            self._context_menu.popup(self._map_to_global(pos))

    def _update_context_menu(self):
        play_action_text = "Stop" if (self.selected_track == self._track_currently_playing) else "Play"
        self._play_action.setText('{0} "{1}"'.format(self.tr(play_action_text), self.selected_track.track_title))
        self._play_action.setDisabled(self.selected_track.type == Album.Type.FLAC)

    def _map_to_global(self, pos):
        return self._table.mapToGlobal(self._map_to_table(pos))

    def _map_to_table(self, pos):
        left_margin, top_margin = self._table.verticalHeader().width(), self._table.horizontalHeader().height()
        return QPoint(pos.x() + left_margin, pos.y() + top_margin)

    @property
    def selected_row(self):
        current_selection = self._table.selectedIndexes()
        if current_selection:
            return current_selection[0].row()
        else:
            return None

    @property
    def selected_track(self):
        return self._tracks[self.selected_row]

    def _signal_remove_track(self):
        if self.selected_track:
            self.remove_track.emit(self.selected_track)

    def _signal_play_track(self):
        if self.selected_track:
            self.play_track.emit(self.selected_track)

    def _signal_move_track(self, _, from_, to):
        self.move_track.emit(self._tracks[from_], to)

    def _update_all_rows(self, _):
        for index in range(len(self._tracks)):
            self._update_row(row=index)

    def _insert_row(self, at_index, track):
        self._tracks.insert(at_index, track)
        self._table.insertRow(at_index)
        self._update_row(at_index)
        self.subscribe(track.metadata_changed, lambda state: self._update_track(track))

    def _remove_row(self, at_index, track):
        self.unsubscribe(track.metadata_changed)
        self._table.removeRow(at_index)
        self._tracks.pop(at_index)

    def _update_track(self, track):
        self._update_row(row=self._tracks.index(track))

    def _update_row(self, row):
        for index, column in enumerate(Columns):
            self._table.setItem(row, index, column.item(self._tracks[row]))

    albumStateChanged = _update_all_rows


class Columns(Enum):
    __LEFT_ALIGNED__ = Qt.AlignLeft | Qt.AlignVCenter
    __RIGHT_ALIGNED__ = Qt.AlignRight | Qt.AlignVCenter

    track_title = (lambda track: track.track_title, __LEFT_ALIGNED__)
    lead_performer = (lambda track: track.lead_performer, __LEFT_ALIGNED__)
    release_name = (lambda track: track.album.release_name, __LEFT_ALIGNED__)
    bitrate = (lambda track: "{0} kbps".format(formatting.in_kbps(track.bitrate)), __RIGHT_ALIGNED__)
    duration = (lambda track: formatting.to_duration(track.duration), __RIGHT_ALIGNED__)

    def __init__(self, value, alignment=__LEFT_ALIGNED__):
        self._value = value
        self._alignment = alignment

    def item(self, track):
        item = QTableWidgetItem(self._value(track))
        item.setTextAlignment(self._alignment)
        return item

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

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QWidget, QHeaderView, QMenu, QTableWidgetItem

from tgit.album import AlbumListener
from tgit.ui.track_list_table_model import Column, TrackItem
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.observer import Observer
from tgit.ui.event_filters import MovableSectionsCursor

VERTICAL_HEADER_WIDTH = 18


def ignore():
    pass


@Observer
class TrackListPage(QWidget, UIFile, AlbumListener):
    _playing_track = None

    def __init__(self, album, player, select_tracks, **request_handlers):
        super().__init__()
        self._items = []
        self._player = player
        self._select_tracks = select_tracks

        self._setup_ui()
        self._listen_to(album, player)
        self._register_request_handlers(request_handlers)
        self._display_album(album)

    def _setup_ui(self):
        self._load(":/ui/track_list_page.ui")
        self._react_to_table_events(self._track_table)
        self._make_context_menu(self._track_table)
        self._setup_horizontal_header(self._track_table.horizontalHeader())
        self._setup_vertical_header(self._track_table.verticalHeader())

    def _listen_to(self, album, player):
        self.subscribe(album.track_inserted, self._insert_item)
        self.subscribe(album.track_removed, lambda index, _: self._remove_item(index))
        self.subscribe(player.playing, lambda track: self.playback_started(track))
        self.subscribe(player.stopped, lambda track: self.playback_stopped(track))
        # todo when we have proper signals on album, we can get rid of that
        album.addAlbumListener(self)

    def _register_request_handlers(self, handlers):
        for name, handler in handlers.items():
            getattr(self, name)(handler)

    def on_add_tracks(self, add):
        self._add_tracks_button.clicked.connect(lambda: self._select_tracks(add))

    def on_move_track(self, move):
        # todo should we pass the index instead of the track?
        move_track = lambda _, from_position, to_position: move(self._items[from_position].track, to_position)
        self._track_table.verticalHeader().sectionMoved.connect(move_track)

    def on_play_track(self, play):
        self._play_action.triggered.connect(lambda: play(self._selected_item.track))

    def on_stop_track(self, stop):
        self._stop_action.triggered.connect(lambda: stop())
        self._remove_action.triggered.connect(lambda: stop() if self._selected_item.is_playing else ignore())

    def on_remove_track(self, remove):
        # todo should we pass the index instead of the track?
        self._remove_action.triggered.connect(lambda: remove(self._selected_item.track))

    def _display_album(self, album):
        for index in range(self._item_count()):
            self._remove_item(index)

        for index, track in enumerate(album.tracks):
            self._insert_item(index, track)

    def albumStateChanged(self, state):
        for item in self._items:
            self._update_item(item)

    def _react_to_table_events(self, table):
        table.customContextMenuRequested.connect(self._open_context_menu)
        table.itemSelectionChanged.connect(self._update_actions)

    def _make_context_menu(self, table):
        self._context_menu = QMenu(table)
        self._context_menu.setObjectName("context_menu")
        self._context_menu.addAction(self._remove_action)
        self._remove_action.setShortcuts([QKeySequence.Delete, QKeySequence(Qt.Key_Backspace)])
        table.addAction(self._remove_action)
        self._context_menu.addAction(self._play_action)
        table.addAction(self._play_action)
        self._context_menu.addAction(self._stop_action)
        table.addAction(self._stop_action)

    def _setup_horizontal_header(self, header):
        for col in range(Column.count()):
            header.resizeSection(col, Column.at(col).width)
            header.setSectionResizeMode(col, Column.at(col).resize_mode)

    def _setup_vertical_header(self, header):
        header.setSectionResizeMode(QHeaderView.Fixed)
        header.setMinimumWidth(VERTICAL_HEADER_WIDTH)
        header.setSectionsMovable(True)
        self._cursor = MovableSectionsCursor.install(header)

    def _open_context_menu(self, pos):
        if self._track_table.indexAt(pos).isValid():
            self._context_menu.popup(self._screen_coordinates(pos))

    def _screen_coordinates(self, table_pos):
        return self._track_table.mapToGlobal(self._table_coordinates(table_pos))

    def _table_coordinates(self, table_pos):
        left_header_width = self._track_table.verticalHeader().width()
        top_header_height = self._track_table.horizontalHeader().height()
        return QPoint(table_pos.x() + left_header_width, table_pos.y() + top_header_height)

    def playback_started(self, track):
        item = self._item_for(track)
        item.mark_playing()
        self._update_actions()
        self._update_item(item)

    def playback_stopped(self, track):
        item = self._item_for(track)
        item.mark_stopped()
        self._update_actions()
        self._update_item(item)

    def _update_actions(self):
        if self._selected_item:
            self._remove_action.setEnabled(True)
            self._play_action.setVisible(self._selected_item.is_stopped)
            self._play_action.setEnabled(self._selected_item.is_mp3)
            self._play_action.setText('{0} "{1}"'.format(self.tr("Play"), self._selected_item.track_title))
            self._stop_action.setVisible(self._selected_item.is_playing)
            self._stop_action.setEnabled(self._selected_item.is_mp3)
            self._stop_action.setText('{0} "{1}"'.format(self.tr("Stop"), self._selected_item.track_title))
        else:
            self._remove_action.setEnabled(False)
            self._play_action.setEnabled(False)
            self._stop_action.setEnabled(False)

    def _item_count(self):
        return len(self._items)

    def _item_for(self, track):
        return next(item for item in self._items if item.track == track)

    def _index_of(self, item):
        return self._items.index(item)

    @property
    def _selected_item(self):
        try:
            selected_row = next(item.row() for item in self._track_table.selectedItems())
            return self._items[selected_row]
        except StopIteration:
            return None

    def _insert_item(self, at_index, track):
        item = self._make_item(track)
        self._items.insert(at_index, item)
        self._track_table.insertRow(at_index)
        self._refresh_row(at_index)
        self.subscribe(item.changed, lambda state: self._update_item(item))

    def _make_item(self, track):
        item = TrackItem(track)
        if self._player.is_playing(track):
            item.mark_playing()
        return item

    def _remove_item(self, at_index):
        self.unsubscribe(self._items[at_index].changed)
        self._track_table.removeRow(at_index)
        self._items.pop(at_index)

    def _update_item(self, item):
        self._refresh_row(self._index_of(item))

    def _refresh_row(self, row):
        self._track_table.setVerticalHeaderItem(row, self._header_item())
        for col in range(Column.count()):
            self._track_table.setItem(row, col, self._cell_item_at(row, col))

    def _cell_item_at(self, row, col):
        return Column.at(col).value(self._items[row])

    def _header_item(self):
        return QTableWidgetItem(QIcon(":/images/drag-handle.gif"), None)

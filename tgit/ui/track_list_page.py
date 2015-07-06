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

from PyQt5.QtCore import Qt, QPoint, QObject, QEvent
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QWidget, QHeaderView, QMenu, QTableWidgetItem

from tgit.album import Album, AlbumListener
from tgit.ui.helpers import formatting, ui_file
from tgit.ui.observer import Observer

VERTICAL_HEADER_WIDTH = 18
COLUMNS_WIDTHS = [30, 300, 245, 270, 90, 70]


@Observer
class TrackListPage(QWidget, AlbumListener):
    _playing_track = None

    def __init__(self, album, player, select_tracks, **handlers):
        super().__init__()
        self._tracks = []
        self._select_tracks = select_tracks
        self._setup_ui()
        self._subscribe_to_events(album, player)
        self._register_handlers(handlers)
        self._display_album(album)

    def _register_handlers(self, handlers):
        for name, handler in handlers.items():
            getattr(self, name)(handler)

    def on_add_tracks(self, handler):
        self._add_tracks_button.clicked.connect(lambda pressed: self._select_tracks(handler))

    def on_move_track(self, handler):
        self._track_table.verticalHeader().sectionMoved.connect(lambda _, from_, to: handler(self._tracks[from_], to))

    def on_play_track(self, handler):
        self._play_action.triggered.connect(lambda pressed: handler(self.selected_track))

    def on_remove_track(self, handler):
        self._remove_action.triggered.connect(lambda checked: handler(self.selected_track))

    def _subscribe_to_events(self, album, player):
        self.subscribe(album.track_inserted, self._insert_row)
        self.subscribe(album.track_removed, self._remove_row)
        self.subscribe(player.playing, lambda track: self._update_playing_track(track))
        self.subscribe(player.stopped, lambda track: self._update_playing_track(None))
        # todo when we have proper signals on album, we can get rid of that
        album.addAlbumListener(self)

    def _setup_ui(self):
        ui_file.load(":/ui/track_list_page.ui", self)
        self._track_table.itemSelectionChanged.connect(self._update_actions)
        self._drag_and_drop_cursor = self._make_drag_and_drop_cursor(self._track_table)
        self._context_menu = self._make_context_menu(self._track_table)
        self._resize_columns(self._track_table)
        self._setup_vertical_header(self._track_table)

    def _make_drag_and_drop_cursor(self, table):
        cursor = DragAndDropCursor(table)
        table.verticalHeader().setMouseTracking(True)
        table.verticalHeader().viewport().installEventFilter(cursor)
        return cursor

    def _setup_vertical_header(self, table):
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.verticalHeader().setSectionsMovable(True)
        table.verticalHeader().setMinimumWidth(VERTICAL_HEADER_WIDTH)

    def _resize_columns(self, table):
        for index, width in enumerate(COLUMNS_WIDTHS):
            table.horizontalHeader().resizeSection(index, width)

    def _make_context_menu(self, table):
        table.customContextMenuRequested.connect(self._open_context_menu)
        context_menu = QMenu(self._track_table)
        context_menu.setObjectName("context_menu")
        context_menu.addAction(self._remove_action)
        self._remove_action.setDisabled(True)
        self._remove_action.setShortcuts([QKeySequence.Delete, QKeySequence(Qt.Key_Backspace)])
        table.addAction(self._remove_action)
        context_menu.addAction(self._play_action)
        self._play_action.setDisabled(True)
        table.addAction(self._play_action)
        return context_menu

    def _open_context_menu(self, pos):
        if self._track_table.indexAt(pos).isValid():
            self._context_menu.popup(self._map_to_global(pos))

    def _map_to_global(self, pos):
        return self._track_table.mapToGlobal(self._map_to_table(pos))

    def _update_playing_track(self, playing_track):
        self._playing_track = playing_track
        self._update_actions()
        self._update_all_rows()

    def _map_to_table(self, pos):
        vertical_header_width = self._track_table.verticalHeader().width()
        horizontal_header_height = self._track_table.horizontalHeader().height()
        return QPoint(pos.x() + vertical_header_width, pos.y() + horizontal_header_height)

    def _is_playing(self, track):
        return self._playing_track == track

    def _update_actions(self):
        self._remove_action.setEnabled(self.selected_track is not None)
        self._play_action.setEnabled(self.selected_track is not None and self.selected_track.type == Album.Type.MP3)
        if self.selected_track is not None:
            play_action_text = "Stop" if self._is_playing(self.selected_track) else "Play"
            self._play_action.setText('{0} "{1}"'.format(self.tr(play_action_text), self.selected_track.track_title))

    @property
    def _selected_row(self):
        selection = self._track_table.selectedIndexes()
        return selection[0].row() if selection else None

    @property
    def selected_track(self):
        return self._tracks[self._selected_row] if self._selected_row is not None else None

    def _display_album(self, album):
        for index, track in enumerate(self._tracks):
            self._remove_row(index, track)

        for index, track in enumerate(album.tracks):
            self._insert_row(index, track)

    def _update_all_rows(self, _=None):
        for index in range(len(self._tracks)):
            self._update_row(row_index=index)

    def _insert_row(self, at_index, track):
        self._tracks.insert(at_index, track)
        self._track_table.insertRow(at_index)
        self._update_row(at_index)
        self.subscribe(track.metadata_changed, lambda state: self._update_track(track))

    def _remove_row(self, at_index, track):
        self.unsubscribe(track.metadata_changed)
        self._track_table.removeRow(at_index)
        self._tracks.pop(at_index)

    def _update_track(self, track):
        self._update_row(row_index=self._tracks.index(track))

    def _update_row(self, row_index):
        track = self._tracks[row_index]
        header_item = QTableWidgetItem()
        header_item.setIcon(QIcon(":/images/volume-up-16.png") if self._is_playing(track)
                            else QIcon(":/images/drag-handle.gif"))
        self._track_table.setVerticalHeaderItem(row_index, header_item)

        for col_index, column in enumerate(Columns):
            self._track_table.setItem(row_index, col_index, column.item(track))

    albumStateChanged = _update_all_rows


class Columns(Enum):
    __LEFT_ALIGNED__ = Qt.AlignLeft | Qt.AlignVCenter
    __RIGHT_ALIGNED__ = Qt.AlignRight | Qt.AlignVCenter

    track_number = (lambda track: str(track.track_number), __RIGHT_ALIGNED__)
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


class DragAndDropCursor(QObject):
    REGULAR_CURSOR = Qt.ArrowCursor
    DRAGGABLE_CURSOR = Qt.OpenHandCursor
    DRAGGING_CURSOR = Qt.ClosedHandCursor

    _mouse_pressed = False

    def __init__(self, table):
        super().__init__()
        self._table = table

    def _header_height(self):
        return sum(map(self._table.rowHeight, range(self._table.rowCount())))

    def _within_bounds(self, pos):
        return 0 < pos.y() <= self._header_height()

    def eventFilter(self, target, event):
        if event.type() == QEvent.Leave:
            self._table.setCursor(self.REGULAR_CURSOR)
        if event.type() == QEvent.MouseButtonPress:
            self._mouse_pressed = True
            self._table.setCursor(self.DRAGGING_CURSOR)
        if event.type() == QEvent.MouseButtonRelease:
            self._mouse_pressed = False
            self._table.setCursor(self.DRAGGABLE_CURSOR if self._within_bounds(event.pos()) else self.REGULAR_CURSOR)
        if event.type() == QEvent.MouseMove:
            self._table.setCursor(self.DRAGGING_CURSOR if self._mouse_pressed
                                  else self.DRAGGABLE_CURSOR if self._within_bounds(event.pos())
            else self.REGULAR_CURSOR)

        return super().eventFilter(target, event)
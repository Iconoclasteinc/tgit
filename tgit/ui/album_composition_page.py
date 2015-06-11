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

from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QObject, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHeaderView, QMenu, QTableWidgetItem

from tgit.album import Album, AlbumListener
from tgit.track import Track
from tgit.ui.helpers import formatting, ui_file
from tgit.ui.observer import Observer


COLUMNS_WIDTHS = [30, 300, 245, 270, 90, 70]


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

    _playing_track = None

    def __init__(self, album, player):
        super().__init__()
        self._setup_ui()
        self._subscribe_to_events(album, player)
        self._tracks = []

    def _subscribe_to_events(self, album, player):
        self.subscribe(album.track_inserted, self._insert_row)
        self.subscribe(album.track_removed, self._remove_row)
        self.subscribe(player.playing, lambda track: self._update_playing_track(track))
        self.subscribe(player.stopped, lambda track: self._update_playing_track(None))
        # todo when we have proper signals on album, we can get rid of that
        album.addAlbumListener(self)

    def _setup_ui(self):
        ui_file.load(":/ui/album_composition_page.ui", self)
        self._add_tracks_button.clicked.connect(lambda pressed: self.add_tracks.emit())
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
        table.verticalHeader().sectionMoved.connect(self._signal_move_track)
        table.verticalHeader().sectionMoved.connect(lambda _, from_, to: self._select_row(to))
        table.verticalHeader().setMinimumWidth(18)

    def _resize_columns(self, table):
        for index, width in enumerate(COLUMNS_WIDTHS):
            table.horizontalHeader().resizeSection(index, width)

    def _make_context_menu(self, table):
        table.customContextMenuRequested.connect(self._open_context_menu)
        context_menu = QMenu(self._track_table)
        context_menu.setObjectName("context_menu")
        self._remove_action.triggered.connect(lambda checked: self._signal_remove_track())
        context_menu.addAction(self._remove_action)
        table.addAction(self._remove_action)
        self._play_action.triggered.connect(lambda checked: self._signal_play_track())
        context_menu.addAction(self._play_action)
        table.addAction(self._play_action)
        return context_menu

    def _update_playing_track(self, playing_track):
        self._playing_track = playing_track
        self._update_all_rows()

    def _select_row(self, row):
        self._track_table.selectRow(row)

    def _open_context_menu(self, pos):
        if self.selected_row is not None:
            self._update_context_menu()
            self._context_menu.popup(self._map_to_global(pos))

    def _is_playing(self, track):
        return self._playing_track == track

    def _update_context_menu(self):
        play_action_text = "Stop" if self._is_playing(self.selected_track) else "Play"
        self._play_action.setText('{0} "{1}"'.format(self.tr(play_action_text), self.selected_track.track_title))
        self._play_action.setDisabled(self.selected_track.type == Album.Type.FLAC)

    def _map_to_global(self, pos):
        return self._track_table.mapToGlobal(self._map_to_table(pos))

    def _map_to_table(self, pos):
        vertical_header_width = self._track_table.verticalHeader().width()
        horizontal_header_height = self._track_table.horizontalHeader().height()
        return QPoint(pos.x() + vertical_header_width, pos.y() + horizontal_header_height)

    @property
    def selected_row(self):
        current_selection = self._track_table.selectedIndexes()
        return current_selection[0].row() if current_selection else None

    @property
    def selected_track(self):
        return self._tracks[self.selected_row] if self.selected_row is not None else None

    def _signal_remove_track(self):
        if self.selected_track:
            self.remove_track.emit(self.selected_track)

    def _signal_play_track(self):
        if self.selected_track:
            self.play_track.emit(self.selected_track)

    def _signal_move_track(self, _, from_, to):
        self.move_track.emit(self._tracks[from_], to)

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
        header_item.setIcon(QIcon(":/images/volume-up.png") if self._is_playing(track)
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

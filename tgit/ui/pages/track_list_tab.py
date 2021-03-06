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

from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QWidget, QHeaderView, QMenu, QTableWidgetItem, QApplication

from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.event_filters import MovableSectionsCursor
from tgit.ui.helpers.ui_file import UIFile
from tgit.ui.observer import Observer
from tgit.ui.pages.track_list_table_model import Column, RowItem


def make_track_list_tab(project, player, select_tracks, **handlers):
    page = TrackListTab(select_tracks)
    page.display(project)

    for name, handler in handlers.items():
        getattr(page, name)(handler)

    subscriptions = MultiSubscription()
    subscriptions += project.metadata_changed.subscribe(page.album_metadata_changed)
    subscriptions += project.track_inserted.subscribe(page.track_added)
    subscriptions += project.track_removed.subscribe(page.track_removed)
    subscriptions += project.track_moved.subscribe(lambda _, from_, to: page.track_moved(from_, to))
    subscriptions += player.playing.subscribe(page.playback_started)
    subscriptions += player.stopped.subscribe(page.playback_stopped)
    subscriptions += player.error_occurred.subscribe(page.playback_error)
    page.closed.connect(lambda: subscriptions.cancel())

    return page


VERTICAL_HEADER_WIDTH = 24


@Closeable
@Observer
class TrackListTab(QWidget, UIFile):
    closed = pyqtSignal()

    def __init__(self, select_tracks):
        super().__init__()
        self._items = []
        self._select_tracks = select_tracks
        self._setup_ui()

    def on_add_tracks(self, add):
        self._add_tracks_button.clicked.connect(lambda: self._select_tracks(add))

    def on_move_track(self, move):
        def move_track(_, from_position, to_position):
            move(from_position, to_position)

        self._track_table.verticalHeader().sectionMoved.connect(move_track)
        self._move_up_action.triggered.connect(lambda checked: move(self._selected_row, self._selected_row - 1))
        self._move_down_action.triggered.connect(lambda checked: move(self._selected_row, self._selected_row + 1))

    def on_play_track(self, play):
        self._play_action.triggered.connect(lambda: play(self._selected_item.track))

    def on_stop_track(self, stop):
        self._stop_action.triggered.connect(lambda: stop())

    def on_remove_track(self, remove):
        self._remove_action.triggered.connect(lambda: remove(self._selected_row))

    def _setup_ui(self):
        self._load(":/ui/track_list_tab.ui")
        self._react_to_table_events(self._track_table)
        self._react_to_focus_events()
        self._make_context_menu(self._track_table)
        self._setup_horizontal_header(self._track_table.horizontalHeader())
        self._setup_vertical_header(self._track_table.verticalHeader())
        self._remove_action.triggered.connect(self._stop_selected_track)
        self._remove_action.changed.connect(
            lambda: self._remove_track_button.setEnabled(self._remove_action.isEnabled()))
        self._move_up_action.changed.connect(
            lambda: self._move_track_up_button.setEnabled(self._move_up_action.isEnabled()))
        self._move_down_action.changed.connect(
            lambda: self._move_track_down_button.setEnabled(self._move_down_action.isEnabled()))

    def display(self, album):
        for index, track in enumerate(album.tracks):
            self.track_added(index, track)

    def _stop_selected_track(self):
        if self._selected_item.is_playing:
            self._stop_action.trigger()

    def _react_to_table_events(self, table):
        table.customContextMenuRequested.connect(self._open_context_menu)
        table.selectionModel().currentRowChanged.connect(self._current_row_changed)
        table.itemSelectionChanged.connect(self._update_actions)

    def _react_to_focus_events(self):
        # todo we need to be more specific on which focus events we're interested in
        # by installing an event filter on the table widget
        QApplication.instance().focusObjectChanged.connect(self._focus_changed)

    def _focus_changed(self):
        if self._selected_item is not None:
            self._selected_item.active = self._track_table.hasFocus()
            self._item_changed(self._selected_item)

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

    @staticmethod
    def _setup_horizontal_header(header):
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
        self._item_changed(item)
        self._update_actions()

    def playback_stopped(self, track):
        item = self._item_for(track)
        item.mark_stopped()
        self._item_changed(item)
        self._update_actions()

    def playback_error(self, track, error):
        item = self._item_for(track)
        item.mark_error(error)
        self._item_changed(item)
        self._update_actions()

    def _update_actions(self):
        if self._selected_item:
            self._play_action.setVisible(not self._selected_item.is_playing)
            self._play_action.setText('{0} "{1}"'.format(self.tr("Play"), self._selected_item.track_title))
            self._stop_action.setVisible(self._selected_item.is_playing)
            self._stop_action.setText('{0} "{1}"'.format(self.tr("Stop"), self._selected_item.track_title))

        self._remove_action.setEnabled(self._selected_item is not None)
        self._move_up_action.setEnabled(self._selected_item is not None and self._selected_row > 0)
        self._move_down_action.setEnabled(self._selected_item is not None and self._selected_row < self._item_count - 1)
        self._play_action.setEnabled(self._selected_item is not None)
        self._stop_action.setEnabled(self._selected_item is not None)

    def _current_row_changed(self, current, previous):
        if previous.isValid():
            self._items[previous.row()].selected = False
            self._item_changed(self._items[previous.row()])

        if current.isValid():
            self._items[current.row()].selected = True
            self._item_changed(self._items[current.row()])

    @property
    def _item_count(self):
        return len(self._items)

    def _item_for(self, track):
        return next(item for item in self._items if item.track == track)

    def _index_of(self, item):
        return self._items.index(item)

    @property
    def _selected_row(self):
        try:
            return next(item.row() for item in self._track_table.selectedItems())
        except StopIteration:
            return None

    @property
    def _selected_item(self):
        selected_row = self._selected_row
        if selected_row is None:
            return None
        else:
            return self._items[selected_row]

    def track_added(self, at_index, track):
        item = RowItem(track)
        self._items.insert(at_index, item)
        self._track_table.insertRow(at_index)
        self._refresh_row(at_index)
        self.subscribe(track.metadata_changed, lambda _: self._item_changed(item))

    def track_removed(self, at_index, track):
        self.unsubscribe(track.metadata_changed)
        self._track_table.removeRow(at_index)
        del self._items[at_index]

    def track_moved(self, from_index, to_index):
        self._track_table.removeRow(from_index)
        item = self._items.pop(from_index)
        self._items.insert(to_index, item)
        self._track_table.insertRow(to_index)
        self._refresh_row(to_index)
        self._track_table.selectRow(to_index)

    def album_metadata_changed(self, *_):
        for item in self._items:
            self._item_changed(item)

    def _item_changed(self, item):
        self._refresh_row(self._index_of(item))

    def _refresh_row(self, row_index):
        self._track_table.setVerticalHeaderItem(row_index, self._header_item())
        for col_index in range(Column.count()):
            self._track_table.setItem(row_index, col_index, self._cell_item_at(row_index, col_index))

    def _cell_item_at(self, row_index, col_index):
        return Column.at(col_index).value(self._items[row_index])

    @staticmethod
    def _header_item():
        return QTableWidgetItem(QIcon(":/icons/reorder"), None)

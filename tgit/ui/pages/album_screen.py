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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from tgit.album import AlbumListener
from tgit.signal import MultiSubscription
from tgit.ui.closeable import Closeable
from tgit.ui.helpers.ui_file import UIFile


def make_album_screen(album, track_list_page, album_page, track_page):
    screen = AlbumScreen(track_list_page, album_page, track_page)

    album.addAlbumListener(screen)
    subscriptions = MultiSubscription()
    subscriptions.add(album.track_inserted.subscribe(screen.track_added))
    subscriptions.add(album.track_removed.subscribe(lambda position, track: screen.track_removed(position)))
    subscriptions.add(album.track_moved.subscribe(lambda track, from_, to: screen.track_moved(from_, to)))
    screen.closed.connect(lambda: subscriptions.cancel())
    screen.closed.connect(lambda: album.removeAlbumListener(screen))
    screen.display(album)
    return screen


@Closeable
class AlbumScreen(QWidget, UIFile, AlbumListener):
    closed = pyqtSignal()

    _TRACK_LIST_PAGE_INDEX, _ALBUM_PAGE_INDEX, _TRACK_PAGES_STARTING_INDEX = range(3)

    def __init__(self, list_tracks, edit_album, edit_track):
        super().__init__()
        self._list_tracks = list_tracks
        self._edit_album = edit_album
        self._edit_track = edit_track
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/album_screen.ui")
        self._pages.currentChanged.connect(self._update_navigation_controls)
        self._previous.clicked.connect(self._to_previous_page)
        self._next.clicked.connect(self._to_next_page)
        self._pages_navigation.currentIndexChanged.connect(
            lambda index: self._to_page(self._pages_navigation.itemData(index)))

    def display(self, album):
        self._remove_all_pages()
        self._add_track_list_page(album)
        self._add_album_page(album)

        self._pages_navigation.addItem(self.tr("Track list"), self._TRACK_LIST_PAGE_INDEX)
        self._pages_navigation.addItem(self.tr("Project edition"), self._ALBUM_PAGE_INDEX)
        for index, track in enumerate(album.tracks):
            self.track_added(index, track)

    def _add_track_list_page(self, album):
        self._insert_page(self._list_tracks(album), self._TRACK_LIST_PAGE_INDEX)

    def _add_album_page(self, album):
        self._insert_page(self._edit_album(album), self._ALBUM_PAGE_INDEX)

    def track_added(self, index, track):
        self._insert_page(self._edit_track(track), self._track_page_index(index))
        self._pages_navigation.addItem("{} - {}".format(index + 1, track.track_title),
                                       self._TRACK_PAGES_STARTING_INDEX + index)

    def track_removed(self, index):
        self._remove_page(self._track_page_index(index))

    def track_moved(self, from_index, to_index):
        page = self._pages.widget(self._track_page_index(from_index))
        self._pages.removeWidget(page)
        self._pages.insertWidget(self._track_page_index(to_index), page)
        self._update_navigation_controls()

    def to_project_edition_page(self):
        self._to_page(self._ALBUM_PAGE_INDEX)

    def to_track_list_page(self):
        self._to_page(self._TRACK_LIST_PAGE_INDEX)

    def to_track_page(self, index):
        self._to_page(self._track_page_index(index))

    def _track_page_index(self, from_position):
        return self._TRACK_PAGES_STARTING_INDEX + from_position

    def _update_navigation_controls(self):
        self._previous.setDisabled(self._on_first_page())
        self._next.setDisabled(self._on_last_page())

    def _on_last_page(self):
        return self._on_page(self._page_count - 1)

    def _on_first_page(self):
        return self._on_page(0)

    def _on_page(self, number):
        return self.current_page == number

    def _insert_page(self, widget, position):
        self._pages.insertWidget(position, widget)
        self._update_navigation_controls()

    def _remove_page(self, number):
        page = self._pages.widget(number)
        self._pages.removeWidget(page)
        page.setParent(None)
        page.close()
        self._update_navigation_controls()

    @property
    def current_page(self):
        return self._pages.currentIndex()

    @property
    def _page_count(self):
        return self._pages.count()

    def _to_previous_page(self):
        self._to_page(self.current_page - 1)

    def _to_next_page(self):
        self._to_page(self.current_page + 1)

    def _to_page(self, number):
        self._pages.setCurrentIndex(number)
        self._pages_navigation.setCurrentIndex(number)

    def close(self):
        self._remove_all_pages()
        return True

    def _remove_all_pages(self):
        for index in reversed(range(self._page_count)):
            self._remove_page(index)

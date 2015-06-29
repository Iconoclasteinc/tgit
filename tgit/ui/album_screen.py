
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

from PyQt5.QtWidgets import QWidget

from tgit.album import AlbumListener
from tgit.ui.helpers import ui_file


def album_screen(composition_page, album_page, track_page, album):
    page = AlbumScreen(composition_page(album), album_page(album), track_page)
    #todo make album screen accept the album as a constructor parameter
    album.addAlbumListener(page)
    for index, track in enumerate(album.tracks):
        page.trackAdded(track, index)
    return page


class AlbumScreen(QWidget, AlbumListener):
    ALBUM_COMPOSITION_PAGE_INDEX = 0
    ALBUM_EDITION_PAGE_INDEX = 1
    TRACK_PAGES_INDEX = 2

    def __init__(self, compose_album, edit_album, edit_track):
        super().__init__()
        ui_file.load(":/ui/album_screen.ui", self)

        self.pages.currentChanged.connect(self._update_controls)
        self.previous.clicked.connect(self._to_previous_page)
        self.next.clicked.connect(self._to_next_page)

        self.pages.addWidget(compose_album)
        self.pages.addWidget(edit_album)
        self._update_controls()

        self.editTrack = edit_track

    def trackAdded(self, track, position):
        self._add_track_edition_page(self.editTrack(track), position)

    def trackRemoved(self, track, position):
        self._remove_track_edition_page(position)

    def show_album_edition_page(self):
        self._to_page(self.ALBUM_EDITION_PAGE_INDEX)

    def show_album_composition_page(self):
        self._to_page(self.ALBUM_COMPOSITION_PAGE_INDEX)

    def show_track_page(self, track_number):
        self._to_page(self.TRACK_PAGES_INDEX + (track_number - 1))

    def _has_track_page(self):
        return self.total_pages > self.TRACK_PAGES_INDEX

    def _update_controls(self):
        self.previous.setDisabled(self._on_first_page())
        self.next.setDisabled(self._on_last_page())

    def _on_last_page(self):
        return self._on_page(self.total_pages - 1)

    def _on_first_page(self):
        return self._on_page(0)

    def _on_page(self, number):
        return self.current_page == number

    def _add_track_edition_page(self, page, position):
        self._insert_page(page, self.TRACK_PAGES_INDEX + position)

    def _remove_track_edition_page(self, position):
        self._remove_page(self.TRACK_PAGES_INDEX + position)

    def _insert_page(self, widget, position):
        self.pages.insertWidget(position, widget)
        self._update_controls()

    def _remove_page(self, number):
        page = self.pages.widget(number)
        self.pages.removeWidget(page)
        page.setParent(None)
        page.close()
        self._update_controls()

    @property
    def current_page(self):
        return self.pages.currentIndex()

    @property
    def total_pages(self):
        return self.pages.count()

    def _to_previous_page(self):
        self._to_page(self.current_page - 1)

    def _to_next_page(self):
        self._to_page(self.current_page + 1)

    def _to_page(self, number):
        self.pages.setCurrentIndex(number)

    def close(self):
        for index in reversed(range(self.total_pages)):
            self._remove_page(index)

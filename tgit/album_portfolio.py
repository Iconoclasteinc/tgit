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
from tgit.album import Album

from tgit.signal import signal, Observable


class AlbumPortfolioListener(object):
    def albumCreated(self, album):
        pass


class AlbumPortfolio(metaclass=Observable):
    album_created = signal(Album)
    album_removed = signal(Album)

    def __init__(self):
        self._albums = []

    def add_album(self, album):
        self._albums.append(album)
        self.album_created.emit(album)

    def remove_album(self, album):
        self._albums.remove(album)
        self.album_removed.emit(album)

    def __getitem__(self, index):
        return self._albums[index]
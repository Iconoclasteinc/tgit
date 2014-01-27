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
from tgit.announcer import Announcer
from tgit.ui.views import albumCompositionPage

from tgit.ui.views.album_composition_model import AlbumCompositionModel


class AlbumComposer(object):
    def __init__(self, album, player):
        self._album = AlbumCompositionModel(album, player)
        self._player = player
        self._announce = Announcer()
        self._page = albumCompositionPage(self)

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def render(self):
        return self._page.render(self._album)

    def addTracksToAlbum(self):
        self._announce.addTracksToAlbum()

    def moveTrack(self, fromPosition, toPosition):
        self._album.move(fromPosition, toPosition)

    def playTrack(self, track):
        if track.playing():
            track.stop(self._player)
        else:
            track.play(self._player)

    def removeTrack(self, track):
        if track.playing():
            track.stop(self._player)

        track.remove()

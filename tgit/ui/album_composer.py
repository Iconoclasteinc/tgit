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

from tgit.ui.views.album_composition_model import AlbumCompositionModel


class AlbumComposer(object):
    def __init__(self, album, player, page):
        self._album = AlbumCompositionModel(album, player)
        self._player = player
        self._page = page

        self._bindEventHandlers()

    def _bindEventHandlers(self):
        self._page.bind(trackMoved=self.moveTrack, play=self.playTrack, remove=self.removeTrack)

    def render(self):
        self._page.display(self._album)
        return self._page

    def onAddTracks(self, handler):
        self._page.bind(add=handler)

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

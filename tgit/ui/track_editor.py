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

from tgit.album import AlbumListener
from tgit.track import TrackListener


class TrackEditor(AlbumListener, TrackListener):
    # todo when track records its track number (including total tracks in album)
    # we won't be needing its album
    def __init__(self, track, page):
        self._track = track
        # _album will eventually go away
        self._album = track.album
        self._album.addAlbumListener(self)
        self._track.addTrackListener(self)
        self._page = page

        self._bindEventHandlers()

    def _bindEventHandlers(self):
        self._page.onMetadataChange(self.updateTrack)

    def render(self):
        self.refresh()
        return self._page

    def updateTrack(self, state):
        self._track.trackTitle = state.trackTitle
        self._track.leadPerformer = state.leadPerformer
        self._track.versionInfo = state.versionInfo
        self._track.featuredGuest = state.featuredGuest
        self._track.lyricist = state.lyricist
        self._track.composer = state.composer
        self._track.publisher = state.publisher
        self._track.isrc = state.isrc
        self._track.tags = state.tags
        self._track.lyrics = state.lyrics
        self._track.language = state.language

    def trackStateChanged(self, track):
        self.refresh()

    def trackAdded(self, track, position):
        self.refresh()

    def trackRemoved(self, track, position):
        # todo let AlbumDirector decide of that
        if track == self._track:
            self._album.removeAlbumListener(self)
            self._track.removeTrackListener(self)
        else:
            # but first we need track to know its track number and total tracks
            self.refresh()

    def refresh(self):
        self._page.display(self._track)
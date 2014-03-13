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
    def __init__(self, album, track):
        self._album = album
        self._album.addAlbumListener(self)
        self._track = track
        self._track.addTrackListener(self)
        self._pages = []

    def add(self, page):
        page.onMetadataChange(self.metadataEdited)
        self._update(page)
        self._pages.append(page)

    def metadataEdited(self, state):
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
        self._updatePages()

    def trackAdded(self, track, position):
        self._updatePages()

    def trackRemoved(self, track, position):
        if track == self._track:
            self._album.removeAlbumListener(self)
            self._track.removeTrackListener(self)
        else:
            self._updatePages()

    def _updatePages(self):
        for page in self._pages:
            self._update(page)

    def _update(self, page):
        page.updateTrack(self._track, self._album)
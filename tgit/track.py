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
from tgit import tag
from tgit.metadata import Metadata


class TrackListener(object):
    def trackStateChanged(self, track):
        pass


class Track(object):
    __metaclass__ = tag.Taggable

    trackTitle = tag.text()
    compilation = tag.boolean()
    leadPerformer = tag.text()
    versionInfo = tag.text()
    featuredGuest = tag.text()
    publisher = tag.text()
    lyricist = tag.text()
    composer = tag.text()
    isrc = tag.text()
    labels = tag.text()
    lyrics = tag.text()
    language = tag.text()
    tagger = tag.text()
    taggingTime = tag.text()

    # todo Introduce Recording
    bitrate = tag.integer()
    duration = tag.decimal()

    def __init__(self, filename, metadata=None):
        self._filename = filename
        self._metadata = metadata or Metadata()
        self._album = None
        self._listeners = Announcer()

    def addTrackListener(self, listener):
        self._listeners.addListener(listener)

    def removeTrackListener(self, listener):
        self._listeners.removeListener(listener)

    @property
    def filename(self):
        return self._filename

    @property
    def metadata(self):
        return self._metadata

    @property
    def album(self):
        return self._album

    @album.deleter
    def album(self):
        self._album.removeAlbumListener(self)
        self._album = None

    @album.setter
    def album(self, album):
        self._album = album
        self.update(album.metadata)
        album.addAlbumListener(self)

    @property
    def number(self):
        # todo this should be a metadata of the track and not rely on the album
        return self.album and self.album.positionOf(self) + 1 or None

    def update(self, metadata):
        changes = metadata
        if changes[tag.COMPILATION] and tag.LEAD_PERFORMER in changes:
            del changes[tag.LEAD_PERFORMER]
        self._metadata.update(metadata)
        self.signalStateChange()

    def albumStateChanged(self, album):
        self.update(album.metadata)

    def trackAdded(self, track, position):
        pass

    def trackRemoved(self, track, position):
        pass

    def signalStateChange(self):
        self._listeners.trackStateChanged(self)
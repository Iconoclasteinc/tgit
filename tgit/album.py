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
from tgit.metadata import Image, Metadata
from tgit import tags


class AlbumListener(object):
    def albumStateChanged(self, album):
        pass

    def trackAdded(self, track, position):
        pass

    def trackRemoved(self, track, position):
        pass


class Album(object):
    def __init__(self, metadata=None):
        self._metadata = metadata or Metadata()
        self._tracks = []
        self._listeners = Announcer()

    def addAlbumListener(self, listener):
        self._listeners.addListener(listener)

    @property
    def images(self):
        return self._metadata.images

    def imagesOfType(self, type_):
        return self._metadata.imagesOfType(type_)

    @property
    def frontCovers(self):
        return self.imagesOfType(Image.FRONT_COVER)

    def addImage(self, mime, data, type_=Image.FRONT_COVER, desc=''):
        self._metadata.addImage(mime, data, type_, desc)
        self._signalStateChange()

    def addFrontCover(self, mime, data, desc='Front Cover'):
        self.addImage(mime, data, Image.FRONT_COVER, desc)

    def removeImages(self):
        self._metadata.removeImages()
        self._signalStateChange()

    @property
    def tracks(self):
        return list(self._tracks)

    def empty(self):
        return len(self._tracks) == 0

    def indexOf(self, track):
        return self.tracks.index(track)

    def addTrack(self, track, position=-1):
        self._copyTrackMetadataIfEmpty(track)

        if position == -1:
            position = len(self._tracks)
        self._tracks.insert(position, track)
        self._listeners.trackAdded(track, position)

    def _copyTrackMetadataIfEmpty(self, track):
        if self._metadata.empty():
            self._metadata.update(track.metadata.copy(*tags.ALBUM_TAGS))
            self._signalStateChange()

    def removeTrack(self, track):
        position = self._tracks.index(track)
        self._tracks.remove(track)
        self._listeners.trackRemoved(track, position)

    def tag(self):
        for track in self._tracks:
            track.tag(self._metadata)

    def _signalStateChange(self):
        self._listeners.albumStateChanged(self)


def addMetadataPropertiesTo(cls):
    for meta in tags.ALBUM_TAGS:
        def createProperty(name):
            def getter(self):
                return self._metadata[name]

            def setter(self, value):
                self._metadata[name] = value
                self._signalStateChange()

            setattr(cls, name, property(getter, setter))

        createProperty(meta)

addMetadataPropertiesTo(Album)

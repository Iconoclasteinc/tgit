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

from tgit.metadata import Image, Metadata
from tgit.announcer import Announcer

TITLE = 'releaseName'
LEAD_PERFORMER = 'leadPerformer'
GUEST_PERFORMERS = 'guestPerformers'
LABEL_NAME = 'labelName'
RECORDING_TIME = 'recordingTime'
RELEASE_TIME = 'releaseTime'
ORIGINAL_RELEASE_TIME = 'originalReleaseTime'
UPC = 'upc'

METADATA = [
    TITLE, LEAD_PERFORMER, GUEST_PERFORMERS, LABEL_NAME, RECORDING_TIME, RELEASE_TIME,
    ORIGINAL_RELEASE_TIME, UPC
]


class AlbumListener(object):
    def trackAdded(self, track, position):
        pass

    def trackRemoved(self, track, position):
        pass


class Album(object):
    def __init__(self):
        self._metadata = Metadata()
        self._tracks = []
        self._listeners = Announcer()

    def addAlbumListener(self, listener):
        self._listeners.add(listener)

    @property
    def frontCoverPicture(self):
        frontCovers = self._metadata.imagesOfType(Image.FRONT_COVER)
        return self._firstPictureIn(frontCovers)

    @frontCoverPicture.setter
    def frontCoverPicture(self, picture):
        self._replaceFrontCover(self._metadata, picture)

    @property
    def tracks(self):
        return list(self._tracks)

    def empty(self):
        return len(self._tracks) == 0

    def addTrack(self, track, position=-1):
        if position == -1:
            position = len(self._tracks)

        self._tracks.insert(position, track)
        self._listeners.announce().trackAdded(track, position)

    def removeTrack(self, track):
        position = self._tracks.index(track)
        self._tracks.remove(track)
        self._listeners.announce().trackRemoved(track, position)

    def tag(self):
        for track in self._tracks:
            self._updateAlbumMetadataOf(track)
            track.tag()

    def _firstPictureIn(self, pictures):
        if pictures:
            return pictures[0].mime, pictures[0].data
        else:
            return None, None

    def _replaceFrontCover(self, metadata, picture):
        metadata.removeImages()
        mime, data = picture
        if data:
            metadata.addImage(mime, data, Image.FRONT_COVER, 'Front Cover')

    def _updateAlbumMetadataOf(self, track):
        for meta in METADATA:
            track.metadata[meta] = self._metadata[meta]
        self._replaceFrontCover(track.metadata, self.frontCoverPicture)


def addMetadataPropertiesTo(cls):
    for meta in METADATA:
        def createProperty(name):
            def getter(self):
                return self._metadata[name]

            def setter(self, value):
                self._metadata[name] = value

            setattr(cls, name, property(getter, setter))

        createProperty(meta)

addMetadataPropertiesTo(Album)

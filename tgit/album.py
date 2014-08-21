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
from tgit import tag


class AlbumListener(object):
    def albumStateChanged(self, album):
        pass

    def trackAdded(self, track, position):
        pass

    def trackRemoved(self, track, position):
        pass


class Album(object):
    __metaclass__ = tag.Taggable

    releaseName = tag.text()
    compilation = tag.flag()
    leadPerformer = tag.text()
    isni = tag.text()
    guestPerformers = tag.pairs()
    labelName = tag.text()
    upc = tag.text()
    catalogNumber = tag.text()
    recordingTime = tag.text()
    releaseTime = tag.text()
    originalReleaseTime = tag.text()
    recordingStudios = tag.text()
    producer = tag.text()
    mixer = tag.text()
    contributors = tag.pairs()
    comments = tag.text()
    primaryStyle = tag.text()

    def __init__(self, metadata=None):
        self.metadata = metadata or Metadata()
        self.tracks = []
        self.listeners = Announcer()

    def addAlbumListener(self, listener):
        self.listeners.addListener(listener)

    def removeAlbumListener(self, listener):
        self.listeners.removeListener(listener)

    @property
    def images(self):
        return self.metadata.images

    def imagesOfType(self, type_):
        return self.metadata.imagesOfType(type_)

    @property
    def mainCover(self):
        if not self.images:
            return None

        if self.frontCovers:
            return self.frontCovers[0]

        return self.images[0]

    @property
    def frontCovers(self):
        return self.imagesOfType(Image.FRONT_COVER)

    def addImage(self, mime, data, type_=Image.OTHER, desc=''):
        self.metadata.addImage(mime, data, type_, desc)
        self.metadataChanged()

    def addFrontCover(self, mime, data, desc='Front Cover'):
        self.addImage(mime, data, Image.FRONT_COVER, desc)

    def removeImages(self):
        self.metadata.removeImages()
        self.metadataChanged()

    def __len__(self):
        return len(self.tracks)

    def empty(self):
        return len(self) == 0

    def positionOf(self, track):
        return self.tracks.index(track)

    def addTrack(self, track):
        self.insertTrack(track, len(self.tracks))

    def _inheritMetadataIfInitialTrack(self, track):
        if self.metadata.empty():
            self.metadata = track.metadata.copy(*Album.tags())
            self.metadataChanged()

    def insertTrack(self, track, position):
        self._inheritMetadataIfInitialTrack(track)
        self.tracks.insert(position, track)
        track.album = self
        self.listeners.trackAdded(track, position)

    def removeTrack(self, track):
        position = self.tracks.index(track)
        self.tracks.remove(track)
        self.listeners.trackRemoved(track, position)

    def metadataChanged(self):
        self.listeners.albumStateChanged(self)
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
from tgit import tags
from metadata import Metadata


class TrackListener(object):
    def trackStateChanged(self, track):
        pass


class Track(object):
    def __init__(self, filename, metadata=None, album=None):
        self._filename = filename
        self._metadata = metadata or Metadata()
        self._listeners = Announcer()
        self._album = album

    def addTrackListener(self, listener):
        self._listeners.addListener(listener)

    def removeTrackListener(self, listener):
        self._listeners.removeListener(listener)

    @property
    def filename(self):
        return self._filename

    @property
    def metadata(self):
        return self._metadata.copy()

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, album):
        self._album = album

    def _signalStateChange(self):
        self._listeners.trackStateChanged(self)


def addMetadataPropertiesTo(cls):
    for meta in tags.TRACK_TAGS:
        def createProperty(name):
            def getter(self):
                return self._metadata[name]

            def setter(self, value):
                self._metadata[name] = value
                self._signalStateChange()

            setattr(cls, name, property(getter, setter))

        createProperty(meta)

addMetadataPropertiesTo(Track)
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

TITLE = 'trackTitle'
VERSION_INFO = 'versionInfo'
FEATURED_GUEST = 'featuredGuest'
ISRC = 'isrc'

METADATA = [TITLE, VERSION_INFO, FEATURED_GUEST, ISRC]


class Track(object):
    def __init__(self, audioFile):
        self._audioFile = audioFile
        self._metadata = audioFile.metadata()

    @property
    def metadata(self):
        return self._metadata

    @property
    def filename(self):
        return self._audioFile.filename

    @property
    def bitrate(self):
        return self._audioFile.bitrate

    @property
    def duration(self):
        return self._audioFile.duration

    def tag(self):
        self._audioFile.save(self._metadata)


def addMetadataPropertiesTo(cls):
    for meta in METADATA:
        def createProperty(name):
            def getter(self):
                return self._metadata[name]

            def setter(self, value):
                self._metadata[name] = value

            setattr(cls, name, property(getter, setter))

        createProperty(meta)

addMetadataPropertiesTo(Track)

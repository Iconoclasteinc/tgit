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

from tgit.track import Track
from tgit.album import Album

from tgit import tags


class EmbeddedMetadata(object):
    def __init__(self, container):
        self._container = container

    def fetch(self, name):
        metadata = self._container.load(name)
        album = Album(albumMetadataFrom(metadata))
        track = Track(name, trackMetadataFrom(metadata))
        album.addTrack(track)
        return track

    def store(self, track):
        metadata = track.metadata
        metadata.merge(track.albumMetadata)
        self._container.save(track.filename, metadata)


def albumMetadataFrom(metadata):
    albumMetadata = metadata.subset(*tags.ALBUM_TAGS)
    albumMetadata.addImages(*metadata.images)
    return albumMetadata


def trackMetadataFrom(metadata):
    return metadata.subset(*tags.TRACK_TAGS)
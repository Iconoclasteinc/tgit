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

from tgit import tag
from tgit.metadata import Image, Metadata
from tgit.signal import signal
from tgit.track import Track


class Album(metaclass=tag.Taggable):
    track_inserted = signal(int, Track)
    track_removed = signal(int, Track)
    track_moved = signal(Track, int, int)

    # todo this should probably be in Track
    class Type:
        MP3 = "mp3"
        FLAC = "flac"

    release_name = tag.text()
    compilation = tag.flag()
    lead_performer = tag.text()
    lead_performer_region = tag.pairs()
    lead_performer_date_of_birth = tag.text()
    guest_performers = tag.pairs()
    label_name = tag.text()
    upc = tag.text()
    catalog_number = tag.text()
    release_time = tag.text()
    original_release_time = tag.text()
    contributors = tag.pairs()
    isnis = tag.map()
    ipis = tag.map()

    def __init__(self, metadata=None, of_type=Type.FLAC, filename=None):
        self.metadata = metadata.copy(*Album.tags()) if metadata is not None else Metadata()
        self.tracks = []
        self.type = of_type
        self.filename = filename

    @property
    def images(self):
        return self.metadata.images

    def images_of_type(self, type_):
        return self.metadata.imagesOfType(type_)

    @property
    def main_cover(self):
        if not self.images:
            return None

        if self.front_covers:
            return self.front_covers[0]

        return self.images[0]

    @property
    def front_covers(self):
        return self.images_of_type(Image.FRONT_COVER)

    def add_image(self, mime, data, type_=Image.OTHER, desc=""):
        self.metadata.addImage(mime, data, type_, desc)
        self.metadata_changed.emit(self)

    def add_front_cover(self, mime, data, desc="Front Cover"):
        self.add_image(mime, data, Image.FRONT_COVER, desc)

    def remove_images(self):
        self.metadata.removeImages()
        self.metadata_changed.emit(self)

    def add_isni(self, name, id_):
        if self.isnis is None:
            self.isnis = {name: id_}
        else:
            self.isnis[name] = id_
            self.metadata_changed.emit(self)

    def __len__(self):
        return len(self.tracks)

    def empty(self):
        return len(self) == 0

    def add_track(self, track):
        self._insert_track(len(self.tracks), track)

    def insert_track(self, track, position):
        self._insert_track(position, track)

    def _insert_track(self, position, track):
        track.album = self
        # todo move to Track
        if not self.compilation:
            track.lead_performer = self.lead_performer

        self.tracks.insert(position, track)
        self._renumber_tracks()
        self.track_inserted.emit(position, track)

    def remove_track(self, position):
        track = self.tracks.pop(position)
        self._renumber_tracks()
        self.track_removed.emit(position, track)
        return track

    def move_track(self, from_position, to_position):
        track = self.tracks.pop(from_position)
        self.tracks.insert(to_position, track)
        self._renumber_tracks()
        self.track_moved.emit(track, from_position, to_position)

    def _renumber_tracks(self):
        for index, track in enumerate(self.tracks):
            track.track_number = index + 1
            track.total_tracks = len(self.tracks)

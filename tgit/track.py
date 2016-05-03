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
from tgit.metadata import Metadata
from tgit.signal import Signal, signal


class ChainOfTitle:
    changed = signal(Signal.SELF)

    def __init__(self, track):
        lyricists = track.lyricist or []
        composers = track.composer or []
        publishers = track.publisher or []

        self._authors_composers = {}
        for name in set(lyricists + composers):
            self._authors_composers[name] = {"name": name}

        self._publishers = {}
        for name in publishers:
            self._publishers[name] = {"name": name}

    def load(self, chain_of_title):
        self._publishers = chain_of_title["publishers"]
        self._authors_composers = chain_of_title["authors_composers"]

    def update(self, track):
        lyricists = track.lyricist or []
        composers = track.composer or []
        publishers = set(track.publisher or [])
        authors_composers = set(lyricists + composers)

        to_remove_authors_composers = self._authors_composers.keys() - authors_composers
        to_add_authors_composers = authors_composers - self._authors_composers.keys()
        for name in to_remove_authors_composers:
            del self._authors_composers[name]

        for name in to_add_authors_composers:
            self._authors_composers[name] = {"name": name}

        to_remove_publishers = self._publishers.keys() - publishers
        to_add_publishers = publishers - self._publishers.keys()
        for name in to_remove_publishers:
            del self._publishers[name]

        for name in to_add_publishers:
            self._publishers[name] = {"name": name}

        if len(to_remove_publishers) > 0:
            for value in self._authors_composers.values():
                if "publisher" in value.keys() and value["publisher"] not in publishers:
                    value["publisher"] = ""

        if len(to_remove_authors_composers) > 0 or len(to_add_authors_composers) > 0 or len(
                to_remove_publishers) > 0 or len(to_add_publishers) > 0:
            self.changed.emit(self)

    @property
    def contributors(self):
        return {"authors_composers": self._authors_composers, "publishers": self._publishers}

    def update_contributor(self, **contributor):
        if contributor["name"] in self._authors_composers:
            self._authors_composers[contributor["name"]] = contributor

        if contributor["name"] in self._publishers:
            self._publishers[contributor["name"]] = contributor


class Track(object, metaclass=tag.Taggable):
    metadata_changed = signal(Signal.SELF)
    chain_of_title_changed = signal(ChainOfTitle)

    album = None

    track_title = tag.text()
    lead_performer = tag.text()
    version_info = tag.text()
    featured_guest = tag.text()
    comments = tag.text()
    publisher = tag.sequence()
    lyricist = tag.sequence()
    composer = tag.sequence()
    isrc = tag.text()
    iswc = tag.text()
    labels = tag.text()
    lyrics = tag.text()
    language = tag.text()
    tagger = tag.text()
    tagger_version = tag.text()
    tagging_time = tag.text()
    track_number = tag.numeric()
    total_tracks = tag.numeric()

    recording_time = tag.text()
    recording_studio = tag.text()
    recording_studio_region = tag.pairs()
    production_company = tag.text()
    production_company_region = tag.pairs()
    music_producer = tag.text()
    mixer = tag.text()
    primary_style = tag.text()

    # todo Introduce Recording
    bitrate = tag.numeric()
    duration = tag.decimal()

    def __init__(self, filename, metadata=None):
        self.filename = filename
        self.metadata = metadata or Metadata()
        self.chain_of_title = ChainOfTitle(self)
        self.chain_of_title.changed.subscribe(self.chain_of_title_changed.emit)

    @property
    def type(self):
        return self.album.type if self.album is not None else None

    def metadataChanged(self):
        self.metadata_changed.emit(self)

    def __repr__(self):
        return "Track(filename={}, metadata={})".format(self.filename, self.metadata)

    def load_chain_of_title(self, chain_of_title):
        self.chain_of_title.load(chain_of_title)

    def update_chain_of_title(self):
        self.chain_of_title.update(self)

    def update_contributor(self, **contributor):
        self.chain_of_title.update_contributor(**contributor)
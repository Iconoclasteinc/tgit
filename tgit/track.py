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


class Track(object, metaclass=tag.Taggable):
    metadata_changed = signal(Signal.SELF)

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

    @property
    def type(self):
        return self.album.type if self.album is not None else None

    def metadataChanged(self):
        self.metadata_changed.emit(self)

    def isni_for(self, role):
        if not self.isni:
            return ""

        # noinspection PyTypeChecker
        for current_role, _, isni in self.isni:
            if role == current_role:
                return isni

        return ""

    def __repr__(self):
        return "Track(filename={0}, metadata={1})".format(self.filename, self.metadata)

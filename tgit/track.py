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
from tgit.signal import signal


class Track(object, metaclass=tag.Taggable):
    metadata_changed = signal(Metadata)

    track_title = tag.text()
    lead_performer = tag.text()
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
    tagger_version = tag.text()
    tagging_time = tag.text()
    track_number = tag.numeric()

    # todo Introduce Recording
    bitrate = tag.numeric()
    duration = tag.decimal()

    def __init__(self, filename, metadata=None):
        self.filename = filename
        self.metadata = metadata or Metadata()
        self.album = None

    def metadataChanged(self):
        self.metadata_changed.emit(self.metadata)
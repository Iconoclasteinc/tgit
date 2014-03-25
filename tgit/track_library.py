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
import os
import re
import shutil
from datetime import datetime
from dateutil import tz

from tgit import tags, __version__

from tgit.track import Track


def sanitize(filename):
    return re.sub(r'[/<>?*\\:|"]', '_', filename).strip()


class TrackStorage(object):
    @staticmethod
    def filenameFor(track):
        return sanitize(u"{artist} - {title}.{format}".format(artist=track.leadPerformer,
                                                              title=track.trackTitle,
                                                              format='mp3'))

    @staticmethod
    def add(track):
        _, ext = os.path.splitext(track.filename)
        copy = os.path.join(os.path.dirname(track.filename), TrackStorage.filenameFor(track))
        if copy != track.filename:
            shutil.copy(track.filename, copy)
        return copy


class SystemClock(object):
    @staticmethod
    def now():
        return datetime.now(tz.tzlocal())


class TrackLibrary(object):
    def __init__(self, container, storage=TrackStorage(), clock=SystemClock()):
        self._container = container
        self._storage = storage
        self._clock = clock

    def fetch(self, name):
        metadata = self._container.load(name)
        return Track(name, metadata)

    def store(self, track):
        track.tagger = 'TGiT v' + __version__
        track.taggingTime = self._clock.now().strftime('%Y-%m-%d %H:%M:%S %z')
        self._container.save(self._storage.add(track), track.metadata)
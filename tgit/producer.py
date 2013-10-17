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


class MusicProducer(object):
    def importTrack(self, filename):
        pass

    def record(self):
        pass


class AlbumTagger(MusicProducer):
    def __init__(self, album, audioLibrary):
        self._album = album
        self._audioLibrary = audioLibrary

    def _loadAudioFile(self, filename):
        return self._audioLibrary.load(filename)

    def importTrack(self, filename):
        self._album.addTrack(Track(self._loadAudioFile(filename)))

    def record(self):
        self._album.tag()

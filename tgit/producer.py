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

from tgit.mp3 import MP3File


class ProductionListener(object):
    def trackAdded(self, track):
        pass


# todo collect tracks in album and let album notify listeners of album changes
# I'm thinking trackAdded, trackRemoved and trackMoved events, trackChanged, albumChanged
# todo we need focused tests
class AlbumProducer(object):
    def __init__(self, ui):
        self._ui = ui

    def addToAlbum(self, filename):
        track = MP3File(filename)
        self._ui.trackAdded(track)

    def removeTrack(self, track):
        self._ui.trackRemoved(track)

    def moveTrack(self, track, position):
        pass

    def saveAlbum(self, album):
        for track in album:
            track.save()

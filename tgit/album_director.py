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


class Snapshot(object):
    def __str__(self):
        return str(self.__dict__)


def updateTrack(track, state):
    track.trackTitle = state.trackTitle
    track.leadPerformer = state.leadPerformer
    track.versionInfo = state.versionInfo
    track.featuredGuest = state.featuredGuest
    track.lyricist = state.lyricist
    track.composer = state.composer
    track.publisher = state.publisher
    track.isrc = state.isrc
    track.tags = state.tags
    track.lyrics = state.lyrics
    track.language = state.language
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

from tgit.announcer import Announcer


class PlayerListener(object):
    def loading(self, track):
        pass

    def playing(self, track):
        pass

    def stopped(self, track):
        pass

    def paused(self, track):
        pass


class FakeAudioPlayer(object):
    def __init__(self):
        self._filename = None
        self._announce = Announcer()

    @property
    def media(self):
        return self._filename

    def isPlaying(self, filename):
        return self._filename == filename

    def play(self, filename):
        self._filename = filename
        self._announce.started(self._filename)

    def stop(self):
        self._announce.stopped(self._filename)
        self._filename = None

    def addPlayerListener(self, listener):
        self._announce.addListener(listener)

    def removePlayerListener(self, listener):
        self._announce.removeListener(listener)
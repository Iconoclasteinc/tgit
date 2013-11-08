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

from PyQt4.phonon import Phonon

from tgit.announcer import Announcer


class PlayerListener(object):
    def started(self, track):
        pass

    def stopped(self, track):
        pass

    def paused(self, track):
        pass


class PhononPlayer(object):
    LOADING = Phonon.LoadingState
    STOPPED = Phonon.StoppedState
    PLAYING = Phonon.PlayingState
    PAUSED = Phonon.PausedState

    def __init__(self, library):
        self._mediaLibrary = library
        self._player = Phonon.createPlayer(Phonon.MusicCategory)
        self._player.stateChanged.connect(self._stateChanged)
        self._announce = Announcer()
        self._media = None

    @property
    def media(self):
        return self._media.name

    def isPlaying(self):
        return self._player.state() == self.PLAYING

    def play(self, name):
        self._loading = self._mediaLibrary.load(name)
        self._player.setCurrentSource(Phonon.MediaSource(self._loading.source()))
        self._player.play()

    def stop(self):
        self._player.stop()

    def addPlayerListener(self, listener):
        self._announce.addListener(listener)

    def removePlayerListener(self, listener):
        self._announce.removeListener(listener)

    def _stateChanged(self, is_, was):
        if is_ == self.PLAYING:
            self._announce.started(self._loading.name)
            self._media = self._loading
        elif was == self.PLAYING:
            # On OSX loading a new media source triggers a transition to the stopped state first
            # whereas on Windows it goes straight to the LOADING state
            if is_ == self.STOPPED or is_ == self.LOADING:
                self.releaseMediaFile()
                self._announce.stopped(self._media.name)
            if is_ == self.PAUSED:
                self.releaseMediaFile()
                self._announce.paused(self._media.name)

    def releaseMediaFile(self):
        self._mediaLibrary.release(self._media)
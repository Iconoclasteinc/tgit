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

from tgit import fs
from tgit.announcer import Announcer
from tgit.metadata import Metadata


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

    def __init__(self):
        self._media = Phonon.createPlayer(Phonon.MusicCategory)
        self._media.stateChanged.connect(self._stateChanged)
        self._announce = Announcer()
        self._previous = None
        self._track = None

    def track(self):
        return self._track

    def isPlaying(self):
        return self._media.state() == self.PLAYING

    def play(self, track):
        self._starting = track
        track.playAudio(self)

    def playMp3(self, mp3):
        self._media.setCurrentSource(self._mediaSourceFor(mp3))
        self._media.play()

    def _mediaSourceFor(self, mp3):
        # On Windows, we have 2 issues with Phonon:
        # 1- It locks the file so we have to make a copy to allow tagging
        # 2- It fails to play files with our tags so we have to clear the frames
        copy = fs.makeCopy(mp3.filename)
        mp3.save(metadata=Metadata(), overwrite=True, filename=copy)
        return Phonon.MediaSource(copy)

    def stop(self):
        self._media.stop()

    def addPlayerListener(self, listener):
        self._announce.addListener(listener)

    def removePlayerListener(self, listener):
        self._announce.removeListener(listener)

    def _stateChanged(self, is_, was):
        if is_ == self.PLAYING:
            self._announce.started(self._starting)
            self._track = self._starting
        elif was == self.PLAYING:
            # On OSX loading a new media source triggers a transition to the stopped state first
            # whereas on Windows it goes straight to the LOADING state
            if is_ == self.STOPPED or is_ == self.LOADING:
                self._deleteMediaSourceFile()
                self._announce.stopped(self._track)
            if is_ == self.PAUSED:
                self._deleteMediaSourceFile()
                self._announce.paused(self._track)

    def _deleteMediaSourceFile(self):
        os.remove(self._media.currentSource().fileName())

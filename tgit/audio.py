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

from PyQt4.phonon import Phonon


def noSound():
    return NullAudio()


class NullAudio(object):
    def isPlaying(self):
        return False

    def play(self, filename):
        pass

    def stop(self):
        pass

    def addMediaListener(self, listener):
        pass


class MediaListener(object):
    def mediaStopped(self, media):
        pass

    def mediaPaused(self, media):
        pass


class PhononPlayer(object):
    LOADING = Phonon.LoadingState
    STOPPED = Phonon.StoppedState
    PLAYING = Phonon.PlayingState
    PAUSED = Phonon.PausedState

    def __init__(self):
        self._media = Phonon.createPlayer(Phonon.MusicCategory)
        self._media.stateChanged.connect(self._stateChanged)
        self._listeners = []

    def isPlaying(self):
        return self._media.state() == Phonon.PlayingState

    def play(self, filename):
        self._media.setCurrentSource(Phonon.MediaSource(filename))
        self._media.play()

    def stop(self):
        self._media.stop()

    def addMediaListener(self, listener):
        self._listeners.append(listener)

    def _stateChanged(self, is_, was):
        if was == self.PLAYING:
            if is_ == self.STOPPED:
                self._announceStopped(self._currentTrack())
            if is_ == self.PAUSED:
                self._announcePaused(self._currentTrack())

    def _announceStopped(self, track):
        for listener in self._listeners:
            listener.mediaStopped(track)

    def _announcePaused(self, track):
        for listener in self._listeners:
            listener.mediaPaused(track)

    def _currentTrack(self):
        return self._media.currentSource().fileName()

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
import tempfile
import shutil
from PyQt4.phonon import Phonon
from mutagen import mp3


def copyTrack(track):
    _, ext = os.path.splitext(track.filename)
    copy, path = tempfile.mkstemp(suffix=ext)
    os.close(copy)
    shutil.copy(track.filename, path)
    return mp3.MP3(path)


def clearTags(track):
    track.clear()
    track.save()


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
        self._playingTrack = None

    def isPlaying(self):
        return self._media.state() == Phonon.PlayingState

    def play(self, track):
        self._playingTrack = track
        self._media.setCurrentSource(Phonon.MediaSource(self._source(track)))
        self._media.play()

    def _source(self, track):
        # On Windows, we have 2 issues with Phonon:
        # 1- It locks the file so we have to make a copy to allow tagging
        copy = copyTrack(track)
        # 2- It fails to play files with our tags so we have to clear the frames
        clearTags(copy)
        return copy.filename

    def stop(self):
        self._media.stop()

    def addMediaListener(self, listener):
        self._listeners.append(listener)

    def _stateChanged(self, is_, was):
        if was == self.PLAYING:
            if is_ == self.STOPPED:
                self._announceStopped(self._playingTrack)
            if is_ == self.PAUSED:
                self._announcePaused(self._playingTrack)

    def _announceStopped(self, track):
        for listener in self._listeners:
            listener.mediaStopped(track)

    def _announcePaused(self, track):
        for listener in self._listeners:
            listener.mediaPaused(track)
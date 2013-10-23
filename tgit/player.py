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
from mutagen import mp3

from tgit import fs


class MediaListener(object):
    def mediaStopped(self, media):
        pass

    def mediaPaused(self, media):
        pass


# todo we need focused tests
class PhononPlayer(object):
    LOADING = Phonon.LoadingState
    STOPPED = Phonon.StoppedState
    PLAYING = Phonon.PlayingState
    PAUSED = Phonon.PausedState

    def __init__(self):
        self._media = Phonon.createPlayer(Phonon.MusicCategory)
        self._media.stateChanged.connect(self._stateChanged)
        self._listeners = []
        self._currentTrack = None

    def currentTrack(self):
        return self._currentTrack

    def isPlaying(self):
        return self._media.state() == self.PLAYING

    def play(self, track):
        self._media.setCurrentSource(Phonon.MediaSource(self._copy(track)))
        self._media.play()
        self._currentTrack = track
        # might want to delete the temp file for the previous track at some point

    # todo let audio file make a copy and clear tags
    def _copy(self, track):
        # On Windows, we have 2 issues with Phonon:
        # 1- It locks the file so we have to make a copy to allow tagging
        copy = mp3.MP3(fs.makeCopy(track.filename))
        # 2- It fails to play files with our tags so we have to clear the frames
        self._clearTags(copy)
        return copy.filename

    def _clearTags(self, audioFile):
        audioFile.clear()
        if audioFile.tags is None:
            audioFile.add_tags()
        audioFile.save()

    def stop(self):
        self._media.stop()

    def addMediaListener(self, listener):
        self._listeners.append(listener)

    def _stateChanged(self, is_, was):
        if was == self.PLAYING:
            # On OSX loading a new media source triggers a transition to the stopped state first
            # whereas on Windows it goes straight to the LOADING state
            if is_ == self.STOPPED or is_ == self.LOADING:
                self._announceStopped(self._currentTrack)
            if is_ == self.PAUSED:
                self._announcePaused(self._currentTrack)

    # todo investigate using QObject signals & slots
    def _announceStopped(self, track):
        for listener in self._listeners:
            listener.mediaStopped(track)

    def _announcePaused(self, track):
        for listener in self._listeners:
            listener.mediaPaused(track)
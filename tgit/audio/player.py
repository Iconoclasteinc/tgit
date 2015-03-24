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
from PyQt5.QtCore import QUrl

# noinspection PyUnresolvedReferences
# We want QtNetwork to be included in the binary package, so until we figure out how to do that
# declaratively in PyInstaller, let's import the module explicitely
import PyQt5.QtNetwork
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

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


# todo take a track instead of a filename?
class MediaPlayer(object):
    STOPPED = QMediaPlayer.StoppedState
    PLAYING = QMediaPlayer.PlayingState
    PAUSED = QMediaPlayer.PausedState

    def __init__(self):
        self._player = QMediaPlayer()
        self._player.stateChanged.connect(self._stateChanged)
        self._announce = Announcer()
        self._media = None
        self._loading = None

    def isPlaying(self, filename):
        return self._player.state() == self.PLAYING and self._media == filename

    def play(self, name):
        self._announce.loading(name)
        self._loading = name
        self._player.setMedia(QMediaContent(QUrl.fromLocalFile(name)))
        self._player.play()

    def stop(self):
        self._player.stop()

    def addPlayerListener(self, listener):
        self._announce.addListener(listener)

    def removePlayerListener(self, listener):
        self._announce.removeListener(listener)

    def _stateChanged(self, state):
        if state == self.PLAYING:
            self._media = self._loading
            self._announce.playing(self._media)
        elif state == self.STOPPED:
            self._announce.stopped(self._media)
        elif state == self.PAUSED:
            self._announce.paused(self._media)
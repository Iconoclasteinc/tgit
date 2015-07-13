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
from enum import Enum

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from tgit.signal import Observable, signal
from tgit.track import Track


class PlaybackError(Enum):
    none = QMediaPlayer.NoError
    unsupported_format = QMediaPlayer.FormatError
    access_denied = QMediaPlayer.AccessDeniedError


class MediaPlayer(metaclass=Observable):
    _PLAYING = QMediaPlayer.BufferedMedia
    _STOPPED = QMediaPlayer.StoppedState

    playing = signal(Track)
    stopped = signal(Track)
    error_occurred = signal(Track)

    _track = None

    def __init__(self):
        self._player = QMediaPlayer()
        self._player.stateChanged.connect(self._state_changed)
        self._player.mediaStatusChanged.connect(self._media_status_changed)

    def play(self, track):
        self._player.stop()
        self._track = track
        self._player.setMedia(QMediaContent(QUrl.fromLocalFile(track.filename)))
        self._player.play()

    def stop(self):
        self._player.stop()
        self._player.setMedia(QMediaContent())
        self._track = None

    def _media_status_changed(self, state):
        if state == self._PLAYING:
            self.playing.emit(self._track)

    @property
    def error(self):
        return PlaybackError(self._player.error())

    def _state_changed(self, state):
        if state == self._STOPPED and self.error is not PlaybackError.none:
            self.error_occurred.emit(self._track, self.error)
        elif state == self._STOPPED:
            self.stopped.emit(self._track)

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

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from tgit.signal import Observable, signal
from tgit.track import Track
from tgit.util import fs


class MediaPlayer(metaclass=Observable):
    PLAYING = QMediaPlayer.BufferedMedia
    STOPPED = QMediaPlayer.EndOfMedia

    playing = signal(Track)
    stopped = signal(Track)

    _player = None
    _current_track = None
    _media_file = None

    def is_playing(self, track):
        return self._player is not None and self._player.mediaStatus() == self.PLAYING and self._current_track == track

    def play(self, track):
        self.stop()
        self._player = QMediaPlayer()
        self._player.mediaStatusChanged.connect(self._media_state_changed)
        self._current_track = track
        self._media_file = fs.make_temp_copy(track.filename)
        self._player.setMedia(QMediaContent(QUrl.fromLocalFile(self._media_file)))
        self._player.play()

    def stop(self):
        if self._player is not None:
            self._player.stop()
            self.stopped.emit(self._current_track)
            self._player = None
            os.unlink(self._media_file)

    def _media_state_changed(self, state):
        if state == self.PLAYING:
            self.playing.emit(self._current_track)
        if state == self.STOPPED:
            self.stop()

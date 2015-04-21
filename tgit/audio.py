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

from tgit.announcer import Announcer
from tgit.util import fs


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
    LOADING = QMediaPlayer.LoadingMedia
    PLAYING = QMediaPlayer.BufferedMedia
    STOPPED = QMediaPlayer.EndOfMedia

    _player = None
    _current_media = None
    _actual_file = None

    def __init__(self):
        self._announce = Announcer()

    def is_playing(self, filename):
        return self._player is not None and self._player.mediaStatus() == self.PLAYING and self._current_media == filename

    def play(self, filename):
        self.stop()

        self._player = QMediaPlayer()
        self._player.mediaStatusChanged.connect(self._media_changed)
        self._current_media = filename
        self._actual_file = fs.make_temp_copy(filename)
        self._player.setMedia(QMediaContent(QUrl.fromLocalFile(self._actual_file)))
        self._player.play()

    def stop(self):
        if self._player is not None:
            self._player.stop()
            self._announce.stopped(self._current_media)
            self._player = None
            os.unlink(self._actual_file)

    def add_player_listener(self, listener):
        self._announce.addListener(listener)

    def remove_player_listener(self, listener):
        self._announce.removeListener(listener)

    def _media_changed(self, state):
        if state == self.LOADING:
            self._announce.loading(self._current_media)
        if state == self.PLAYING:
            self._announce.playing(self._current_media)
        if state == self.STOPPED:
            self.stop()
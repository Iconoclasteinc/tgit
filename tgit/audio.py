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
import shutil
import sip

from PyQt5.QtCore import QUrl

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from tgit.platforms import windows
from tgit.signal import Observable, signal
from tgit.track import Track
from tgit import fs


def open_media_player(portfolio):
    player = MediaPlayer()
    subscription = portfolio.on_project_closed.subscribe(lambda _: player.stop())
    player.closed.subscribe(subscription.cancel)

    return player


class MediaPlayer(metaclass=Observable):
    class Error(Enum):
        none = QMediaPlayer.NoError
        unsupported_format = QMediaPlayer.FormatError
        access_denied = QMediaPlayer.AccessDeniedError

    closed = signal()
    playing = signal(Track)
    stopped = signal(Track)
    error_occurred = signal(Track)

    def __init__(self):
        self._media_library = create_media_library()
        self._playlist = []
        self._player = QMediaPlayer()
        self._player.stateChanged.connect(self._state_changed)
        self._player.mediaStatusChanged.connect(self._media_status_changed)

    def play(self, track):
        self._playlist.append(track)
        self._player.setMedia(self._media_library.fetch(track.filename))
        self._player.play()

    def stop(self):
        self._player.stop()

    def _media_status_changed(self, state):
        if state == QMediaPlayer.BufferedMedia:
            self._error = QMediaPlayer.NoError
            self.playing.emit(self._playlist[0])
        elif state == QMediaPlayer.InvalidMedia:
            # On windows 8, we only get an InvalidMedia status in case of error,
            # so we need to keep track of the error that occurred
            self._error = QMediaPlayer.FormatError

    @property
    def error(self):
        return MediaPlayer.Error(self._player.error() or self._error)

    def _state_changed(self, state):
        if state == QMediaPlayer.StoppedState and self.error is not MediaPlayer.Error.none:
            self.error_occurred.emit(self._playlist.pop(0), self.error)
        elif state == QMediaPlayer.StoppedState:
            self.stopped.emit(self._playlist.pop(0))

    def dispose(self):
        self._player.stop()
        # force the deletion of the player on windows because windows
        # doesn't release the handle and prevents further instanciations
        sip.delete(self._player)
        self._player = None

        self._media_library.dispose()
        self.closed.emit()


def create_media_library():
    return WindowsMediaLibrary() if windows else MediaLibrary()


class MediaLibrary:
    def fetch(self, filename):
        return QMediaContent(QUrl.fromLocalFile(filename))

    def dispose(self):
        pass


class WindowsMediaLibrary(MediaLibrary):
    def __init__(self):
        self._directory = fs.make_temp_dir()

    def fetch(self, filename):
        return super().fetch(fs.make_temp_copy(filename, self._directory))

    def dispose(self):
        shutil.rmtree(self._directory, ignore_errors=True)

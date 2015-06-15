# -*- coding: utf-8 -*-
import shutil

from test.util import mp3_file as mp3, flac_file as flac
from tgit.signal import Observable, signal
from tgit.track import Track


def recording_library(tmpdir):
    return RecordingLibrary(tmpdir)


class RecordingLibrary(object):
    def __init__(self, root):
        self._root = root
        self._entries = []

    @property
    def root(self):
        return self._root

    @property
    def files(self):
        return iter(self._entries)

    def _add(self, recording):
        self._entries.append(recording)
        return recording.filename

    def add_mp3(self, **metadata):
        return self._add(mp3.make(to=self._root, **metadata))

    def add_flac(self, **metadata):
        return self._add(flac.make(to=self._root, **metadata))

    def delete(self):
        shutil.rmtree(self._root)


def audio_player():
    return FakeAudioPlayer()


class FakeAudioPlayer(metaclass=Observable):
    playing = signal(Track)
    stopped = signal(Track)

    _track = None

    @property
    def current_track(self):
        return self._track

    def is_playing(self, track):
        return self._track == track

    def play(self, track):
        self._track = track
        self.playing.emit(self._track)

    def stop(self):
        self._track = None
        if self._track is not None:
            self.playing.emit(self._track)

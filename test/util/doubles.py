# -*- coding: utf-8 -*-

from test.util import mp3_file as mp3, flac_file as flac
from tgit.signal import Observable, signal
from tgit.track import Track


def recording_library(tmpdir):
    return RecordingLibrary(tmpdir)


class RecordingLibrary(object):
    def __init__(self, local_path):
        self._local_path = local_path
        self._entries = []

    @property
    def root_path(self):
        return self._local_path.strpath

    @property
    def files(self):
        return iter(self._entries)

    def path(self, filename):
        return self._local_path.join(filename).strpath

    def _add(self, recording):
        self._entries.append(recording)
        return recording.filename

    def add_mp3(self, **metadata):
        return self._add(mp3.make(to=self.root_path, **metadata))

    def add_flac(self, **metadata):
        return self._add(flac.make(to=self.root_path, **metadata))

    def delete(self):
        self._local_path.remove()


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

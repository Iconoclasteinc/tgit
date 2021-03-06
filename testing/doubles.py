# -*- coding: utf-8 -*-
from testing import flac_file as flac, mp3_file as mp3
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


def fake_audio_player(*_):
    return FakeAudioPlayer()


class FakeAudioPlayer(metaclass=Observable):
    playing = signal(Track)
    stopped = signal(Track)
    error_occurred = signal(Track, int)

    track = None

    def play(self, track):
        self.track = track
        self.playing.emit(self.track)

    def stop(self):
        if self.track is not None:
            self.stopped.emit(self.track)

        self.track = None

    def error(self, error):
        self.error_occurred.emit(self.track, error)


class FakeFormat:
    album = None
    workbook = None

    def write(self, album, workbook):
        self.album = album
        self.workbook = workbook


class FakeWorkbook:
    filename = ""

    def save(self, filename):
        self.filename = filename

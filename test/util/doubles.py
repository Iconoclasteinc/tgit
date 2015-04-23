# -*- coding: utf-8 -*-
import os

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from test.util import mp3_file as mp3, flac_file as flac
from tgit import tagging
from tgit.announcer import Announcer
from tgit.metadata import Image
from tgit.util import fs


def recording_library(tmpdir):
    return RecordingLibrary(tmpdir)


class RecordingLibrary(object):
    def __init__(self, root):
        self.root = root
        self.entries = []

    def _add(self, recording):
        self.entries.append(recording)
        return recording.filename

    def add_mp3(self, **metadata):
        return self._add(mp3.make(to=self.root, **metadata))

    def add_flac(self, **metadata):
        return self._add(flac.make(to=self.root, **metadata))

    def path(self, filename):
        return os.path.join(self.root, filename)

    def exists(self, filename):
        return os.path.exists(self.path(filename))

    def contains(self, filename, front_cover=None, **tags):
        if not self.exists(filename):
            raise AssertionError('Not in library: ' + filename)

        metadata = tagging.load_metadata(self.path(filename))
        images = []
        # todo use builders and metadata
        if front_cover:
            image, desc = front_cover
            mime = fs.guessMimeType(image)
            images.append(Image(mime, fs.binary_content_of(image), type_=Image.FRONT_COVER, desc=desc))

        assert_that(metadata, has_entries(tags), 'metadata tags')
        assert_that(metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        for recording in self.entries:
            recording.delete()


def audioPlayer(*args):
    return FakeAudioPlayer()


class FakeAudioPlayer(object):
    def __init__(self):
        self._filename = None
        self._announce = Announcer()

    @property
    def media(self):
        return self._filename

    def is_playing(self, filename):
        return self._filename == filename

    def play(self, filename):
        self._filename = filename
        self._announce.started(self._filename)

    def stop(self):
        self._announce.stopped(self._filename)
        self._filename = None

    def add_player_listener(self, listener):
        self._announce.addListener(listener)

    def remove_player_listener(self, listener):
        self._announce.removeListener(listener)


def export_format():
    return FakeExportFormat()


class FakeExportFormat(object):
    def write(self, album, out):
        for track in album.tracks:
            out.write(track.track_title or "")
            out.write('\n')
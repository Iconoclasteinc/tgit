# -*- coding: utf-8 -*-
import os
import tempfile

from hamcrest import assert_that, has_entries, contains_inanyorder as contains
from test.util import mp3_file as mp3
from tgit.util import fs
from tgit.metadata import Image
from tgit.announcer import Announcer
from tgit.mp3 import id3_tagger as tagger


def metadataContainer():
    return FakeMetadataContainer()


# todo make that a driver
class FakeMetadataContainer(object):
    def __init__(self):
        self.files = []
        self.dir = tempfile.mkdtemp()

    def add(self, **metadata):
        return mp3.make(to=self.dir, **metadata).filename

    def load(self, filename):
        if not os.path.exists(filename):
            raise AssertionError('Cannot find in library: ' + filename)

        return tagger.load(filename)

    def contains(self, filename, frontCover=None, **tags):
        images = []
        # todo use builders and metadata
        if frontCover:
            image, desc = frontCover
            mime = fs.guessMimeType(image)
            images.append(Image(mime, fs.readContent(image), type_=Image.FRONT_COVER, desc=desc))

        metadata = self.load(os.path.join(self.dir, filename))
        assert_that(metadata, has_entries(tags), 'metadata tags')
        assert_that(metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        # if we remove the tempdir, Qt filesystem watchers complain
        for f in os.listdir(self.dir):
            os.remove(os.path.join(self.dir, f))


def audioPlayer(*args):
    return FakeAudioPlayer()


class FakeAudioPlayer(object):
    def __init__(self):
        self._filename = None
        self._announce = Announcer()

    @property
    def media(self):
        return self._filename

    def isPlaying(self, filename):
        return self._filename == filename

    def play(self, filename):
        self._filename = filename
        self._announce.started(self._filename)

    def stop(self):
        self._announce.stopped(self._filename)
        self._filename = None

    def addPlayerListener(self, listener):
        self._announce.addListener(listener)

    def removePlayerListener(self, listener):
        self._announce.removeListener(listener)


def trackLibrary():
    return MockTrackLibrary()


class MockTrackLibrary(object):
    def __init__(self):
        self.tracks = []

    def store(self, track):
        self.tracks.append(track)

    def fetch(self, name):
        return next((track for track in self.tracks if track.filename == name), None)

    def assertContains(self, *tracks):
        assert_that(self.tracks, contains(*tracks), 'tracks in catalog')

# -*- coding: utf-8 -*-
import os

from hamcrest import assert_that, has_entries, contains_inanyorder as contains
from test.util import mp3_file as mp3, resources
from tgit.util import fs
from tgit.metadata import Image
from tgit.announcer import Announcer
from tgit.tagging import id3_container as id3


def recordingLibrary():
    return Mp3Library(resources.makeTempDir())


class Mp3Library(object):
    def __init__(self, root):
        self.root = root
        self.recordings = []

    def create(self, **metadata):
        recording = mp3.make(to=self.root, **metadata)
        self.recordings.append(recording.filename)
        return recording.filename

    def path(self, filename):
        return os.path.join(self.root, filename)

    def exists(self, filename):
        return os.path.exists(self.path(filename))

    def contains(self, filename, frontCover=None, **tags):
        if not self.exists(filename):
            raise AssertionError('Not in library: ' + filename)

        metadata = id3.load(self.path(filename))
        images = []
        # todo use builders and metadata
        if frontCover:
            image, desc = frontCover
            mime = fs.guessMimeType(image)
            images.append(Image(mime, fs.readContent(image), type_=Image.FRONT_COVER, desc=desc))

        assert_that(metadata, has_entries(tags), 'metadata tags')
        assert_that(metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        for recording in self.recordings:
            os.remove(recording)


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


def exportFormat():
    return FakeExportFormat()


class FakeExportFormat(object):
    def write(self, album, out):
        for track in album.tracks:
            out.write(track.trackTitle)
            out.write('\n')


def nameRegistry():
    return FakeNameRegistry()


class FakeNameRegistry(object):
    def __init__(self):
        self.registry = []

    def searchByKeywords(self, *keywords):
        firstName = keywords[1]
        lastName = keywords[0]
        entries = []
        for entry in self.registry:
            if entry[1] == lastName and entry[2] == firstName:
                entries.append(entry)

        return entries
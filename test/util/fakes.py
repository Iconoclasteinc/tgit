# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from tgit.audio_library import AudioLibrary
from tgit import mp3_file as mp3File, fs
from tgit.file_chooser import FileChooser
from tgit.metadata import Image
from tgit.announcer import Announcer
from tgit import tags as tagging


class FakeAudioLibrary(AudioLibrary):
    def __init__(self):
        self.files = []

    def add(self, file_):
        self.files.append(file_)
        return file_

    def load(self, filename):
        for file_ in self.files:
            if file_.filename == filename:
                return mp3File.load(filename)

        raise AssertionError('Not in library: % s' % filename)

    def containsFile(self, filename, **tags):
        images = []
        if tagging.FRONT_COVER in tags:
            mime = fs.guessMimeType(tags[tagging.FRONT_COVER])
            images.append(Image(mime, fs.readContent(tags[tagging.FRONT_COVER]),
                                type_=Image.FRONT_COVER, desc='Front Cover'))
            del tags[tagging.FRONT_COVER]

        mp3 = self.load(filename)
        assert_that(mp3.metadata, has_entries(tags), 'metadata tags')
        assert_that(mp3.metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        [mp3.delete() for mp3 in self.files]


class FakeAudioPlayer(object):
    def __init__(self):
        self._track = None
        self._announce = Announcer()

    def track(self):
        return self._track

    def isPlaying(self):
        return self._track is not None

    def play(self, track):
        self._track = track
        self._announce.started(self._track)

    def stop(self):
        self._announce.stopped(self._track)
        self._track = None

    def addPlayerListener(self, listener):
        self._announce.addListener(listener)

    def removePlayerListener(self, listener):
        self._announce.removeListener(listener)


class FakeFileChooser(FileChooser):
    def chooses(self, filename):
        self.filename = filename

    def chooseFile(self):
        if hasattr(self, 'filename'):
            self._signalFileChosen(self.filename)
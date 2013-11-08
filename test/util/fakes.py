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
        self.recordings = []

    def add(self, recording):
        self.recordings.append(recording)
        return recording.filename

    def load(self, filename):
        for file_ in self.recordings:
            if file_.filename == filename:
                return mp3File.load(filename)

        raise AssertionError('Not in library: % s' % filename)

    def contains(self, filename, **tags):
        images = []
        if tagging.FRONT_COVER in tags:
            image, desc = tags[tagging.FRONT_COVER]
            mime = fs.guessMimeType(image)
            images.append(Image(mime, fs.readContent(image), type_=Image.FRONT_COVER, desc=desc))
            del tags[tagging.FRONT_COVER]

        mp3 = self.load(filename)
        assert_that(mp3.metadata, has_entries(tags), 'metadata tags')
        assert_that(mp3.metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        [recording.delete() for recording in self.recordings]


class FakeAudioPlayer(object):
    def __init__(self):
        self._filename = None
        self._announce = Announcer()

    @property
    def media(self):
        return self._filename

    def isPlaying(self):
        return self._filename is not None

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


class FakeFileChooser(FileChooser):
    def chooses(self, filename):
        self.filename = filename

    def chooseFile(self):
        if hasattr(self, 'filename'):
            self._signalFileChosen(self.filename)
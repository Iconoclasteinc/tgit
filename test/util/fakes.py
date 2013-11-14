# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from tgit.util import fs
from tgit.ui.file_chooser import FileChooser
from tgit.metadata import Image
from tgit.announcer import Announcer
from tgit import tags as tagging
from tgit.mp3 import id3_tagger as tagger


class FakeMetadataStore(object):
    def __init__(self):
        self.files = []

    # todo accept metadata tags and create mp3
    def add(self, recording):
        self.files.append(recording)
        return recording.filename

    def load(self, filename):
        for file_ in self.files:
            if file_.filename == filename:
                return tagger.load(filename)

        raise AssertionError('Not in library: % s' % filename)

    def contains(self, filename, **tags):
        images = []
        # todo use builders and metadata
        if tagging.FRONT_COVER in tags:
            image, desc = tags[tagging.FRONT_COVER]
            mime = fs.guessMimeType(image)
            images.append(Image(mime, fs.readContent(image), type_=Image.FRONT_COVER, desc=desc))
            del tags[tagging.FRONT_COVER]

        metadata = self.load(filename)
        assert_that(metadata, has_entries(tags), 'metadata tags')
        assert_that(metadata.images, contains(*images), 'attached pictures')

    def delete(self):
        [recording.delete() for recording in self.files]


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
    def __init__(self):
        super(FakeFileChooser, self).__init__()
        self.choices = []

    def chooses(self, filename):
        self.choices.append(filename)

    def chooseSingleFile(self):
        self.signalFileChosen(self.choices[0])

    def chooseFiles(self):
        self.signalFilesChosen(self.choices)
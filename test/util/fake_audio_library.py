# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from test.util import fs

from tgit.audio_library import AudioLibrary
from tgit.metadata import Image
import tgit.album as album
from tgit import mp3_file as mp3File


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
        if album.FRONT_COVER in tags:
            mime = fs.guessMimeType(tags[album.FRONT_COVER])
            images.append(Image(mime, fs.readContent(tags[album.FRONT_COVER]),
                                type_=Image.FRONT_COVER, desc='Front Cover'))
            del tags[album.FRONT_COVER]

        mp3 = self.load(filename)
        assert_that(mp3.metadata(), has_entries(tags), 'metadata tags')
        assert_that(mp3.metadata().images, contains(*images), 'attached pictures')

    def delete(self):
        [mp3.delete() for mp3 in self.files]

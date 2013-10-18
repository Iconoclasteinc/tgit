# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from tgit.audio_library import AudioLibrary
from tgit.metadata import Image
from tgit import mp3_file as mp3File
from test.util import fs


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

        raise AssertionError("Not in library: % s" % filename)

    def containsFile(self, filename, **tags):
        images = []
        if 'frontCoverPicture' in tags:
            mime = fs.guessMimeType(tags['frontCoverPicture'])
            images.append(Image(mime, fs.readContent(tags['frontCoverPicture']),
                                type_=Image.FRONT_COVER, desc='Front Cover'))
            del tags['frontCoverPicture']

        mp3 = self.load(filename)
        assert_that(mp3.metadata(), has_entries(tags), 'metadata tags')
        assert_that(mp3.metadata().images, contains(*images), 'attached pictures')

    def delete(self):
        [mp3.delete() for mp3 in self.files]

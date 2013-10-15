# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_entries, contains_inanyorder as contains

from tgit.metadata import Image
from tgit import mp3_file as mp3File
from test.util import fs


class FakeAudioLibrary(object):
    def __init__(self):
        self.mp3s = []

    def add(self, mp3):
        mp3.make()
        self.mp3s.append(mp3)
        return mp3

    def delete(self):
        [mp3.delete() for mp3 in self.mp3s]

    def containsFile(self, filename, **tags):
        images = []
        if 'frontCoverPicture' in tags:
            mime = fs.guessMimeType(tags['frontCoverPicture'])
            images.append(Image(mime, fs.readContent(tags['frontCoverPicture']),
                                type_=Image.FRONT_COVER, desc='Front Cover'))
            del tags['frontCoverPicture']

        mp3 = self._loadMp3(filename)
        assert_that(mp3.metadata, has_entries(tags), 'metadata tags')
        assert_that(mp3.metadata.images, contains(*images), 'attached pictures')

    def _loadMp3(self, name):
        try:
            return mp3File.load(name)
        except IOError:
            raise AssertionError("Not in library: % s" % name)
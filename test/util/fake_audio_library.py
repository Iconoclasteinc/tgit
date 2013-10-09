# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_properties

from tgit.mp3 import MP3File

from test.util import matchers


class FakeAudioLibrary(object):
    def __init__(self):
        self.mp3s = []

    def add(self, mp3):
        mp3.make()
        self.mp3s.append(mp3)
        return mp3

    def delete(self):
        [mp3.delete() for mp3 in self.mp3s]

    def containsFile(self, name, **tags):
        if 'frontCoverFile' in tags:
            tags['frontCoverPicture'] = matchers.samePictureAs(tags['frontCoverFile'])
            del tags['frontCoverFile']

        mp3 = self._open(name)
        assert_that(mp3, has_properties(tags))

    def _open(self, name):
        try:
            return MP3File(name)
        except IOError:
            raise AssertionError("Not found in library: % s" % name)
# -*- coding: utf-8 -*-

import os
from hamcrest import assert_that, has_properties

from tgit.mp3 import MP3File

from tests.util import matchers


class FakeAudioLibrary(object):
    def __init__(self):
        self.files = []

    def add(self, filename):
        self.files.append(filename)

    def delete(self):
        [os.remove(f) for f in self.files]

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
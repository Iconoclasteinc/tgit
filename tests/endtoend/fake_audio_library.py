# -*- coding: utf-8 -*-

from hamcrest import assert_that, has_properties

from tgit.mp3 import MP3File

from tests.util import matchers
from tests.util.mp3_maker import MP3


class FakeAudioLibrary(object):
    def __init__(self):
        self.files = []

    def importFile(self, filename):
        mp3 = MP3(filename)
        self.files.append(mp3)
        return mp3.name

    def delete(self):
        [f.delete() for f in self.files]

    def containsFile(self, name, **tags):
        if 'frontCoverFile' in tags:
            tags['frontCoverPicture'] = matchers.samePictureAs(tags['frontCoverFile'])
            del tags['frontCoverFile']

        audioFile = self._openMp3(name)
        assert_that(audioFile, has_properties(tags))

    def _openMp3(self, name):
        try:
            audioFile = MP3File(name)
        except IOError:
            raise AssertionError("Missing in library: % s" % name)
        return audioFile
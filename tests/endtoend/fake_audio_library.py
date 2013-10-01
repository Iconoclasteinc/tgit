# -*- coding: utf-8 -*-

import mimetypes

from hamcrest import *

from tests.util.mp3_maker import MP3

from tgit.mp3 import MP3File


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
            tags['frontCoverPicture'] = samePictureAs(tags['frontCoverFile'])
            del tags['frontCoverFile']

        audioFile = self._openMp3(name)
        assert_that(audioFile, has_properties(tags))

    def _openMp3(self, name):
        try:
            audioFile = MP3File(name)
        except IOError:
            raise AssertionError("Missing in library: % s" % name)
        return audioFile


# todo move to a file related utilities module
def readContent(filename):
    return open(filename, "rb").read()


# todo move to a file related utilities module
def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]


# todo move to a matchers module
def samePictureAs(filename):
    return contains(equal_to(guessMimeType(filename)),
                    has_length(len(readContent(filename))))


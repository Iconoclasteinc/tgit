# -*- coding: utf-8 -*-

import mimetypes

from hamcrest import *

from tests.util.mp3_builder import MP3

from tgit.mp3 import MP3File


class FakeAudioLibrary(object):
    def __init__(self):
        self._files = []

    def addFile(self, filename):
        mp3 = MP3(filename)
        self._files.append(mp3)
        return mp3.name

    def destroy(self):
        [f.delete() for f in self._files]

    def openMp3(self, name):
        try:
            audioFile = MP3File(name)
        except IOError:
            raise AssertionError("Missing in library: % s" % name)
        return audioFile

    def containsFileWithMetadata(self, name, **tags):
        if 'frontCoverFile' in tags:
            tags['frontCoverPicture'] = samePictureAs(tags['frontCoverFile'])
            del tags['frontCoverFile']

        audioFile = self.openMp3(name)
        assert_that(audioFile, has_properties(tags))


def readContent(filename):
    return open(filename, "rb").read()


def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]


def samePictureAs(filename):
    return contains(equal_to(guessMimeType(filename)),
                    has_length(len(readContent(filename))))


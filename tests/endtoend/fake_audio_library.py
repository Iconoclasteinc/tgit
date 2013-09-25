# -*- coding: utf-8 -*-

from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to

from tests.util.mp3_builder import MP3

from tgit.mp3 import MP3File


def readContent(filename):
    return open(filename, "rb").read()


# This is very rudimentary as of now
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
        audioFile = self.openMp3(name)

        assert_that(audioFile.releaseName, equal_to(tags['releaseName']),
                    "audio file release name")
        assert_that(audioFile.leadPerformer, equal_to(tags['leadPerformer']),
                    "audio file lead performer")
        assert_that(audioFile.originalReleaseDate, equal_to(tags['originalReleaseDate']),
                    "audio file original release date")
        assert_that(audioFile.upc, equal_to(tags['upc']),
                    "audio file UPC")
        assert_that(audioFile.trackTitle, equal_to(tags['trackTitle']),
                    "audio file track title")
        assert_that(audioFile.versionInfo, equal_to(tags['versionInfo']),
                    "audio file version information")
        assert_that(audioFile.featuredGuest, equal_to(tags['featuredGuest']),
                    "audio file featured guest")
        assert_that(audioFile.isrc, equal_to(tags['isrc']),
                    "audio file ISRC")
        frontCoverMimeType, frontCoverData = audioFile.frontCoverPicture
        assert_that(len(frontCoverData),
                    equal_to(len(readContent(tags['frontCoverPicture']))),
                    "audio file front cover picture size in bytes")


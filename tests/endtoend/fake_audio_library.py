# -*- coding: utf-8 -*-

import shutil
from tempfile import NamedTemporaryFile
from hamcrest.core.assert_that import assert_that
from hamcrest.core.core.isequal import equal_to

from tgit.mp3 import MP3File


FRONT_COVER_PICTURE = 'frontCoverPicture'
ISRC = 'isrc'
FEATURED_GUEST = 'featuredGuest'
VERSION_INFO = 'versionInfo'
TRACK_TITLE = 'trackTitle'
UPC = 'upc'
ORIGINAL_RELEASE_DATE = 'originalReleaseDate'
LEAD_PERFORMER = 'leadPerformer'
RELEASE_NAME = 'releaseName'


# This is very rudimentary as of now
class FakeAudioLibrary(object):
    def __init__(self):
        self._files = []

    def addFile(self, filename):
        importedFile = NamedTemporaryFile(suffix='.mp3')
        self._files.append(importedFile)
        shutil.copy(filename, importedFile.name)
        return importedFile.name

    def destroy(self):
        [f.close() for f in self._files]

    def hasFileWithMetadata(self, name, **tags):
        try:
            audioFile = MP3File(name)
        except IOError:
            raise AssertionError("Audio library contains no file " + name)

        assert_that(audioFile.releaseName, equal_to(tags[RELEASE_NAME]),
                    "audio file release name")
        assert_that(audioFile.leadPerformer, equal_to(tags[LEAD_PERFORMER]),
                    "audio file lead performer")
        assert_that(audioFile.originalReleaseDate, equal_to(tags[ORIGINAL_RELEASE_DATE]),
                    "audio file original release date")
        assert_that(audioFile.upc, equal_to(tags[UPC]),
                    "audio file UPC")
        assert_that(audioFile.trackTitle, equal_to(tags[TRACK_TITLE]),
                    "audio file track title")
        assert_that(audioFile.versionInfo, equal_to(tags[VERSION_INFO]),
                    "audio file version information")
        assert_that(audioFile.featuredGuest, equal_to(tags[FEATURED_GUEST]),
                    "audio file featured guest")
        assert_that(audioFile.isrc, equal_to(tags[ISRC]),
                    "audio file ISRC")
        frontCoverMimeType, frontCoverData = audioFile.frontCoverPicture
        assert_that(len(frontCoverData),
                    equal_to(len(self._fileContent(tags[FRONT_COVER_PICTURE]))),
                    "audio file front cover picture size in bytes")

    def _fileContent(self, filename):
        return open(filename).read()

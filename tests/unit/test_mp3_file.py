# -*- coding: utf-8 -*-

import shutil
from tempfile import NamedTemporaryFile
import unittest

from hamcrest import *

import mutagen.mp3 as mp3
import mutagen.id3 as id3

from tests.util import project

from tgit.mp3 import MP3File

SAMPLE_MP3_FILE = project.testResourcePath("base.mp3")
FRONT_COVER_PICTURE_FILE = project.testResourcePath("front-cover-sample.jpg")
OTHER_FRONT_COVER_PICTURE_FILE = project.testResourcePath("banana-song-cover.png")
BACK_COVER_PICTURE_FILE = project.testResourcePath("back-cover-sample.jpg")

RELEASE_NAME = u"Release Name"
LEAD_PERFORMER = u"Lead Performer"
ORIGINAL_RELEASE_DATE = u"2013-11-15"
UPC = u"123456789999"
TRACK_TITLE = u"Track Title"
VERSION_INFO = u"Version Info"
FEATURED_GUEST = u"Featured Guest"
ISRC = u"AABB12345678"
BITRATE_IN_BPS = 320000
BITRATE_IN_KBPS = 320
DURATION_IN_S = 9.064475
DURATION_AS_TEXT = "00:09"

UTF_8 = 3


def imageData(filename):
    return open(filename, "rb").read()


class MP3FileTest(unittest.TestCase):
    def setUp(self):
        self._createTestMp3(releaseName=RELEASE_NAME,
                            frontCoverPicture=('image/jpeg', FRONT_COVER_PICTURE_FILE),
                            backCoverPicture=('image/jpeg', BACK_COVER_PICTURE_FILE),
                            leadPerformer=LEAD_PERFORMER,
                            originalReleaseDate=ORIGINAL_RELEASE_DATE,
                            upc=UPC,
                            trackTitle=TRACK_TITLE,
                            versionInfo=VERSION_INFO,
                            featuredGuest=FEATURED_GUEST,
                            isrc=ISRC)
        self.audio = MP3File(self.workingFile.name)

    def tearDown(self):
        self._deleteTestMp3()

    @unittest.skip("Pending")
    def testRemovesTheExistingFrontCoverWhenNoneIsProvided(self):
        self.fail("Not implemented")

    @unittest.skip("Pending")
    def testIgnoresMissingTags(self):
        self.fail("Not implemented")

    @unittest.skip("pending")
    def testCreatesMp3TagsWhenMissing(self):
        self.fail("Not implemented")

    @unittest.skip("pending")
    def testJoinsAllTextsOfFrames(self):
        self.fail("Not implemented")

    def testReadsReleaseNameFromId3Tags(self):
        assert_that(self.audio.releaseName, equal_to(RELEASE_NAME), "release name")

    def testReadsFrontCoverPictureFromId3Tags(self):
        mime, data = self.audio.frontCoverPicture
        assert_that(mime, equal_to('image/jpeg'), "front cover mime type")
        assert_that(len(data), equal_to(len(imageData(FRONT_COVER_PICTURE_FILE))),
                    "front cover picture size in bytes")

    @unittest.skip("Pending")
    def testRecordsASingleFrontCoverPicture(self):
        self.fail("Not implemented")
        # test with a front cover without a description
        # test with a front cover with the same description

    @unittest.skip("Pending")
    def testLeavesOtherAttachedPicturesUnchanged(self):
        self.fail("Not implemented")
        # test with a other attached pictures with or without a description

    def testReadsLeadPerformerFromId3Tags(self):
        assert_that(self.audio.leadPerformer, equal_to(LEAD_PERFORMER), "lead performer")

    def testReadsOriginalReleaseDateFromId3Tags(self):
        assert_that(self.audio.originalReleaseDate, equal_to(ORIGINAL_RELEASE_DATE),
                    "original release date")

    def testReadsUpcFromCustomId3Tag(self):
        assert_that(self.audio.upc, equal_to(UPC), "upc")

    def testReadsTrackTitleFromId3Tags(self):
        assert_that(self.audio.trackTitle, equal_to(TRACK_TITLE), "track title")

    def testReadsVersionInfoFromId3Tags(self):
        assert_that(self.audio.versionInfo, equal_to(VERSION_INFO), "version info")

    def testReadsFeaturedGuestFromCustomId3Tag(self):
        assert_that(self.audio.featuredGuest, equal_to(FEATURED_GUEST), "featured guest")

    def testReadsIsrcFromId3Tags(self):
        assert_that(self.audio.isrc, equal_to(ISRC), "isrc")

    def testReadsTrackBitrateFromAudioStreamInformation(self):
        assert_that(self.audio.bitrate, equal_to(BITRATE_IN_BPS), "bitrate")

    def testCanReportBitrateRoundedInKbps(self):
        assert_that(self.audio.bitrateInKbps, equal_to(BITRATE_IN_KBPS),
                    "bitrate in kbps")

    def testReadsTrackDurationFromAudioStreamInformation(self):
        assert_that(self.audio.duration, equal_to(DURATION_IN_S), "duration")

    def testCanReportDurationAsHumanReadableText(self):
        assert_that(self.audio.durationAsText, equal_to(DURATION_AS_TEXT),
                    "duration as text")

    # todo introduce a matcher for comparing all metadata
    # something like assert_that(modified_audio, same_metada_as(original_audio))
    # then test round tripping on several test data samples
    def testSavesMetadataBackToAudioFile(self):
        self.audio.releaseName = u"Modified Release Name"
        self.audio.frontCoverPicture = 'image/png', imageData(OTHER_FRONT_COVER_PICTURE_FILE)
        self.audio.leadPerformer = u"Modified Lead Performer"
        self.audio.originalReleaseDate = u"2013-12-01"
        self.audio.upc = u"987654321111"
        self.audio.trackTitle = u"Modified Track Title"
        self.audio.versionInfo = u"Modified Version Info"
        self.audio.featuredGuest = u"Modified Featured Guest"
        self.audio.isrc = u"ZZXX87654321"
        self.audio.save()

        modifiedAudio = MP3File(self.workingFile.name)
        assert_that(modifiedAudio.releaseName, equal_to("Modified Release Name"),
                    "modified release name")
        modified_mime, modified_cover_data = modifiedAudio.frontCoverPicture
        assert_that(modified_mime, equal_to('image/png'), "modified front cover mime type")
        assert_that(len(modified_cover_data),
                    equal_to(len(imageData(OTHER_FRONT_COVER_PICTURE_FILE))),
                    "modified front cover picture size in bytes")
        assert_that(modifiedAudio.leadPerformer, equal_to("Modified Lead Performer"),
                    "modified lead performer")
        assert_that(modifiedAudio.originalReleaseDate, equal_to("2013-12-01"),
                    "modified original release date")
        assert_that(modifiedAudio.upc, equal_to("987654321111"), "modified upc")
        assert_that(modifiedAudio.trackTitle, equal_to("Modified Track Title"),
                    "modified track title")
        assert_that(modifiedAudio.versionInfo, equal_to("Modified Version Info"),
                    "modified version info")
        assert_that(modifiedAudio.featuredGuest, equal_to("Modified Featured Guest"),
                    "modified featured guest")
        assert_that(modifiedAudio.isrc, equal_to("ZZXX87654321"), "modified isrc")

    def _createTestMp3(self, **tags):
        self._copyMasterFile(SAMPLE_MP3_FILE)
        self._populateTags(tags)

    def _copyMasterFile(self, masterFile):
        self.workingFile = NamedTemporaryFile(suffix='.mp3')
        shutil.copy(masterFile, self.workingFile.name)

    #todo we need to build different test data each test
    def _populateTags(self, tags):
        testMp3 = mp3.MP3(self.workingFile.name)
        testMp3.add_tags()
        testMp3.tags.add(id3.TALB(encoding=UTF_8, text=[tags['releaseName']]))
        testMp3.tags.add(id3.APIC(UTF_8, tags['backCoverPicture'][0], 4, 'Back Cover',
                                  imageData(tags['backCoverPicture'][1])))
        testMp3.tags.add(id3.APIC(UTF_8, tags['frontCoverPicture'][0], 3, '',
                                  imageData(tags['frontCoverPicture'][1])))
        testMp3.tags.add(id3.TPE1(encoding=UTF_8, text=tags['leadPerformer']))
        testMp3.tags.add(id3.TDOR(encoding=UTF_8, text=[id3.ID3TimeStamp(tags[
                                  'originalReleaseDate'])]))
        testMp3.tags.add(id3.TXXX(encoding=UTF_8, desc='UPC', text=tags['upc']))
        testMp3.tags.add(id3.TIT2(encoding=UTF_8, text=tags['trackTitle']))
        testMp3.tags.add(id3.TPE4(encoding=UTF_8, text=tags['versionInfo']))
        testMp3.tags.add(id3.TXXX(encoding=UTF_8, desc='Featured Guest',
                                  text=tags['featuredGuest']))
        testMp3.tags.add(id3.TSRC(encoding=UTF_8, text=tags['isrc']))
        testMp3.save()

    def _deleteTestMp3(self):
        self.workingFile.close()
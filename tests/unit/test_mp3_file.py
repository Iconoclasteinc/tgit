# -*- coding: utf-8 -*-

import os
import unittest
from hamcrest import *

from tests.util.mp3_builder import MP3, mp3Sample, readContent
from tests.util import resources
from tgit.mp3 import MP3File

OTHER_FRONT_COVER_PICTURE_FILE = resources.path("banana-song-cover.png")
BACK_COVER_PICTURE_FILE = resources.path("back-cover-sample.jpg")


def imageData(filename):
    return open(filename, "rb").read()


class MP3FileTest(unittest.TestCase):
    # def setUp(self):
        # self._audio = MP3(mp3Sample.path,
        #                   releaseName=u"Release Name",
        #                   frontCoverPicture=(
        #                   'image/jpeg', '', resources.path("front-cover-sample.jpg")),
        #                   backCoverPicture=('image/jpeg', 'Back', BACK_COVER_PICTURE_FILE),
        #                   leadPerformer=u"Lead Performer",
        #                   originalReleaseDate=ORIGINAL_RELEASE_DATE,
        #                   upc=UPC,
        #                   trackTitle=TRACK_TITLE,
        #                   versionInfo=VERSION_INFO,
        #                   featuredGuest=FEATURED_GUEST,
        #                   isrc=ISRC)
        # self.mp3 = MP3File(self._audio.name)

    def tearDown(self):
        self._audioFile.delete()

    def makeMp3(self, **tags):
        self._audioFile = MP3(mp3Sample.path, **tags)
        return self._audioFile.name

    def testIgnoresMissingTags(self):
        mp3 = MP3File(self.makeMp3())
        assert_that(mp3.releaseName, is_(None), "missing release name")

    def testReadsReleaseNameFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(releaseName='Release Name'))
        assert_that(mp3.releaseName, equal_to('Release Name'), "release name")

    def testJoinsAllTextsOfFrames(self):
        mp3 = MP3File(self.makeMp3(releaseName=['Release', 'Names']))
        assert_that(mp3.releaseName, equal_to('Release\x00Names'), "release names")

    def testCreatesMp3TagsWhenMissing(self):
        mp3 = MP3File(self.makeMp3())
        mp3.releaseName = 'Release Name'
        assert_that(mp3.releaseName, is_('Release Name'), "release name")

    def testReadsLeadPerformerFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(leadPerformer='Lead Performer'))
        assert_that(mp3.leadPerformer, equal_to('Lead Performer'), "lead performer")

    def testReadsFrontCoverPictureFromId3Tags(self):
        frontCover = ('image/jpeg', '', resources.path("front-cover-sample.jpg"))
        mp3 = MP3File(self.makeMp3(frontCover=frontCover))

        mime, data = mp3.frontCoverPicture
        assert_that(mime, equal_to('image/jpeg'), "front cover mime type")
        assert_that(len(data),
                    equal_to(len(readContent(resources.path("front-cover-sample.jpg")))),
                    "front cover picture size in bytes")

    def testRemovesExistingFrontCoverWhenSetToNone(self):
        mp3 = MP3File(self.makeMp3(frontCover=('image/jpeg', '',
                                               resources.path("front-cover-sample.jpg"))))
        mp3.frontCoverPicture = (None, None)
        mp3.save()

        reloaded = MP3File(mp3.filename)
        assert_that(reloaded.frontCoverPicture, is_((None, None)), "missing front cover")

    def testReadsOriginalReleaseDateFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(originalReleaseDate='2013-11-15'))
        assert_that(mp3.originalReleaseDate, equal_to('2013-11-15'), "original release date")

    def testReadsUpcFromCustomId3Tag(self):
        mp3 = MP3File(self.makeMp3(upc='1234567899999'))
        assert_that(mp3.upc, equal_to('1234567899999'), "upc")

    def testReadsTrackTitleFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(trackTitle='Track Title'))
        assert_that(mp3.trackTitle, equal_to("Track Title"), "track title")

    def testReadsVersionInfoFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(versionInfo='Version Info'))
        assert_that(mp3.versionInfo, equal_to("Version Info"), "version info")

    def testReadsFeaturedGuestFromCustomId3Tag(self):
        mp3 = MP3File(self.makeMp3(featuredGuest='Featured Guest'))
        assert_that(mp3.featuredGuest, equal_to("Featured Guest"), "featured guest")

    def testReadsIsrcFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(isrc='AABB12345678'))
        assert_that(mp3.isrc, equal_to('AABB12345678'), "isrc")

    def testReadsTrackBitrateFromAudioStreamInformation(self):
        mp3 = MP3File(self.makeMp3())
        assert_that(mp3.bitrate, equal_to(mp3Sample.bitrate), "bitrate")

    def testCanReportBitrateRoundedInKbps(self):
        mp3 = MP3File(self.makeMp3())
        assert_that(mp3.bitrateInKbps, equal_to(mp3Sample.bitrateInKbps), "bitrate in kbps")

    def testReadsTrackDurationFromAudioStreamInformation(self):
        mp3 = MP3File(self.makeMp3())
        assert_that(mp3.duration, equal_to(mp3Sample.duration), "duration")

    def testCanReportDurationAsHumanReadableText(self):
        mp3 = MP3File(self.makeMp3())
        assert_that(mp3.durationAsText, equal_to(mp3Sample.durationAsText), "duration as text")

    # todo introduce a matcher for comparing all metadata
    # something like assert_that(modified_audio, same_metada_as(original_audio))
    # then test round tripping on several test data samples
    def testCanSaveAndReloadMetadataInFile(self):
        self.mp3 = MP3File(self.makeMp3())

        self.mp3.releaseName = u"Modified Release Name"
        self.mp3.frontCoverPicture = 'image/png', imageData(OTHER_FRONT_COVER_PICTURE_FILE)
        self.mp3.leadPerformer = u"Modified Lead Performer"
        self.mp3.originalReleaseDate = u"2013-12-01"
        self.mp3.upc = u"987654321111"
        self.mp3.trackTitle = u"Modified Track Title"
        self.mp3.versionInfo = u"Modified Version Info"
        self.mp3.featuredGuest = u"Modified Featured Guest"
        self.mp3.isrc = u"ZZXX87654321"
        self.mp3.save()

        modifiedAudio = MP3File(self.mp3.filename)
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









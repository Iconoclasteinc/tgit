# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, is_, equal_to, has_properties

from tgit.mp3 import MP3File

from test.util.mp3_maker import MP3, mp3Sample
from test.util import resources, fs


class MP3FileTest(unittest.TestCase):
    def tearDown(self):
        self._audioFile.delete()

    def makeMp3(self, **tags):
        self._audioFile = MP3(mp3Sample.path, **tags).make()
        return self._audioFile.filename

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
        frontCover = ('image/jpeg', '', resources.path("front-cover.jpg"))
        mp3 = MP3File(self.makeMp3(frontCover=frontCover))

        mime, data = mp3.frontCoverPicture
        assert_that(mime, equal_to('image/jpeg'), "front cover mime type")
        assert_that(len(data),
                    equal_to(len(fs.readContent(resources.path("front-cover.jpg")))),
                    "front cover picture size in bytes")

    def testDoesNotConfuseFrontCoverWithOtherPictureTypes(self):
        backCover = ('image/jpeg', '', resources.path("back-cover.jpg"))
        mp3 = MP3File(self.makeMp3(backCover=backCover))

        assert_that(mp3.frontCoverPicture, is_((None, None)), "missing front cover")

    def testReadsGuestPerformersFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(guestPerformers='Guest Performers'))
        assert_that(mp3.guestPerformers, equal_to('Guest Performers'), "guest performers")

    def testReadsLabelNameFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(labelName='Label Name'))
        assert_that(mp3.labelName, equal_to('Label Name'), "label name")

    def testReadsRecordingTimeFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(recordingTime='2012-07-15'))
        assert_that(mp3.recordingTime, equal_to('2012-07-15'), "recording time")

    def testReadsReleaseTimeFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(releaseTime='2013-11-15'))
        assert_that(mp3.releaseTime, equal_to('2013-11-15'), "release time")

    def testReadsOriginalReleaseTimeFromId3Tags(self):
        mp3 = MP3File(self.makeMp3(originalReleaseTime='1999-03-15'))
        assert_that(mp3.originalReleaseTime, equal_to('1999-03-15'), "original release time")

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

    def testReadsTrackDurationFromAudioStreamInformation(self):
        mp3 = MP3File(self.makeMp3())
        assert_that(mp3.duration, equal_to(mp3Sample.duration), "duration")

    # todo create a dict of changes, change mp3 accordingly then check that reloaded file
    # has properties matching the changes
    def testCanSaveAndReloadMetadataInFile(self):
        mp3 = MP3File(self.makeMp3())
        mp3.releaseName = u"Release Name"
        mp3.frontCoverPicture = 'image/jpeg', fs.readContent(resources.path("salers.jpg"))
        mp3.leadPerformer = u"Lead Performer"
        mp3.guestPerformers = u"Guest Performers"
        mp3.labelName = u"Label Name"
        mp3.recordingTime = u"2012-07-01"
        mp3.releaseTime = u"2013-12-01"
        mp3.originalReleaseTime = u"1999-01-01"
        mp3.upc = u"987654321111"
        mp3.trackTitle = u"Track Title"
        mp3.versionInfo = u"Version Info"
        mp3.featuredGuest = u"Featured Guest"
        mp3.isrc = u"ZZXX87654321"

        self.assertCanBeSavedAndReloadedWithSameTags(mp3)

    def testRemovesExistingFrontCoverWhenSetToNone(self):
        mp3 = MP3File(self.makeMp3(frontCover=('image/jpeg', '',
                                               resources.path("front-cover.jpg"))))
        mp3.frontCoverPicture = (None, None)
        mp3.save()

        reloaded = MP3File(mp3.filename)
        assert_that(reloaded.frontCoverPicture, is_((None, None)), "removed front cover")

    def assertCanBeSavedAndReloadedWithSameTags(self, original):
        original.save()
        assert_that(MP3File(original.filename), sameTagsAs(original))


def sameTagsAs(other):
    return has_properties(releaseName=other.releaseName,
                          leadPerformer=other.leadPerformer,
                          guestPerformers=other.guestPerformers,
                          labelName=other.labelName,
                          recordingTime=other.recordingTime,
                          releaseTime=other.releaseTime,
                          originalReleaseTime=other.originalReleaseTime,
                          upc=other.upc,
                          isrc=other.isrc,
                          trackTitle=other.trackTitle,
                          versionInfo=other.versionInfo,
                          featuredGuest=other.featuredGuest,
                          frontCoverPicture=other.frontCoverPicture)


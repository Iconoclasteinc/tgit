# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, has_entry, contains_inanyorder, has_key, has_length)

from test.util.mp3 import makeMp3, TestMp3

from tgit import tags
from tgit.metadata import Metadata, Image
import tgit.mp3_file as mp3File

BITRATE = TestMp3.bitrate
DURATION = TestMp3.duration


class MP3FileTest(unittest.TestCase):

    def tearDown(self):
        if hasattr(self, 'testFile'):
            self.testFile.delete()

    def makeMp3(self, **tags):
        self.testFile = makeMp3(TestMp3.filename, **tags)
        return self.testFile.filename

    def testReadsAlbumTitleFromTALBFrame(self):
        mp3 = mp3File.load(self.makeMp3(TALB='Album'))
        assert_that(mp3.metadata, has_entry(tags.RELEASE_NAME, 'Album'), 'metadata')

    def testJoinsAllTextsOfFrames(self):
        mp3 = mp3File.load(self.makeMp3(TALB=['Album', 'Titles']))
        assert_that(mp3.metadata, has_entry(tags.RELEASE_NAME, 'Album\x00Titles'), 'metadata')

    def testReadsLeadPerformerFromTPE1Frame(self):
        mp3 = mp3File.load(self.makeMp3(TPE1='Lead Artist'))
        assert_that(mp3.metadata, has_entry(tags.LEAD_PERFORMER, 'Lead Artist'), 'metadata')

    def testReadsGuestPerformersFromTPE2Frame(self):
        mp3 = mp3File.load(self.makeMp3(TPE2='Band'))
        assert_that(mp3.metadata, has_entry(tags.GUEST_PERFORMERS, 'Band'), 'metadata')

    def testReadsLabelNameFromTOWNFrame(self):
        mp3 = mp3File.load(self.makeMp3(TOWN='Label Name'))
        assert_that(mp3.metadata, has_entry(tags.LABEL_NAME, 'Label Name'), 'metadata')

    def testReadsCatalogNumberFromCustomFrame(self):
        mp3 = mp3File.load(self.makeMp3(TXXX_CATALOG_NUMBER='123 456-1'))
        assert_that(mp3.metadata, has_entry(tags.CATALOG_NUMBER, '123 456-1'), 'metadata')

    def testReadsUpcFromCustomFrame(self):
        mp3 = mp3File.load(self.makeMp3(TXXX_UPC='1234567899999'))
        assert_that(mp3.metadata, has_entry(tags.UPC, '1234567899999'), 'metadata')

    def testReadsRecordingTimeFromTDRCFrame(self):
        mp3 = mp3File.load(self.makeMp3(TDRC='2012-07-15'))
        assert_that(mp3.metadata, has_entry(tags.RECORDING_TIME, '2012-07-15'), 'metadata')

    def testReadsReleaseTimeFromTDRLFrame(self):
        mp3 = mp3File.load(self.makeMp3(TDRL='2013-11-15'))
        assert_that(mp3.metadata, has_entry(tags.RELEASE_TIME, '2013-11-15'), 'metadata')

    def testReadsOriginalReleaseTimeFromTDORFrame(self):
        mp3 = mp3File.load(self.makeMp3(TDOR='1999-03-15'))
        assert_that(mp3.metadata, has_entry(tags.ORIGINAL_RELEASE_TIME, '1999-03-15'),
                    'metadata')

    def testReadsRecordingStudiosFromCustomFrame(self):
        mp3 = mp3File.load(self.makeMp3(TXXX_RECORDING_STUDIOS='Studio Name'))
        assert_that(mp3.metadata, has_entry(tags.RECORDING_STUDIOS, 'Studio Name'), 'metadata')

    def testReadsTrackTitleFromTIT2Frame(self):
        mp3 = mp3File.load(self.makeMp3(TIT2='Track Title'))
        assert_that(mp3.metadata, has_entry(tags.TRACK_TITLE, 'Track Title'), 'metadata')

    def testReadsVersionInfoFromTPE4Frame(self):
        mp3 = mp3File.load(self.makeMp3(TPE4='Version Info'))
        assert_that(mp3.metadata, has_entry(tags.VERSION_INFO, 'Version Info'), 'metadata')

    def testReadsFeaturedGuestFromCustomFrame(self):
        mp3 = mp3File.load(self.makeMp3(TXXX_FEATURED_GUEST='Featured Guest'))
        assert_that(mp3.metadata, has_entry(tags.FEATURED_GUEST, 'Featured Guest'), 'metadata')

    def testReadsIsrcFromTSRCFrame(self):
        mp3 = mp3File.load(self.makeMp3(TSRC='AABB12345678'))
        assert_that(mp3.metadata, has_entry(tags.ISRC, 'AABB12345678'), 'metadata')

    def testReadsBitrateFromAudioStreamInformation(self):
        mp3 = mp3File.load(self.makeMp3())
        assert_that(mp3.metadata, has_entry(tags.BITRATE, BITRATE), 'bitrate')

    def testReadsDurationFromAudioStreamInformation(self):
        mp3 = mp3File.load(self.makeMp3())
        assert_that(mp3.metadata, has_entry(tags.DURATION, DURATION), 'duration')

    def testReadsCoverPicturesFromAPICFrames(self):
        mp3 = mp3File.load(self.makeMp3(
            APIC_FRONT=('image/jpeg', 'Front', 'front-cover.jpg'),
            APIC_BACK=('image/jpeg', 'Back', 'back-cover.jpg')))

        assert_that(mp3.metadata.images, contains_inanyorder(
            Image('image/jpeg', 'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
            Image('image/jpeg', 'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
        ))

    def testCanSaveAndReloadMetadata(self):
        metadata = Metadata()
        metadata.addImage('image/jpeg', 'salers.jpg', Image.FRONT_COVER)
        metadata[tags.RELEASE_NAME] = u"Album"
        metadata[tags.LEAD_PERFORMER] = u"Lead Performer"
        metadata[tags.GUEST_PERFORMERS] = u"Guest Performers"
        metadata[tags.LABEL_NAME] = u"Label Name"
        metadata[tags.CATALOG_NUMBER] = u"123 456-1"
        metadata[tags.UPC] = u"987654321111"
        metadata[tags.RECORDING_TIME] = u"2012-07-01"
        metadata[tags.RELEASE_TIME] = u"2013-12-01"
        metadata[tags.ORIGINAL_RELEASE_TIME] = u"1999-01-01"
        metadata[tags.RECORDING_STUDIOS] = u'Studio Name'
        metadata[tags.TRACK_TITLE] = u"Track Title"
        metadata[tags.VERSION_INFO] = u"Version Info"
        metadata[tags.FEATURED_GUEST] = u"Featured Guest"
        metadata[tags.ISRC] = u"ZZXX87654321"
        metadata[tags.DURATION] = DURATION
        metadata[tags.BITRATE] = BITRATE

        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testCreatesID3TagsWhenMissing(self):
        mp3 = mp3File.load(self.makeMp3())
        mp3.metadata[tags.RELEASE_NAME] = 'Title'
        mp3.save()

        assert_that(reloadMetadata(mp3), has_key(tags.RELEASE_NAME), 'metadata')

    def testCanSaveSeveralPicturesSharingTheSameDescription(self):
        mp3 = mp3File.load(self.makeMp3())
        mp3.metadata.addImage('image/jpeg', 'salers.jpg', desc='Front Cover')
        mp3.metadata.addImage('image/jpeg', 'ragber.jpg', desc='Front Cover')
        mp3.save()

        assert_that(reloadMetadata(mp3).images, contains_inanyorder(
            Image('image/jpeg', 'salers.jpg', type_=Image.OTHER, desc='Front Cover'),
            Image('image/jpeg', 'ragber.jpg', type_=Image.OTHER, desc='Front Cover (2)'),
        ))

    def testRemovesExistingAttachedPicturesOnSave(self):
        mp3 = mp3File.load(self.makeMp3(APIC_FRONT=('image/jpeg', '', 'front-cover.jpg')))
        mp3.metadata.removeImages()
        mp3.save()
        assert_that(reloadMetadata(mp3).images, has_length(0), 'removed images')

        mp3.metadata.addImage(mime='image/jpeg', data='salers.jpg', desc='Front')
        mp3.save()
        assert_that(reloadMetadata(mp3).images, has_length(1), 'updated images')

    def assertCanBeSavedAndReloadedWithSameState(self, metadata):
        mp3 = mp3File.save(self.makeMp3(), metadata)

        assert_that(reloadMetadata(mp3).items(), contains_inanyorder(*metadata.items()),
                    'metadata items')
        assert_that(reloadMetadata(mp3).images, contains_inanyorder(*metadata.images),
                    'metadata images')


def reloadMetadata(mp3):
    return mp3File.load(mp3.filename).metadata
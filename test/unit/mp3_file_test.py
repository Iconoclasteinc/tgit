# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, has_entry, contains_inanyorder, has_key, has_length)

from tgit import album, track
from tgit.metadata import Metadata, Image
import tgit.mp3_file as mp3File

from test.util.mp3 import makeMp3, TestMp3

BITRATE = TestMp3.bitrate
DURATION = TestMp3.duration


class MP3FileTest(unittest.TestCase):
    def tearDown(self):
        self.testFile.delete()

    def makeMp3(self, **tags):
        self.testFile = makeMp3(TestMp3.filename, **tags)
        return self.testFile.filename

    def testReadsAlbumTitleFromTALBFrame(self):
        mp3 = mp3File.load(self.makeMp3(TALB='Album'))
        assert_that(mp3.metadata(), has_entry(album.TITLE, 'Album'), 'metadata')

    def testJoinsAllTextsOfFrames(self):
        mp3 = mp3File.load(self.makeMp3(TALB=['Album', 'Titles']))
        assert_that(mp3.metadata(), has_entry(album.TITLE, 'Album\x00Titles'), 'metadata')

    def testReadsLeadPerformerFromTPE1Frame(self):
        mp3 = mp3File.load(self.makeMp3(TPE1='Lead Artist'))
        assert_that(mp3.metadata(), has_entry(album.LEAD_PERFORMER, 'Lead Artist'), 'metadata')

    def testReadsGuestPerformersFromTPE2Frame(self):
        mp3 = mp3File.load(self.makeMp3(TPE2='Band'))
        assert_that(mp3.metadata(), has_entry(album.GUEST_PERFORMERS, 'Band'), 'metadata')

    def testReadsLabelNameFromTPUBFrame(self):
        mp3 = mp3File.load(self.makeMp3(TPUB='Label Name'))
        assert_that(mp3.metadata(), has_entry(album.LABEL_NAME, 'Label Name'), 'metadata')

    def testReadsRecordingTimeFromTDRCFrame(self):
        mp3 = mp3File.load(self.makeMp3(TDRC='2012-07-15'))
        assert_that(mp3.metadata(), has_entry(album.RECORDING_TIME, '2012-07-15'), 'metadata')

    def testReadsReleaseTimeFromTDRLFrame(self):
        mp3 = mp3File.load(self.makeMp3(TDRL='2013-11-15'))
        assert_that(mp3.metadata(), has_entry(album.RELEASE_TIME, '2013-11-15'), 'metadata')

    def testReadsOriginalReleaseTimeFromTDORFrame(self):
        mp3 = mp3File.load(self.makeMp3(TDOR='1999-03-15'))
        assert_that(mp3.metadata(), has_entry(album.ORIGINAL_RELEASE_TIME, '1999-03-15'),
                    'metadata')

    def testReadsUpcFromCustomFrame(self):
        mp3 = mp3File.load(self.makeMp3(TXXX_UPC='1234567899999'))
        assert_that(mp3.metadata(), has_entry(album.UPC, '1234567899999'), 'metadata')

    def testReadsTrackTitleFromTIT2Frame(self):
        mp3 = mp3File.load(self.makeMp3(TIT2='Track Title'))
        assert_that(mp3.metadata(), has_entry(track.TITLE, 'Track Title'), 'metadata')

    def testReadsVersionInfoFromTPE4Frame(self):
        mp3 = mp3File.load(self.makeMp3(TPE4='Version Info'))
        assert_that(mp3.metadata(), has_entry(track.VERSION_INFO, 'Version Info'), 'metadata')

    def testReadsFeaturedGuestFromCustomFrame(self):
        mp3 = mp3File.load(self.makeMp3(TXXX_FEATURED_GUEST='Featured Guest'))
        assert_that(mp3.metadata(), has_entry(track.FEATURED_GUEST, 'Featured Guest'), 'metadata')

    def testReadsIsrcFromTSRCFrame(self):
        mp3 = mp3File.load(self.makeMp3(TSRC='AABB12345678'))
        assert_that(mp3.metadata(), has_entry(track.ISRC, 'AABB12345678'), 'metadata')

    def testReadsBitrateFromAudioStreamInformation(self):
        mp3 = mp3File.load(self.makeMp3())
        assert_that(mp3.bitrate, equal_to(BITRATE), 'bitrate')

    def testReadsDurationFromAudioStreamInformation(self):
        mp3 = mp3File.load(self.makeMp3())
        assert_that(mp3.duration, equal_to(DURATION), 'duration')

    def testReadsCoverPicturesFromAPICFrames(self):
        mp3 = mp3File.load(self.makeMp3(
            APIC_FRONT=('image/jpeg', 'Front', 'front-cover.jpg'),
            APIC_BACK=('image/jpeg', 'Back', 'back-cover.jpg')))

        assert_that(mp3.metadata().images, contains_inanyorder(
            Image('image/jpeg', 'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
            Image('image/jpeg', 'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
        ))

    def testCanSaveAndReloadMetadata(self):
        metadata = Metadata()
        metadata.addImage('image/jpeg', 'salers.jpg', Image.FRONT_COVER)
        metadata[album.TITLE] = u"Album"
        metadata[album.LEAD_PERFORMER] = u"Lead Performer"
        metadata[album.GUEST_PERFORMERS] = u"Guest Performers"
        metadata[album.LABEL_NAME] = u"Label Name"
        metadata[album.RECORDING_TIME] = u"2012-07-01"
        metadata[album.RELEASE_TIME] = u"2013-12-01"
        metadata[album.ORIGINAL_RELEASE_TIME] = u"1999-01-01"
        metadata[album.UPC] = u"987654321111"
        metadata[track.TITLE] = u"Track Title"
        metadata[track.VERSION_INFO] = u"Version Info"
        metadata[track.FEATURED_GUEST] = u"Featured Guest"
        metadata[track.ISRC] = u"ZZXX87654321"

        self.assertCanBeSavedAndReloadedWithSameMetadata(metadata)

    def testCreatesID3TagsWhenMissing(self):
        withoutTags = mp3File.load(self.makeMp3())
        metadata = Metadata()
        metadata[album.TITLE] = 'Title'
        withoutTags.save(metadata)

        assert_that(reload_(withoutTags).metadata(), has_key(album.TITLE), 'metadata')

    def testCanSaveSeveralPicturesSharingTheSameDescription(self):
        mp3 = mp3File.load(self.makeMp3())
        metadata = Metadata()
        metadata.addImage('image/jpeg', 'salers.jpg', desc='Front Cover')
        metadata.addImage('image/jpeg', 'ragber.jpg', desc='Front Cover')
        mp3.save(metadata)

        assert_that(reload_(mp3).metadata().images, contains_inanyorder(
            Image('image/jpeg', 'salers.jpg', type_=Image.OTHER, desc='Front Cover'),
            Image('image/jpeg', 'ragber.jpg', type_=Image.OTHER, desc='Front Cover (2)'),
        ))

    def testRemovesExistingAttachedPicturesOnSave(self):
        mp3 = mp3File.load(self.makeMp3(APIC_FRONT=('image/jpeg', '', 'front-cover.jpg')))
        mp3.save(Metadata())
        assert_that(reload_(mp3).metadata().images, has_length(0), 'removed images')

        metadata = Metadata()
        metadata.addImage(mime='image/jpeg', data='salers.jpg', desc='Front')
        mp3.save(metadata)
        assert_that(reload_(mp3).metadata().images, has_length(1), 'updated images')

    def assertCanBeSavedAndReloadedWithSameMetadata(self, metadata):
        mp3 = mp3File.load(self.makeMp3())
        mp3.save(metadata)

        assert_that(reload_(mp3).metadata().items(), contains_inanyorder(*metadata.items()),
                    'metadata items')
        assert_that(reload_(mp3).metadata().images, contains_inanyorder(*metadata.images),
                    'metadata images')


def reload_(mp3):
    return mp3File.load(mp3.filename)
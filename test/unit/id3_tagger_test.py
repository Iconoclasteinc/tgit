# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, has_entry, has_items, has_key, has_length, contains,
                      is_not, contains_inanyorder)

from test.util.mp3_file import makeMp3, TestMp3

from tgit import tags
from tgit.metadata import Metadata, Image
import tgit.id3_tagger as tagger

BITRATE = TestMp3.bitrate
DURATION = TestMp3.duration


class Id3TaggerTest(unittest.TestCase):

    def tearDown(self):
        self.mp3.delete()

    def makeMp3(self, **tags):
        self.mp3 = makeMp3(TestMp3.filename, **tags)
        return self.mp3.filename

    def testReadsAlbumTitleFromTALBFrame(self):
        metadata = tagger.load(self.makeMp3(TALB='Album'))
        assert_that(metadata, has_entry(tags.RELEASE_NAME, 'Album'), 'metadata')

    def testJoinsAllTextsOfFrames(self):
        metadata = tagger.load(self.makeMp3(TALB=['Album', 'Titles']))
        assert_that(metadata, has_entry(tags.RELEASE_NAME, 'Album\x00Titles'), 'metadata')

    def testReadsLeadPerformerFromTPE1Frame(self):
        metadata = tagger.load(self.makeMp3(TPE1='Lead Artist'))
        assert_that(metadata, has_entry(tags.LEAD_PERFORMER, 'Lead Artist'), 'metadata')

    def testReadsGuestPerformersFromTMCLFrame(self):
        metadata = tagger.load(self.makeMp3(TMCL=[['Guitar', 'Guitarist'], ['Guitar', 'Bassist'],
                                              ['Piano','Pianist']]))
        assert_that(metadata, has_entry(tags.GUEST_PERFORMERS, contains_inanyorder(
                                                ('Guitar', 'Guitarist'),
                                                ('Guitar', 'Bassist'),
                                                ('Piano', 'Pianist'))), 'metadata')

    def testIgnoresTMCLEntriesWithBlankNames(self):
        metadata = tagger.load(self.makeMp3(TMCL=[['Guitar', 'Guitarist'], ['Piano', '']]))
        assert_that(metadata, has_entry(tags.GUEST_PERFORMERS,
                                            contains(('Guitar', 'Guitarist'))), 'metadata')

    def testReadsLabelNameFromTOWNFrame(self):
        metadata = tagger.load(self.makeMp3(TOWN='Label Name'))
        assert_that(metadata, has_entry(tags.LABEL_NAME, 'Label Name'), 'metadata')

    def testReadsCatalogNumberFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_CATALOG_NUMBER='123 456-1'))
        assert_that(metadata, has_entry(tags.CATALOG_NUMBER, '123 456-1'), 'metadata')

    def testReadsUpcFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_UPC='1234567899999'))
        assert_that(metadata, has_entry(tags.UPC, '1234567899999'), 'metadata')

    def testReadsRecordingTimeFromTDRCFrame(self):
        metadata = tagger.load(self.makeMp3(TDRC='2012-07-15'))
        assert_that(metadata, has_entry(tags.RECORDING_TIME, '2012-07-15'), 'metadata')

    def testReadsReleaseTimeFromTDRLFrame(self):
        metadata = tagger.load(self.makeMp3(TDRL='2013-11-15'))
        assert_that(metadata, has_entry(tags.RELEASE_TIME, '2013-11-15'), 'metadata')

    def testReadsOriginalReleaseTimeFromTDORFrame(self):
        metadata = tagger.load(self.makeMp3(TDOR='1999-03-15'))
        assert_that(metadata, has_entry(tags.ORIGINAL_RELEASE_TIME, '1999-03-15'),
                    'metadata')

    def testReadsRecordingStudiosFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_RECORDING_STUDIOS='Studio Name'))
        assert_that(metadata, has_entry(tags.RECORDING_STUDIOS, 'Studio Name'), 'metadata')

    def testReadsArtisticProducerFromTIPLFrame(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['producer', 'Artistic Producer']]))
        assert_that(metadata, has_entry(tags.PRODUCER, 'Artistic Producer'), 'metadata')

    def testTakesIntoAccountLastOfMultipleRoleDefinitions(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['producer', 'first'], ['producer', 'last']]))
        assert_that(metadata, has_entry(tags.PRODUCER, 'last'), 'metadata')

    def testIgnoresTPILEntriesWithBlankNames(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['producer', '']]))
        assert_that(metadata, is_not(has_key(tags.PRODUCER)), 'metadata')

    def testReadsMixingEngineerFromTIPLFrame(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['mix', 'Mixing Engineer']]))
        assert_that(metadata, has_entry(tags.MIXER, 'Mixing Engineer'), 'metadata')

    def testReadsTrackTitleFromTIT2Frame(self):
        metadata = tagger.load(self.makeMp3(TIT2='Track Title'))
        assert_that(metadata, has_entry(tags.TRACK_TITLE, 'Track Title'), 'metadata')

    def testReadsVersionInfoFromTPE4Frame(self):
        metadata = tagger.load(self.makeMp3(TPE4='Version Info'))
        assert_that(metadata, has_entry(tags.VERSION_INFO, 'Version Info'), 'metadata')

    def testReadsFeaturedGuestFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_FEATURED_GUEST='Featured Guest'))
        assert_that(metadata, has_entry(tags.FEATURED_GUEST, 'Featured Guest'), 'metadata')

    def testReadsLyricistFromTEXTFrame(self):
        metadata = tagger.load(self.makeMp3(TEXT='Lyricist'))
        assert_that(metadata, has_entry(tags.LYRICIST, 'Lyricist'), 'metadata')

    def testReadsComposerFromTCOMFrame(self):
        metadata = tagger.load(self.makeMp3(TCOM='Composer'))
        assert_that(metadata, has_entry(tags.COMPOSER, 'Composer'), 'metadata')

    def testReadsPublisherFromTPUBFrame(self):
        metadata = tagger.load(self.makeMp3(TPUB='Publisher'))
        assert_that(metadata, has_entry(tags.PUBLISHER, 'Publisher'), 'metadata')

    def testReadsIsrcFromTSRCFrame(self):
        metadata = tagger.load(self.makeMp3(TSRC='AABB12345678'))
        assert_that(metadata, has_entry(tags.ISRC, 'AABB12345678'), 'metadata')

    def testReadsBitrateFromAudioStreamInformation(self):
        metadata = tagger.load(self.makeMp3())
        assert_that(metadata, has_entry(tags.BITRATE, BITRATE), 'bitrate')

    def testReadsDurationFromAudioStreamInformation(self):
        metadata = tagger.load(self.makeMp3())
        assert_that(metadata, has_entry(tags.DURATION, DURATION), 'duration')

    def testReadsCoverPicturesFromAPICFrames(self):
        metadata = tagger.load(self.makeMp3(
            APIC_FRONT=('image/jpeg', 'Front', 'front-cover.jpg'),
            APIC_BACK=('image/jpeg', 'Back', 'back-cover.jpg')))

        assert_that(metadata.images, contains_inanyorder(
            Image('image/jpeg', 'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
            Image('image/jpeg', 'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
        ))

    def testRoundTripsMetadataToFile(self):
        metadata = Metadata()
        metadata.addImage('image/jpeg', 'salers.jpg', Image.FRONT_COVER)
        metadata[tags.RELEASE_NAME] = u'Album'
        metadata[tags.LEAD_PERFORMER] = u'Lead Performer'
        metadata[tags.GUEST_PERFORMERS] = [
            ('Guitar', 'Guitarist'), ('Guitar', 'Bassist'), ('Piano', 'Pianist')
        ]
        metadata[tags.LABEL_NAME] = u'Label Name'
        metadata[tags.CATALOG_NUMBER] = u'123 456-1'
        metadata[tags.UPC] = u'987654321111'
        metadata[tags.RECORDING_TIME] = u'2012-07-01'
        metadata[tags.RELEASE_TIME] = u'2013-12-01'
        metadata[tags.ORIGINAL_RELEASE_TIME] = u'1999-01-01'
        metadata[tags.RECORDING_STUDIOS] = u'Studio Name'
        metadata[tags.PRODUCER] = u'Artistic Producer'
        metadata[tags.MIXER] = u'Mixing Engineer'
        metadata[tags.CONTRIBUTORS] = [('recording', 'Recording Eng.'),
                                 ('mastering', 'Mastering Eng.'),
                                 ('recording', 'Assistant Recording Eng.')]
        metadata[tags.TRACK_TITLE] = u'Track Title'
        metadata[tags.VERSION_INFO] = u'Version Info'
        metadata[tags.FEATURED_GUEST] = u'Featured Guest'
        metadata[tags.LYRICIST] = u'Lyricist'
        metadata[tags.COMPOSER] = u'Composer'
        metadata[tags.PUBLISHER] = u'Publisher'
        metadata[tags.ISRC] = u'ZZXX87654321'

        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testRemovesID3TagWhenNotInMetadata(self):
        filename = self.makeMp3(TALB='Album',
                                TMCL=[['Guitar', 'Guitarist']],
                                TIPL=[['mix', 'Mixing Engineer']])

        tagger.save(filename, Metadata())

        assert_that(load(filename), has_length(len(['bitrate', 'duration'])), 'metadata')

    def testCanSaveSeveralPicturesSharingTheSameDescription(self):
        filename = self.makeMp3()
        metadata = tagger.load(filename)
        metadata.addImage('image/jpeg', 'salers.jpg', desc='Front Cover')
        metadata.addImage('image/jpeg', 'ragber.jpg', desc='Front Cover')
        tagger.save(filename, metadata)

        assert_that(load(filename).images, contains_inanyorder(
            Image('image/jpeg', 'salers.jpg', type_=Image.OTHER, desc='Front Cover'),
            Image('image/jpeg', 'ragber.jpg', type_=Image.OTHER, desc='Front Cover (2)'),
        ))

    def testRemovesExistingAttachedPicturesOnSave(self):
        filename = self.makeMp3(APIC_FRONT=('image/jpeg', '', 'front-cover.jpg'))
        metadata = tagger.load(filename)
        metadata.removeImages()

        tagger.save(filename, metadata)
        assert_that(load(filename).images, has_length(0), 'removed images')

        metadata.addImage(mime='image/jpeg', data='salers.jpg', desc='Front')
        tagger.save(filename, metadata)

        assert_that(load(filename).images, has_length(1), 'updated images')

    def assertCanBeSavedAndReloadedWithSameState(self, metadata):
        filename = self.makeMp3()
        tagger.save(filename, metadata.copy())

        assert_that(load(filename).items(), has_items(*metadata.items()),
                    'metadata items')
        assert_that(load(filename).images, has_items(*metadata.images),
                    'metadata images')


def load(filename):
    return tagger.load(filename)
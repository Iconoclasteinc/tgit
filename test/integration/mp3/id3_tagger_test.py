# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, has_entry, has_items, has_key, has_length, contains,
                      is_not, contains_inanyorder)

from test.util import mp3_file as mp3

from tgit import tag
from tgit.metadata import Metadata, Image
import tgit.mp3.id3_tagger as tagger

BITRATE = mp3.Base.bitrate
DURATION = mp3.Base.duration


# todo introduce dedicated focused tests for the processors?
class ID3TaggerTest(unittest.TestCase):
    def tearDown(self):
        self.mp3.delete()

    def makeMp3(self, **tags):
        self.mp3 = mp3.make(**tags)
        return self.mp3.filename

    def testReadsAlbumTitleFromTALBFrame(self):
        metadata = tagger.load(self.makeMp3(TALB='Album'))
        assert_that(metadata, has_entry(tag.RELEASE_NAME, 'Album'), 'metadata')

    def testJoinsAllTextsOfFrames(self):
        metadata = tagger.load(self.makeMp3(TALB=['Album', 'Titles']))
        assert_that(metadata, has_entry(tag.RELEASE_NAME, 'Album\x00Titles'), 'metadata')

    def testReadsLeadPerformerFromTPE1Frame(self):
        metadata = tagger.load(self.makeMp3(TPE1='Lead Artist'))
        assert_that(metadata, has_entry(tag.LEAD_PERFORMER, 'Lead Artist'), 'metadata')

    def testReadsGuestPerformersFromTMCLFrame(self):
        metadata = tagger.load(self.makeMp3(TMCL=[['Guitar', 'Guitarist'], ['Guitar', 'Bassist'],
                                                  ['Piano', 'Pianist']]))
        assert_that(metadata, has_entry(tag.GUEST_PERFORMERS, contains_inanyorder(
            ('Guitar', 'Guitarist'),
            ('Guitar', 'Bassist'),
            ('Piano', 'Pianist'))), 'metadata')

    def testIgnoresTMCLEntriesWithBlankNames(self):
        metadata = tagger.load(self.makeMp3(TMCL=[['Guitar', 'Guitarist'], ['Piano', '']]))
        assert_that(metadata, has_entry(tag.GUEST_PERFORMERS,
                                        contains(('Guitar', 'Guitarist'))), 'metadata')

    def testReadsLabelNameFromTOWNFrame(self):
        metadata = tagger.load(self.makeMp3(TOWN='Label Name'))
        assert_that(metadata, has_entry(tag.LABEL_NAME, 'Label Name'), 'metadata')

    def testReadsCatalogNumberFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_CATALOG_NUMBER='123 456-1'))
        assert_that(metadata, has_entry(tag.CATALOG_NUMBER, '123 456-1'), 'metadata')

    def testReadsUpcFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_UPC='1234567899999'))
        assert_that(metadata, has_entry(tag.UPC, '1234567899999'), 'metadata')

    def testReadsRecordingTimeFromTDRCFrame(self):
        metadata = tagger.load(self.makeMp3(TDRC='2012-07-15'))
        assert_that(metadata, has_entry(tag.RECORDING_TIME, '2012-07-15'), 'metadata')

    def testReadsReleaseTimeFromTDRLFrame(self):
        metadata = tagger.load(self.makeMp3(TDRL='2013-11-15'))
        assert_that(metadata, has_entry(tag.RELEASE_TIME, '2013-11-15'), 'metadata')

    def testReadsOriginalReleaseTimeFromTDORFrame(self):
        metadata = tagger.load(self.makeMp3(TDOR='1999-03-15'))
        assert_that(metadata, has_entry(tag.ORIGINAL_RELEASE_TIME, '1999-03-15'),
                    'metadata')

    def testReadsRecordingStudiosFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_RECORDING_STUDIOS='Studio Name'))
        assert_that(metadata, has_entry(tag.RECORDING_STUDIOS, 'Studio Name'), 'metadata')

    def testReadsArtisticProducerFromTIPLFrame(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['producer', 'Artistic Producer']]))
        assert_that(metadata, has_entry(tag.PRODUCER, 'Artistic Producer'), 'metadata')

    def testTakesIntoAccountLastOfMultipleRoleDefinitions(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['producer', 'first'], ['producer', 'last']]))
        assert_that(metadata, has_entry(tag.PRODUCER, 'last'), 'metadata')

    def testIgnoresTPILEntriesWithBlankNames(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['producer', '']]))
        assert_that(metadata, is_not(has_key(tag.PRODUCER)), 'metadata')

    def testReadsMixingEngineerFromTIPLFrame(self):
        metadata = tagger.load(self.makeMp3(TIPL=[['mix', 'Mixing Engineer']]))
        assert_that(metadata, has_entry(tag.MIXER, 'Mixing Engineer'), 'metadata')

    def testReadsCommentsFromFrenchCOMMFrame(self):
        metadata = tagger.load(self.makeMp3(COMM=('Comments', 'fra')))
        assert_that(metadata, has_entry(tag.COMMENTS, 'Comments'), 'metadata')

    def testReadsTrackTitleFromTIT2Frame(self):
        metadata = tagger.load(self.makeMp3(TIT2='Track Title'))
        assert_that(metadata, has_entry('trackTitle', 'Track Title'), 'metadata')

    def testReadsVersionInfoFromTPE4Frame(self):
        metadata = tagger.load(self.makeMp3(TPE4='Version Info'))
        assert_that(metadata, has_entry('versionInfo', 'Version Info'), 'metadata')

    def testReadsFeaturedGuestFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_FEATURED_GUEST='Featured Guest'))
        assert_that(metadata, has_entry('featuredGuest', 'Featured Guest'), 'metadata')

    def testReadsLyricistFromTEXTFrame(self):
        metadata = tagger.load(self.makeMp3(TEXT='Lyricist'))
        assert_that(metadata, has_entry('lyricist', 'Lyricist'), 'metadata')

    def testReadsComposerFromTCOMFrame(self):
        metadata = tagger.load(self.makeMp3(TCOM='Composer'))
        assert_that(metadata, has_entry('composer', 'Composer'), 'metadata')

    def testReadsPublisherFromTPUBFrame(self):
        metadata = tagger.load(self.makeMp3(TPUB='Publisher'))
        assert_that(metadata, has_entry('publisher', 'Publisher'), 'metadata')

    def testReadsIsrcFromTSRCFrame(self):
        metadata = tagger.load(self.makeMp3(TSRC='AABB12345678'))
        assert_that(metadata, has_entry('isrc', 'AABB12345678'), 'metadata')

    def testReadsTagsFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_TAGS='Tag1 Tag2 Tag3'))
        assert_that(metadata, has_entry('labels', 'Tag1 Tag2 Tag3'), 'metadata')

    def testReadsLyricsFromUSLTFrenchFrame(self):
        metadata = tagger.load(self.makeMp3(USLT=('Lyrics', 'fra')))
        assert_that(metadata, has_entry('lyrics', 'Lyrics'), 'metadata')

    def testReadsLanguageFromTLANFrame(self):
        metadata = tagger.load(self.makeMp3(TLAN='fra'))
        assert_that(metadata, has_entry('language', 'fra'), 'metadata')

    def testReadsPrimaryStyleFromTCONFrame(self):
        metadata = tagger.load(self.makeMp3(TCON='Jazz'))
        assert_that(metadata, has_entry(tag.PRIMARY_STYLE, 'Jazz'), 'metadata')

    def testReadsCompilationFlagFromNonStandardTCMPFlag(self):
        metadata = tagger.load(self.makeMp3(TCMP='0'))
        assert_that(metadata, has_entry(tag.COMPILATION, False), 'metadata')
        metadata = tagger.load(self.makeMp3(TCMP='1'))
        assert_that(metadata, has_entry(tag.COMPILATION, True), 'metadata')

    def testReadsBitrateFromAudioStreamInformation(self):
        metadata = tagger.load(self.makeMp3())
        assert_that(metadata, has_entry('bitrate', BITRATE), 'bitrate')

    def testReadsDurationFromAudioStreamInformation(self):
        metadata = tagger.load(self.makeMp3())
        assert_that(metadata, has_entry('duration', DURATION), 'duration')

    def testReadsCoverPicturesFromAPICFrames(self):
        metadata = tagger.load(self.makeMp3(
            APIC_FRONT=('image/jpeg', 'Front', 'front-cover.jpg'),
            APIC_BACK=('image/jpeg', 'Back', 'back-cover.jpg')))

        assert_that(metadata.images, contains_inanyorder(
            Image('image/jpeg', 'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
            Image('image/jpeg', 'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
        ))

    def testReadsTaggerFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_TAGGER='TGiT v1.0'))
        assert_that(metadata, has_entry('tagger', 'TGiT v1.0'), 'metadata')

    def testReadsTaggingTimeFromCustomFrame(self):
        metadata = tagger.load(self.makeMp3(TXXX_TAGGING_TIME='2014-03-26 14:18:55 EDT-0400'))
        assert_that(metadata, has_entry('taggingTime', '2014-03-26 14:18:55 EDT-0400'), 'metadata')

    def testRoundTripsEmptyMetadataToFile(self):
        metadata = Metadata()
        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testRoundTripsMetadataToFile(self):
        metadata = Metadata()
        metadata.addImage('image/jpeg', 'salers.jpg', Image.FRONT_COVER)
        metadata[tag.RELEASE_NAME] = u'Album'
        metadata[tag.COMPILATION] = True
        metadata['leadPerformer'] = u'Lead Performer'
        metadata[tag.GUEST_PERFORMERS] = [
            ('Guitar', 'Guitarist'), ('Guitar', 'Bassist'), ('Piano', 'Pianist')
        ]
        metadata[tag.LABEL_NAME] = u'Label Name'
        metadata[tag.CATALOG_NUMBER] = u'123 456-1'
        metadata[tag.UPC] = u'987654321111'
        metadata[tag.RECORDING_TIME] = u'2012-07-01'
        metadata[tag.RELEASE_TIME] = u'2013-12-01'
        metadata[tag.ORIGINAL_RELEASE_TIME] = u'1999-01-01'
        metadata[tag.RECORDING_STUDIOS] = u'Studio Name'
        metadata[tag.PRODUCER] = u'Artistic Producer'
        metadata[tag.MIXER] = u'Mixing Engineer'
        metadata[tag.CONTRIBUTORS] = [('recording', 'Recording Eng.'),
                                       ('mastering', 'Mastering Eng.'),
                                       ('recording', 'Assistant Recording Eng.')]
        metadata[tag.COMMENTS] = u'Comments'
        metadata[tag.PRIMARY_STYLE] = u'Jazz'
        metadata['trackTitle'] = u'Track Title'
        metadata['versionInfo'] = u'Version Info'
        metadata['featuredGuest'] = u'Featured Guest'
        metadata['lyricist'] = u'Lyricist'
        metadata['composer'] = u'Composer'
        metadata['publisher'] = u'Publisher'
        metadata['isrc'] = u'ZZXX87654321'
        metadata['labels'] = u'Tag1 Tag2 Tag3'
        metadata['lyrics'] = u'Lyrics'
        metadata['language'] = u'fra'
        metadata['tagger'] = u'TGiT v1.0'
        metadata['taggingTime'] = u'2014-03-26 14:18:55 EDT-0400'
        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testHandlesUnicodeMetadata(self):
        metadata = Metadata()
        metadata[tag.RELEASE_NAME] = u'Titre en Français'
        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testRemovesFrameWhenTagNotInMetadata(self):
        filename = self.makeMp3(TALB='Album',
                                TMCL=[['Guitar', 'Guitarist']],
                                TIPL=[['mix', 'Mixing Engineer']],
                                USLT=('', 'fra'))

        tagger.save(filename, Metadata())
        self.assertContainsMetadata(filename, Metadata())

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
        self.assertContainsMetadata(filename, metadata)

    def assertContainsMetadata(self, filename, expected):
        expectedLength = len(expected) + len(('bitrate', 'duration'))
        metadata = load(filename)
        assert_that(metadata.items(), has_items(*expected.items()),
                    'metadata items')
        assert_that(metadata, has_length(expectedLength), 'metadata count')
        assert_that(metadata.images, has_items(*expected.images),
                    'metadata images')


def load(filename):
    return tagger.load(filename)
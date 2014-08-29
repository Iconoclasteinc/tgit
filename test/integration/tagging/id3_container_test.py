# -*- coding: utf-8 -*-

import unittest
from hamcrest import assert_that, has_entry, has_items, has_key, has_length, contains, is_not, contains_inanyorder

from test.util import mp3_file as mp3

from tgit.metadata import Metadata, Image
import tgit.tagging.id3_container as container

BITRATE = mp3.Base.bitrate
DURATION = mp3.Base.duration


class ID3ContainerTest(unittest.TestCase):
    def setUp(self):
        self.mp3 = None

    def tearDown(self):
        self.mp3.delete()

    def makeMp3(self, **tags):
        if self.mp3:
            self.mp3.delete()

        self.mp3 = mp3.make(**tags)
        return self.mp3.filename

    def testReadsAlbumTitleFromTALBFrame(self):
        metadata = container.load(self.makeMp3(TALB='Album'))
        assert_that(metadata, has_entry('releaseName', 'Album'), 'metadata')

    def testJoinsAllTextsOfFrames(self):
        metadata = container.load(self.makeMp3(TALB=['Album', 'Titles']))
        assert_that(metadata, has_entry('releaseName', 'Album\x00Titles'), 'metadata')

    def testReadsLeadPerformerFromTPE1Frame(self):
        metadata = container.load(self.makeMp3(TPE1='Lead Artist'))
        assert_that(metadata, has_entry('leadPerformer', 'Lead Artist'), 'metadata')

    def testReadsGuestPerformersFromTMCLFrame(self):
        metadata = container.load(self.makeMp3(TMCL=[['Guitar', 'Guitarist'], ['Guitar', 'Bassist'],
                                                    ['Piano', 'Pianist']]))
        assert_that(metadata, has_entry('guestPerformers', contains_inanyorder(
            ('Guitar', 'Guitarist'),
            ('Guitar', 'Bassist'),
            ('Piano', 'Pianist'))), 'metadata')

    def testIgnoresTMCLEntriesWithBlankNames(self):
        metadata = container.load(self.makeMp3(TMCL=[['Guitar', 'Guitarist'], ['Piano', '']]))
        assert_that(metadata, has_entry('guestPerformers', contains(('Guitar', 'Guitarist'))), 'metadata')

    def testReadsLabelNameFromTOWNFrame(self):
        metadata = container.load(self.makeMp3(TOWN='Label Name'))
        assert_that(metadata, has_entry('labelName', 'Label Name'), 'metadata')

    def testReadsCatalogNumberFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_CATALOG_NUMBER='123 456-1'))
        assert_that(metadata, has_entry('catalogNumber', '123 456-1'), 'metadata')

    def testReadsUpcFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_UPC='1234567899999'))
        assert_that(metadata, has_entry('upc', '1234567899999'), 'metadata')

    def testReadsRecordingTimeFromTDRCFrame(self):
        metadata = container.load(self.makeMp3(TDRC='2012-07-15'))
        assert_that(metadata, has_entry('recordingTime', '2012-07-15'), 'metadata')

    def testReadsReleaseTimeFromTDRLFrame(self):
        metadata = container.load(self.makeMp3(TDRL='2013-11-15'))
        assert_that(metadata, has_entry('releaseTime', '2013-11-15'), 'metadata')

    def testReadsOriginalReleaseTimeFromTDORFrame(self):
        metadata = container.load(self.makeMp3(TDOR='1999-03-15'))
        assert_that(metadata, has_entry('originalReleaseTime', '1999-03-15'), 'metadata')

    def testReadsRecordingStudiosFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_RECORDING_STUDIOS='Studio Name'))
        assert_that(metadata, has_entry('recordingStudios', 'Studio Name'), 'metadata')

    def testReadsArtisticProducerFromTIPLFrame(self):
        metadata = container.load(self.makeMp3(TIPL=[['producer', 'Artistic Producer']]))
        assert_that(metadata, has_entry('producer', 'Artistic Producer'), 'metadata')

    def testTakesIntoAccountLastOfMultipleRoleDefinitions(self):
        metadata = container.load(self.makeMp3(TIPL=[['producer', 'first'], ['producer', 'last']]))
        assert_that(metadata, has_entry('producer', 'last'), 'metadata')

    def testIgnoresTPILEntriesWithBlankNames(self):
        metadata = container.load(self.makeMp3(TIPL=[['producer', '']]))
        assert_that(metadata, is_not(has_key('producer')), 'metadata')

    def testReadsMixingEngineerFromTIPLFrame(self):
        metadata = container.load(self.makeMp3(TIPL=[['mix', 'Mixing Engineer']]))
        assert_that(metadata, has_entry('mixer', 'Mixing Engineer'), 'metadata')

    def testReadsCommentsFromFrenchCOMMFrame(self):
        metadata = container.load(self.makeMp3(COMM=('Comments', 'fra')))
        assert_that(metadata, has_entry('comments', 'Comments'), 'metadata')

    def testReadsTrackTitleFromTIT2Frame(self):
        metadata = container.load(self.makeMp3(TIT2='Track Title'))
        assert_that(metadata, has_entry('trackTitle', 'Track Title'), 'metadata')

    def testReadsVersionInfoFromTPE4Frame(self):
        metadata = container.load(self.makeMp3(TPE4='Version Info'))
        assert_that(metadata, has_entry('versionInfo', 'Version Info'), 'metadata')

    def testReadsFeaturedGuestFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_FEATURED_GUEST='Featured Guest'))
        assert_that(metadata, has_entry('featuredGuest', 'Featured Guest'), 'metadata')

    def testReadsLyricistFromTEXTFrame(self):
        metadata = container.load(self.makeMp3(TEXT='Lyricist'))
        assert_that(metadata, has_entry('lyricist', 'Lyricist'), 'metadata')

    def testReadsComposerFromTCOMFrame(self):
        metadata = container.load(self.makeMp3(TCOM='Composer'))
        assert_that(metadata, has_entry('composer', 'Composer'), 'metadata')

    def testReadsPublisherFromTPUBFrame(self):
        metadata = container.load(self.makeMp3(TPUB='Publisher'))
        assert_that(metadata, has_entry('publisher', 'Publisher'), 'metadata')

    def testReadsIsrcFromTSRCFrame(self):
        metadata = container.load(self.makeMp3(TSRC='AABB12345678'))
        assert_that(metadata, has_entry('isrc', 'AABB12345678'), 'metadata')

    def testReadsTagsFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_TAGS='Tag1 Tag2 Tag3'))
        assert_that(metadata, has_entry('labels', 'Tag1 Tag2 Tag3'), 'metadata')

    def testReadsISNIFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_ISNI='00000123456789'))
        assert_that(metadata, has_entry('isni', '00000123456789'), 'metadata')

    def testReadsLyricsFromUSLTFrenchFrame(self):
        metadata = container.load(self.makeMp3(USLT=('Lyrics', 'fra')))
        assert_that(metadata, has_entry('lyrics', 'Lyrics'), 'metadata')

    def testReadsLanguageFromTLANFrame(self):
        metadata = container.load(self.makeMp3(TLAN='fra'))
        assert_that(metadata, has_entry('language', 'fra'), 'metadata')

    def testReadsPrimaryStyleFromTCONFrame(self):
        metadata = container.load(self.makeMp3(TCON='Jazz'))
        assert_that(metadata, has_entry('primaryStyle', 'Jazz'), 'metadata')

    def testReadsCompilationFlagFromNonStandardTCMPFlag(self):
        metadata = container.load(self.makeMp3(TCMP='0'))
        assert_that(metadata, has_entry('compilation', False), 'metadata')
        metadata = container.load(self.makeMp3(TCMP='1'))
        assert_that(metadata, has_entry('compilation', True), 'metadata')

    def testReadsBitrateFromAudioStreamInformation(self):
        metadata = container.load(self.makeMp3())
        assert_that(metadata, has_entry('bitrate', BITRATE), 'bitrate')

    def testReadsDurationFromAudioStreamInformation(self):
        metadata = container.load(self.makeMp3())
        assert_that(metadata, has_entry('duration', DURATION), 'duration')

    def testReadsCoverPicturesFromAPICFrames(self):
        metadata = container.load(self.makeMp3(
            APIC_FRONT=('image/jpeg', 'Front', 'front-cover.jpg'),
            APIC_BACK=('image/jpeg', 'Back', 'back-cover.jpg')))

        assert_that(metadata.images, contains_inanyorder(
            Image('image/jpeg', 'front-cover.jpg', type_=Image.FRONT_COVER, desc='Front'),
            Image('image/jpeg', 'back-cover.jpg', type_=Image.BACK_COVER, desc='Back'),
        ))

    def testReadsTaggerFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_TAGGER='TGiT v1.0'))
        assert_that(metadata, has_entry('tagger', 'TGiT v1.0'), 'metadata')

    def testReadsTaggingTimeFromCustomFrame(self):
        metadata = container.load(self.makeMp3(TXXX_TAGGING_TIME='2014-03-26 14:18:55 EDT-0400'))
        assert_that(metadata, has_entry('taggingTime', '2014-03-26 14:18:55 EDT-0400'), 'metadata')

    def testRoundTripsEmptyMetadataToFile(self):
        metadata = Metadata()
        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testRoundTripsMetadataToFile(self):
        metadata = Metadata()
        metadata.addImage('image/jpeg', 'salers.jpg', Image.FRONT_COVER)
        metadata['releaseName'] = u'Album'
        metadata['compilation'] = True
        metadata['leadPerformer'] = u'Lead Performer'
        metadata['isni'] = u'0000123456789'
        metadata['guestPerformers'] = [('Guitar', 'Guitarist'), ('Guitar', 'Bassist'), ('Piano', 'Pianist')]
        metadata['labelName'] = u'Label Name'
        metadata['catalogNumber'] = u'123 456-1'
        metadata['upc'] = u'987654321111'
        metadata['recordingTime'] = u'2012-07-01'
        metadata['releaseTime'] = u'2013-12-01'
        metadata['originalReleaseTime'] = u'1999-01-01'
        metadata['recordingStudios'] = u'Studio Name'
        metadata['producer'] = u'Artistic Producer'
        metadata['mixer'] = u'Mixing Engineer'
        metadata['contributors'] = [('recording', 'Recording Eng.'),
                                    ('mastering', 'Mastering Eng.'),
                                    ('recording', 'Assistant Recording Eng.')]
        metadata['comments'] = u'Comments'
        metadata['primaryStyle'] = u'Jazz'
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
        metadata['releaseName'] = u'Titre en Français'
        self.assertCanBeSavedAndReloadedWithSameState(metadata)

    def testRemovesFrameWhenTagNotInMetadata(self):
        filename = self.makeMp3(TALB='Album',
                                TMCL=[['Guitar', 'Guitarist']],
                                TIPL=[['mix', 'Mixing Engineer']],
                                USLT=('', 'fra'))

        container.save(filename, Metadata())
        self.assertContainsMetadata(filename, Metadata())

    def testCanSaveSeveralPicturesSharingTheSameDescription(self):
        filename = self.makeMp3()
        metadata = container.load(filename)
        metadata.addImage('image/jpeg', 'salers.jpg', desc='Front Cover')
        metadata.addImage('image/jpeg', 'ragber.jpg', desc='Front Cover')
        container.save(filename, metadata)

        assert_that(container.load(filename).images, contains_inanyorder(
            Image('image/jpeg', 'salers.jpg', type_=Image.OTHER, desc='Front Cover'),
            Image('image/jpeg', 'ragber.jpg', type_=Image.OTHER, desc='Front Cover (2)'),
        ))

    def testRemovesExistingAttachedPicturesOnSave(self):
        filename = self.makeMp3(APIC_FRONT=('image/jpeg', '', 'front-cover.jpg'))
        metadata = container.load(filename)
        metadata.removeImages()

        container.save(filename, metadata)
        assert_that(container.load(filename).images, has_length(0), 'removed images')

        metadata.addImage(mime='image/jpeg', data='salers.jpg', desc='Front')
        container.save(filename, metadata)

        assert_that(container.load(filename).images, has_length(1), 'updated images')

    def assertCanBeSavedAndReloadedWithSameState(self, metadata):
        filename = self.makeMp3()
        container.save(filename, metadata.copy())
        self.assertContainsMetadata(filename, metadata)

    def assertContainsMetadata(self, filename, expected):
        expectedLength = len(expected) + len(('bitrate', 'duration'))
        metadata = container.load(filename)
        assert_that(metadata.items(), has_items(*expected.items()), 'metadata items')
        assert_that(metadata, has_length(expectedLength), 'metadata count')
        assert_that(metadata.images, has_items(*expected.images), 'metadata images')
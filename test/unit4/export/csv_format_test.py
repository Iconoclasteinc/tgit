# -*- coding: utf-8 -*-

from StringIO import StringIO
import csv
import unittest

from hamcrest import assert_that, contains, has_item
from hamcrest.core.core.isequal import equal_to

from test.util4 import builders as build

from tgit4.export.csv_format import CsvFormat, toBoolean


class CsvFormatTest(unittest.TestCase):
    def setUp(self):
        self.encoding = 'utf-8'
        self.format = CsvFormat(self.encoding)
        self.out = StringIO()

    def encoded(self, text):
        return text.encode(self.encoding)

    def testIncludesHeaderRow(self):
        album = build.album()
        self.format.write(album, self.out)

        rows = readCsv(self.out)
        headers = rows.next()
        assert_that(headers, contains('Album Title',
                                      'Compilation',
                                      'Lead Performer',
                                      'Lead Performer ISNI',
                                      'Guest Performers',
                                      'Label Name',
                                      'Catalog Number',
                                      'UPC/EAN',
                                      'Comments',
                                      'Release Date',
                                      'Recording Date',
                                      'Recording Studios',
                                      'Producer',
                                      'Mixer',
                                      'Primary Style',
                                      'Track Title',
                                      'Version Information',
                                      'Featured Guest',
                                      'Lyrics',
                                      'Language',
                                      'Publisher',
                                      'Lyricist',
                                      'Composer',
                                      'ISRC',
                                      'Tags'), 'header')

    def testWritesTrackMetadataInColumns(self):
        album = build.album(
            releaseName='Release Name',
            isni='0000123456789',
            guestPerformers=[('Instrument1', 'Performer1'), ('Instrument2', 'Performer2')],
            labelName='Label Name',
            catalogNumber='Catalog Number',
            upc='Barcode',
            comments='Comments\n...\n...',
            releaseTime='2014',
            recordingTime='2013',
            recordingStudios='Studios',
            producer='Artistic Producer',
            mixer='Mixing Engineer',
            primaryStyle='Genre',
            tracks=[build.track(
                trackTitle='Track Title',
                leadPerformer='Lead Performer',
                versionInfo='Version Info',
                featuredGuest='Featuring',
                lyrics='Lyrics\n...\...\n...',
                language='eng',
                publisher='Publisher',
                lyricist='Lyricist',
                composer='Composer',
                isrc='ISRC',
                labels='Tag1 Tag2 Tag3')])

        self.format.write(album, self.out)

        rows = readCsv(self.out)
        _ = rows.next()
        data = rows.next()
        assert_that(data, contains('Release Name',
                                  'False',
                                  'Lead Performer',
                                  '0000123456789',
                                  'Instrument1: Performer1; Instrument2: Performer2',
                                  'Label Name',
                                  'Catalog Number',
                                  'Barcode',
                                  'Comments\r...\r...',
                                  '2014',
                                  '2013',
                                  'Studios',
                                  'Artistic Producer',
                                  'Mixing Engineer',
                                  'Genre',
                                  'Track Title',
                                  'Version Info',
                                  'Featuring',
                                  'Lyrics\r...\...\r...',
                                  'eng',
                                  'Publisher',
                                  'Lyricist',
                                  'Composer',
                                  'ISRC',
                                  'Tag1 Tag2 Tag3'), 'row')

    def testConvertsBooleansToText(self):
        assert_that(toBoolean(None), equal_to('False'), 'boolean(None)')
        assert_that(toBoolean(False), equal_to('False'), 'boolean(False)')
        assert_that(toBoolean(True), equal_to('True'), 'boolean(True)')

    def testWritesOneRecordPerTrackInAlbum(self):
        album = build.album(tracks=[build.track(trackTitle='Song 1'),
                                    build.track(trackTitle='Song 2'),
                                    build.track(trackTitle='Song 3')])

        self.format.write(album, self.out)

        rows = readCsv(self.out)
        _ = rows.next()
        assert_that(rows.next(), has_item('Song 1'), 'first row')
        assert_that(rows.next(), has_item('Song 2'), 'second row')
        assert_that(rows.next(), has_item('Song 3'), 'third row')

    def testMakeLineBreaksExcelFriendlyByConvertingLineFeedsToCarriageReturns(self):
        album = build.album(comments='Comments\nspanning\nseveral lines', tracks=[build.track()])

        self.format.write(album, self.out)

        csv = readCsv(self.out)
        _ = csv.next()
        assert_that(csv.next(), has_item('Comments\rspanning\rseveral lines'),
                    'row with line feeds')

    def testEncodesNonAsciiRecordContents(self):
        album = build.album(comments=u'en français dans le texte', tracks=[build.track()])
        self.format.write(album, self.out)

        csv = readCsv(self.out)
        _ = csv.next()
        assert_that(csv.next(), has_item(self.encoded(u'en français dans le texte')))


def readCsv(out):
    out.seek(0)
    return csv.reader(out)
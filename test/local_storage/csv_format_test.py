# -*- coding: utf-8 -*-

from io import StringIO
import csv
import unittest

from hamcrest import assert_that, contains, has_item
from hamcrest.core.core.isequal import equal_to

from test.util import builders as build
from tgit.local_storage.csv_format import CsvFormat, toBoolean


class CsvFormatTest(unittest.TestCase):
    def setUp(self):
        self.format = CsvFormat()
        self.out = StringIO()

    def testIncludesHeaderRow(self):
        album = build.album()
        self.format.write(album, self.out)

        rows = readCsv(self.out)
        headers = next(rows)
        assert_that(headers, contains('Release Name',
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
                                      'Track Number',
                                      'Total Tracks',
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
            release_name='Release Name',
            lead_performer='Lead Performer',
            isni='0000123456789',
            guest_performers=[('Instrument1', 'Performer1'), ('Instrument2', 'Performer2')],
            label_name='Label Name',
            catalog_number='Catalog Number',
            upc='Barcode',
            comments='Comments\n...\n...',
            release_time='2014',
            recording_time='2013',
            recording_studios='Studios',
            producer='Artistic Producer',
            mixer='Mixing Engineer',
            primary_style='Genre')

        track = build.track(
            track_title='Track Title',
            versionInfo='Version Info',
            featuredGuest='Featuring',
            lyrics='Lyrics\n...\...\n...',
            language='eng',
            publisher='Publisher',
            lyricist='Lyricist',
            composer='Composer',
            isrc='ISRC',
            labels='Tag1 Tag2 Tag3')

        album.addTrack(track)
        track.track_number = 3
        track.total_tracks = 9

        self.format.write(album, self.out)

        rows = readCsv(self.out)
        _ = next(rows)
        data = next(rows)
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
                                   '3',
                                   '9',
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
        album = build.album(tracks=[build.track(track_title='Song 1'),
                                    build.track(track_title='Song 2'),
                                    build.track(track_title='Song 3')])

        self.format.write(album, self.out)

        rows = readCsv(self.out)
        _ = next(rows)
        assert_that(next(rows), has_item('Song 1'), 'first row')
        assert_that(next(rows), has_item('Song 2'), 'second row')
        assert_that(next(rows), has_item('Song 3'), 'third row')

    def testMakeLineBreaksExcelFriendlyByConvertingLineFeedsToCarriageReturns(self):
        album = build.album(comments='Comments\nspanning\nseveral lines', tracks=[build.track()])

        self.format.write(album, self.out)

        csv = readCsv(self.out)
        _ = next(csv)
        assert_that(next(csv), has_item('Comments\rspanning\rseveral lines'), 'row with line feeds')


def readCsv(out):
    out.seek(0)
    return csv.reader(out)

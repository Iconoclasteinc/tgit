# -*- coding: utf-8 -*-

import csv
from StringIO import StringIO
import unittest
from hamcrest import assert_that, contains, has_item
from hamcrest.core.core.isequal import equal_to

from test.util import builders as build

from tgit.csv.csv_format import CsvFormat, toBoolean


class CsvFormatTest(unittest.TestCase):
    def setUp(self):
        self.encoding = 'utf-8'
        self.format = CsvFormat(self.encoding)
        self.out = StringIO()

    def encoded(self, text):
        return text.encode(self.encoding)

    def testIncludesEncodedHeaderRow(self):
        album = build.album()
        self.format.write(album, self.out)

        rows = readCsv(self.out)
        headers = rows.next()
        assert_that(headers, contains("Titre de l'album",
                                      'Compilation',
                                      "Nom de l'artiste principal",
                                      "Musiciens de l'album",
                                      'Nom de la maison de disques',
                                      self.encoded(u'Numéro de catalogue'),
                                      'UPC/EAN',
                                      'Commentaires',
                                      self.encoded(u"Date de mise en marché de l'album"),
                                      "Date de l'enregistrement",
                                      "Studios d'enregistrement",
                                      self.encoded(u'Réalisateur'),
                                      'Mixeur',
                                      "Genre de l'album",
                                      'Titre de la piste',
                                      'Infos sur la version',
                                      self.encoded(u'Invité spécial'),
                                      'Paroles',
                                      'Langue des paroles',
                                      'Éditeur',
                                      'Auteur',
                                      'Compositeur',
                                      'ISRC',
                                      'Tags'), 'header')

    def testWritesTrackMetadataInColumns(self):
        album = build.album(
            releaseName='Release Name',
            leadPerformer='Lead Performer',
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
                versionInfo='Version Info',
                featuredGuest='Featuring',
                lyrics='Lyrics\n...\...\n...',
                language='eng',
                publisher='Publisher',
                lyricist='Lyricist',
                composer='Composer',
                isrc='ISRC',
                tags='Tag1 Tag2 Tag3')])

        self.format.write(album, self.out)

        rows = readCsv(self.out)
        _ = rows.next()
        data = rows.next()
        assert_that(data, contains('Release Name',
                                  'False',
                                  'Lead Performer',
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

# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
from hamcrest import assert_that, equal_to, is_, contains, has_properties
from test.util import builders as build, resources, doubles

from tgit import album_director as director
from tgit.album_director import Snapshot
from tgit.metadata import Image
from tgit.util import fs


class FakeExportFormat(object):
    def write(self, album, out):
        for track in album.tracks:
            out.write(track.trackTitle)
            out.write('\n')


class AlbumDirectorTest(unittest.TestCase):
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempDir)

    def testUpdatesTrackMetadataWithNewState(self):
        changes = Snapshot()
        changes.trackTitle = 'Title'
        changes.leadPerformer = 'Artist'
        changes.versionInfo = 'Version'
        changes.featuredGuest = 'Featuring'
        changes.lyricist = 'Lyricist'
        changes.composer = 'Composer'
        changes.publisher = 'Publisher'
        changes.isrc = 'ZZZ123456789'
        changes.tags = 'Tags'
        changes.lyrics = 'Lyrics\nLyrics\n...'
        changes.language = 'und'

        track = build.track()
        director.updateTrack(track, changes)

        assert_that(track.trackTitle, equal_to('Title'), 'track title')
        assert_that(track.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(track.versionInfo, equal_to('Version'), 'version info')
        assert_that(track.featuredGuest, equal_to('Featuring'), 'featured guest')
        assert_that(track.lyricist, equal_to('Lyricist'), 'lyricist')
        assert_that(track.composer, equal_to('Composer'), 'composer')
        assert_that(track.publisher, equal_to('Publisher'), 'publisher')
        assert_that(track.isrc, equal_to('ZZZ123456789'), 'isrc')
        assert_that(track.tags, equal_to('Tags'), 'tags')
        assert_that(track.lyrics, equal_to('Lyrics\nLyrics\n...'), 'lyrics')
        assert_that(track.language, equal_to('und'), 'language')

    def testUpdatesAlbumMetadataWithNewState(self):
        changes = Snapshot()
        changes.releaseName = 'Title'
        changes.compilation = True
        changes.leadPerformer = 'Artist'
        changes.guestPerformers = [('Guitar', 'Guitarist')]
        changes.labelName = 'Label'
        changes.catalogNumber = 'XXX123456789'
        changes.upc = '123456789999'
        changes.comments = 'Comments\n...'
        changes.releaseTime = '2009-01-01'
        changes.recordingTime = '2008-09-15'
        changes.recordingStudios = 'Studios'
        changes.producer = 'Producer'
        changes.mixer = 'Engineer'
        changes.primaryStyle = 'Style'

        album = build.album()
        director.updateAlbum(album, changes)

        assert_that(album.releaseName, equal_to('Title'), 'release name')
        assert_that(album.compilation, is_(True), 'compilation')
        assert_that(album.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(album.guestPerformers, equal_to([('Guitar', 'Guitarist')]), 'guest performers')
        assert_that(album.labelName, equal_to('Label'), 'label name')
        assert_that(album.catalogNumber, equal_to('XXX123456789'), 'catalog number')
        assert_that(album.upc, equal_to('123456789999'), 'upc')
        assert_that(album.comments, equal_to('Comments\n...'), 'comments')
        assert_that(album.releaseTime, equal_to('2009-01-01'), 'release time')
        assert_that(album.recordingTime, equal_to('2008-09-15'), 'recording time')
        assert_that(album.recordingStudios, equal_to('Studios'), 'recording studios')
        assert_that(album.producer, equal_to('Producer'), 'producer')
        assert_that(album.mixer, equal_to('Engineer'), 'mixer')
        assert_that(album.primaryStyle, equal_to('Style'), 'primary style')

    def testClearsAlbumImages(self):
        album = build.album(images=[build.image('image/jpeg', 'image data')])
        director.removeAlbumCover(album)
        assert_that(album.images, equal_to([]), 'images')

    def testLoadsAndChangesAlbumMainCover(self):
        album = build.album()
        album.addFrontCover(mime='image/gif', data='old cover')

        coverFile = resources.path('front-cover.jpg')
        director.changeAlbumCover(album, coverFile)

        assert_that(album.images, contains(has_properties(mime='image/jpeg',
                                                          data=fs.readContent(coverFile),
                                                          type=Image.FRONT_COVER,
                                                          desc='Front Cover')), 'images')

    def testMovesTrackInAlbum(self):
        setFireToTheRain = build.track(trackTitle='Set Fire to the Rain')
        rollingInTheDeep = build.track(trackTitle='Rolling in the Deep')
        twentyOne = build.album(tracks=[setFireToTheRain, rollingInTheDeep])

        director.moveTrack(twentyOne, rollingInTheDeep, 0)
        assert_that(twentyOne.tracks, contains(rollingInTheDeep, setFireToTheRain), 'reordered tracks')

    def testSavesAllTracksInAlbum(self):
        setFireToTheRain = build.track(trackTitle='Set Fire to the Rain')
        rollingInTheDeep = build.track(trackTitle='Rolling in the Deep')
        twentyOne = build.album(tracks=[setFireToTheRain, rollingInTheDeep])

        catalog = doubles.trackLibrary()
        director.recordAlbum(catalog, twentyOne)

        catalog.assertContains(setFireToTheRain, rollingInTheDeep)

    def testFormatsAlbumAndWritesToDestinationFile(self):
        setFireToTheRain = build.track(trackTitle='Set Fire to the Rain')
        rollingInTheDeep = build.track(trackTitle='Rolling in the Deep')
        twentyOne = build.album(tracks=[setFireToTheRain, rollingInTheDeep])

        destinationFile = os.path.join(self.tempDir, 'twentyOne.csv')

        exportAs = FakeExportFormat()
        director.exportAlbum(exportAs, twentyOne, destinationFile)

        assert_that(fs.readContent(destinationFile), equal_to('Set Fire to the Rain\nRolling in the Deep\n'))
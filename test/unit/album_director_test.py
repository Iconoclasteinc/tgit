# -*- coding: utf-8 -*-

from tgit.util import sip_api

sip_api.use_v2()

from datetime import datetime
import os
import shutil
import unittest
from dateutil import tz
from hamcrest import assert_that, equal_to, is_, contains, has_properties, has_entries, contains_inanyorder, none
from test.util import builders as build, resources, doubles, mp3_file

from tgit import album_director as director, __version__
from tgit.album_director import sanitize
from tgit.metadata import Image
from tgit.tagging import id3_container
from tgit.tagging.id3_container import ID3Container
from tgit.util import fs


class AlbumDirectorTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = resources.makeTempDir()
        self.library = doubles.recordingLibrary()
        self.nameRegistry = doubles.nameRegistry()

    def tearDown(self):
        self.library.delete()
        shutil.rmtree(self.tempdir)

    def testUpdatesTrackMetadata(self):
        track = build.track()
        director.updateTrack(track,
                             trackTitle='Title', leadPerformer='Artist', versionInfo='Version',
                             featuredGuest='Featuring', lyricist='Lyricist', composer='Composer',
                             publisher='Publisher', isrc='ZZZ123456789', labels='Tags', lyrics='Lyrics\nLyrics\n...',
                             language='und')

        assert_that(track.trackTitle, equal_to('Title'), 'track title')
        assert_that(track.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(track.versionInfo, equal_to('Version'), 'version info')
        assert_that(track.featuredGuest, equal_to('Featuring'), 'featured guest')
        assert_that(track.lyricist, equal_to('Lyricist'), 'lyricist')
        assert_that(track.composer, equal_to('Composer'), 'composer')
        assert_that(track.publisher, equal_to('Publisher'), 'publisher')
        assert_that(track.isrc, equal_to('ZZZ123456789'), 'isrc')
        assert_that(track.labels, equal_to('Tags'), 'tags')
        assert_that(track.lyrics, equal_to('Lyrics\nLyrics\n...'), 'lyrics')
        assert_that(track.language, equal_to('und'), 'language')

    def testUpdatesAlbumMetadata(self):
        album = build.album()
        director.updateAlbum(album,
                             releaseName='Title', compilation=True, leadPerformer='Artist', isni='0000123456789',
                             guestPerformers=[('Guitar', 'Guitarist')], labelName='Label',
                             catalogNumber='XXX123456789', upc='123456789999', comments='Comments\n...',
                             releaseTime='2009-01-01', recordingTime='2008-09-15', recordingStudios='Studios',
                             producer='Producer', mixer='Engineer', primaryStyle='Style')

        assert_that(album.releaseName, equal_to('Title'), 'release name')
        assert_that(album.compilation, is_(True), 'compilation')
        assert_that(album.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(album.isni, equal_to('0000123456789'), 'isni')
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

    def testUpdatesTracksLeadPerformerWhenAlbumIsNotACompilation(self):
        album = build.album(tracks=[build.track(), build.track(), build.track()])
        director.updateAlbum(album, compilation=False, leadPerformer='Album Artist')

        for track in album.tracks:
            assert_that(track.leadPerformer, equal_to('Album Artist'), 'track artist')

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

    # todo remove duplication with doubles.recordingLibrary()
    # will need to standardize behavior of images
    def testTagsCopyOfOriginalRecordingWithCompleteMetadata(self):
        original = mp3_file.make(to=self.tempdir)
        track = build.track(filename=original.filename,
                            trackTitle='Track Title',
                            album=build.album(releaseName='Album Title',
                                              leadPerformer='Album Artist',
                                              images=[build.image(mime='image/jpeg', data='<image data>')]))
        now = datetime(2014, 03, 23, 16, 44, 33, tzinfo=tz.tzutc())

        tagged = os.path.join(self.tempdir, 'tagged.mp3')
        director.recordTrack(ID3Container(), tagged, track, now)

        metadata = id3_container.load(tagged)
        assert_that(metadata, has_entries(tagger='TGiT v' + __version__,
                                          taggingTime='2014-03-23 16:44:33 +0000',
                                          releaseName='Album Title',
                                          leadPerformer='Album Artist'), 'metadata tags')
        assert_that(metadata.images, contains(Image(mime='image/jpeg', data='<image data>')), 'attached pictures')

    def testGracefullyHandlesWhenTaggingOriginalRecording(self):
        original = mp3_file.make(to=self.tempdir)
        track = build.track(filename=original.filename)
        album = build.album(tracks=[track])

        director.recordTrack(ID3Container(), original.filename, track, datetime.now())

    def testFormatsAlbumAndWritesToDestinationFile(self):
        album = build.album(tracks=[
            build.track(trackTitle='Set Fire to the Rain'),
            build.track(trackTitle='Rolling in the Deep'),
            build.track(trackTitle='Someone Like You')])

        destinationFile = os.path.join(self.tempdir, 'twentyOne.csv')

        exportAs = doubles.exportFormat()
        director.exportAlbum(exportAs, album, destinationFile)

        assert_that(fs.readContent(destinationFile), equal_to('Set Fire to the Rain\n'
                                                              'Rolling in the Deep\n'
                                                              'Someone Like You\n'))

    def testAddsSelectedTracksToAlbumInSelectionOrder(self):
        self.library.create(trackTitle='Rolling in the Deep')
        self.library.create(trackTitle='Set Fire to the Rain')
        self.library.create(trackTitle='Someone Like You')

        album = build.album()
        director.addTracksToAlbum(ID3Container(), album, self.library.recordings)
        assert_that(album.tracks, contains(
            has_properties(trackTitle='Rolling in the Deep'),
            has_properties(trackTitle='Set Fire to the Rain'),
            has_properties(trackTitle='Someone Like You')))

    def testAddsAllTracksInSelectedFolder(self):
        self.library.create(trackTitle='Rolling in the Deep')
        self.library.create(trackTitle='Set Fire to the Rain')
        self.library.create(trackTitle='Someone Like You')

        album = build.album()

        director.addTracksToAlbum(ID3Container(), album, (self.library.root, ))
        assert_that(album.tracks, contains_inanyorder(
            has_properties(trackTitle='Rolling in the Deep'),
            has_properties(trackTitle='Set Fire to the Rain'),
            has_properties(trackTitle='Someone Like You')))

    def testReplacesInvalidCharactersForFileNamesWithUnderscores(self):
        assert_that(sanitize(u'1/2<3>4:5"6/7\\8?9*10|'), equal_to('1_2_3_4_5_6_7_8_9_10_'), 'sanitized name')

    def testStripsLeadingAndTrailingWhitespaceFromFileNames(self):
        assert_that(sanitize(u'  filename   '), equal_to('filename'), 'sanitized name')

    def testTagsFileToSameDirectoryUnderArtistAndTitleName(self):
        track = build.track(filename='track.mp3', leadPerformer='artist', trackTitle='title')
        album = build.album(tracks=[build.track(), build.track(), track])

        assert_that(director.taggedName(track), equal_to('artist - 03 - title.mp3'), 'name of tagged file')

    def testUpdatesIsniMetadataToFirstIsniFoundInRegistry(self):
        self.nameRegistry.registry.append(('0000123456789', 'Clerc', 'Julien'))

        album = build.album(leadPerformer='Julien Clerc')
        director.lookupISNI(self.nameRegistry, album)
        assert_that(album.isni, equal_to('0000123456789'), 'isni')

    def testUpdatesIsniMetadataToNoneWhenIsniIsNotFoundInRegistry(self):
        album = build.album(leadPerformer='Julien Clerc', isni='0000123456789')
        director.lookupISNI(self.nameRegistry, album)
        assert_that(album.isni, none(), 'isni')

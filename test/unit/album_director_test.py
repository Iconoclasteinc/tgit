# -*- coding: utf-8 -*-
from datetime import datetime
import os
import shutil
import unittest

from dateutil import tz

from hamcrest import assert_that, equal_to, is_, contains, has_properties, has_entries, contains_inanyorder, none, \
    has_item, empty
import pytest

from test.util import builders as build, resources, doubles, mp3_file
import tgit
from tgit import album_director as director, tagging
from tgit.metadata import Image
from tgit.util import fs


now = datetime(2014, 3, 23, 16, 44, 33, tzinfo=tz.tzutc())

@pytest.fixture
def recordings(request, tmpdir):
    library = doubles.recording_library(tmpdir.strpath)
    request.addfinalizer(library.delete)
    return library


@pytest.yield_fixture
def mp3(tmpdir):
    def maker(**tags):
        return mp3_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    shutil.rmtree(tmpdir.strpath)


def test_adds_selected_tracks_to_album_in_selection_order(recordings):
    recordings.add_mp3(trackTitle='Rolling in the Deep')
    recordings.add_mp3(trackTitle='Set Fire to the Rain')
    recordings.add_mp3(trackTitle='Someone Like You')

    album = build.album()
    director.add_tracks_to_album(album, [recording.filename for recording in recordings.entries])

    assert_that(album.tracks, contains(
        has_properties(trackTitle='Rolling in the Deep'),
        has_properties(trackTitle='Set Fire to the Rain'),
        has_properties(trackTitle='Someone Like You')))


def test_finds_and_adds_to_album_all_supported_audio_files_in_selected_folder(recordings):
    recordings.add_mp3(trackTitle='Rolling in the Deep')
    recordings.add_mp3(trackTitle='Set Fire to the Rain')
    recordings.add_flac(lead_performer='Adele')

    album = build.album()
    director.add_tracks_to_album(album, (recordings.root,))

    assert_that(album.tracks, contains_inanyorder(
        has_properties(trackTitle='Rolling in the Deep'),
        has_properties(trackTitle='Set Fire to the Rain'),
        has_properties(leadPerformer='Adele')))


def test_tags_copy_of_original_recording_with_complete_metadata(mp3):
    album = build.album(releaseName='Album Title',
                        leadPerformer='Album Artist',
                        images=[build.image(mime='image/jpeg', data=b'<image data>')])
    track = build.track(filename=mp3(),
                        trackTitle='Track Title',
                        album=album)

    destination_file = os.path.join(os.path.dirname(track.filename), 'tagged.mp3')
    director.record_track(destination_file, track, now)

    metadata = tagging.load_metadata(destination_file)
    assert_that(metadata, has_entries(releaseName='Album Title', leadPerformer='Album Artist'), 'metadata tags')
    assert_that(metadata.images, contains(Image(mime='image/jpeg', data=b'<image data>')), 'attached pictures')


def test_adds_version_information_to_tags(mp3):
    track = build.track(filename=mp3(), album=build.album())

    tagged_file = mp3()
    director.record_track(tagged_file, track, now)

    metadata = tagging.load_metadata(tagged_file)
    assert_that(metadata, has_entries(tagger='TGiT v' + tgit.__version__, taggingTime='2014-03-23 16:44:33 +0000'))


def test_gracefully_handles_when_tagging_original_recording(mp3):
    original_file = mp3()
    track = build.track(filename=original_file, album=build.album())

    director.record_track(original_file, track, datetime.now())


class AlbumDirectorTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = resources.makeTempDir()
        self.library = doubles.recording_library(self.tempdir)

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
                                                          data=fs.binary_content_of(coverFile),
                                                          type=Image.FRONT_COVER,
                                                          desc='Front Cover')), 'images')

    def testMovesTrackInAlbum(self):
        setFireToTheRain = build.track(trackTitle='Set Fire to the Rain')
        rollingInTheDeep = build.track(trackTitle='Rolling in the Deep')
        twentyOne = build.album(tracks=[setFireToTheRain, rollingInTheDeep])

        director.moveTrack(twentyOne, rollingInTheDeep, 0)
        assert_that(twentyOne.tracks, contains(rollingInTheDeep, setFireToTheRain), 'reordered tracks')

    def test_encodes_exported_file_in_specified_charset(self):
        album = build.album(tracks=[build.track(trackTitle="Les Comédiens")])
        destination_file = os.path.join(self.tempdir, 'french.csv')

        director.export_album(doubles.export_format(), album, destination_file, 'windows-1252')

        def text_content_of(file):
            return open(file, 'r', encoding='windows-1252').read()

        assert_that(text_content_of(destination_file), equal_to('Les Comédiens\n'))

    def testReplacesInvalidCharactersForFileNamesWithUnderscores(self):
        assert_that(director.sanitize('1/2<3>4:5"6/7\\8?9*10|'), equal_to('1_2_3_4_5_6_7_8_9_10_'), 'sanitized name')

    def testStripsLeadingAndTrailingWhitespaceFromFileNames(self):
        assert_that(director.sanitize('  filename   '), equal_to('filename'), 'sanitized name')

    def testTagsFileToSameDirectoryUnderArtistAndTitleName(self):
        track = build.track(filename='track.mp3', leadPerformer='artist', trackTitle='title')
        album = build.album(tracks=[build.track(), build.track(), track])

        assert_that(director.taggedName(track), equal_to('artist - 03 - title.mp3'), 'name of tagged file')

    def testReturnsListOfIdentitiesWhenISNIFoundInRegistry(self):
        class NameRegistry:
            def search_by_keywords(self, *keywords):
                if keywords[0] == 'Maloy' and keywords[1] == 'Rebecca' and keywords[2] == 'Ann':
                    return '1', [('0000000115677274', 'Rebecca Ann Maloy')]
                return '0', []

        _, identities = director.lookupISNI(NameRegistry(), 'Rebecca Ann Maloy')
        assert_that(identities, has_item(('0000000115677274', 'Rebecca Ann Maloy')), 'isni')

    def testReturnsEmptyListWhenISNIIsNotFoundInRegistry(self):
        class NameRegistry:
            def search_by_keywords(self, *keywords):
                return '0', []

        _, identities = director.lookupISNI(NameRegistry(), 'Rebecca Ann Maloy')
        assert_that(identities, empty(), 'isni')

    def testUpdatesISNIFromSelectedIdentity(self):
        identity = '0000000115677274', ('_', '_', '_')
        album = build.album(compilation=False)

        director.selectISNI(identity, album)
        assert_that(album.isni, equal_to(identity[0]), 'isni')

    def testUpdatesLeadPerformerFromSelectedIdentity(self):
        name = 'Paul McCartney'
        identity = '_', (name, '_', '_')
        track = build.track(leadPerformer='artist')
        album = build.album(tracks=[track], compilation=False)

        director.selectISNI(identity, album)
        assert_that(album.leadPerformer, equal_to(name), 'lead performer')
        assert_that(track.leadPerformer, equal_to(name), 'lead performer')

    def testClearsLeadPerformerISNIFromAlbum(self):
        album = build.album(isni='0000123456789')
        director.clearISNI(album)
        assert_that(album.isni, none(), 'isni')

    def testAssignsISNIToLeadPerformerUsingTheAlbumTitle(self):
        class NameRegistry:
            def assign(self, forename, surname, *titleOfWorks):
                if forename == 'Paul' and surname == 'McCartney' and titleOfWorks[0] == 'Memory Almost Full':
                    return '0000123456789'
                return None

        album = build.album(leadPerformer='Paul McCartney', releaseName='Memory Almost Full')
        assert_that(director.assignISNI(NameRegistry(), album), equal_to('0000123456789'), 'isni assigned')

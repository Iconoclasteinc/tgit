# -*- coding: utf-8 -*-
from datetime import datetime
import os
import shutil
import unittest

from dateutil import tz

from hamcrest import assert_that, equal_to, is_, contains, has_properties, has_entries, contains_inanyorder, none, \
    has_item, empty, has_property, contains_string
import pytest

from test.util import builders as build, resources, doubles, mp3_file
import tgit
from tgit import album_director as director, tagging
from tgit.album import Album
from tgit.album_portfolio import AlbumPortfolio
from tgit.metadata import Image
from tgit.ui.new_album_screen import AlbumCreationProperties
from tgit.util import fs

NOW = datetime(2014, 3, 23, 16, 44, 33, tzinfo=tz.tzutc())


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


def test_adds_new_album_to_porfolio(tmpdir):
    album_destination = tmpdir.strpath
    portfolio = AlbumPortfolio()
    director.create_album_into(portfolio)(
        AlbumCreationProperties(type_=Album.Type.MP3, album_name="album", album_location=album_destination))
    assert_that(portfolio, not empty())


def test_saves_new_album_to_disk(tmpdir):
    destination = tmpdir.strpath
    portfolio = AlbumPortfolio()
    creation_properties = AlbumCreationProperties(type_=Album.Type.FLAC, album_name="album", album_location=destination)
    director.create_album_into(portfolio)(creation_properties)

    def read_lines(file):
        content = open(file, "r").read()
        return content.split("\n")

    assert_that(read_lines(creation_properties.album_full_path), has_item(contains_string("type: flac")))


def test_saves_album_metadata_to_disk(tmpdir):
    destination = tmpdir.join("album.tgit").strpath
    album = build.album(release_name="Title", compilation=True, lead_performer="Artist", isni="0000123456789",
                        guestPerformers=[("Guitar", "Guitarist"), ("Piano", "Pianist")], label_name="Label",
                        catalogNumber="XXX123456789", upc="123456789999", comments="Comments\n...",
                        releaseTime="2009-01-01", recording_time="2008-09-15", recordingStudios="Studios",
                        producer="Producer", mixer="Engineer", primary_style="Style",
                        images=[build.image("image/jpeg", fs.binary_content_of(resources.path("front-cover.jpg")),
                                            Image.FRONT_COVER, "Front Cover")])
    album.destination = destination

    director.export_as_yaml(album)

    def read_lines(file):
        content = open(file, "r").read()
        return content.split("\n")

    lines = read_lines(destination)
    assert_that(lines, has_item(contains_string("release_name: Title")), "release name")
    assert_that(lines, has_item(contains_string("compilation: true")), "compilation")
    assert_that(lines, has_item(contains_string("lead_performer: Artist")), "lead performer")
    assert_that(lines, has_item(contains_string("isni: 0000123456789")), "isni")
    assert_that(lines, has_item(contains_string("label_name: Label")), "label name")
    assert_that(lines, has_item(contains_string("upc: '123456789999'")), "upc")
    assert_that(lines, has_item(contains_string("comments: 'Comments")), "comments")
    assert_that(lines, has_item(contains_string(" ...'")), "comments")
    assert_that(lines, has_item(contains_string("releaseTime: '2009-01-01'")), "release time")
    assert_that(lines, has_item(contains_string("recording_time: '2008-09-15'")), "recording time")
    assert_that(lines, has_item(contains_string("recordingStudios: Studios")), "recording studios")
    assert_that(lines, has_item(contains_string("producer: Producer")), "producer")
    assert_that(lines, has_item(contains_string("mixer: Engineer")), "mixer")
    assert_that(lines, has_item(contains_string("primary_style: Style")), "primary style")
    assert_that(lines, has_item(contains_string("guestPerformers:")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Guitar")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Guitarist")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Piano")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Pianist")), "guest performers")
    assert_that(lines, has_item(contains_string("images:")), "images")
    assert_that(lines, has_item(contains_string("  data: !!binary |")), "images")
    assert_that(lines, has_item(
        contains_string("    /9j/4AAQSkZJRgABAQEASABIAAD/4gxYSUNDX1BST0ZJTEUAAQEAAAxITGlubwIQAABtbnRyUkdC")), "images")
    assert_that(lines, has_item(contains_string("  desc: Front Cover")), "images")
    assert_that(lines, has_item(contains_string("  mime: image/jpeg")), "images")
    assert_that(lines, has_item(contains_string("  type: 1")), "images")


def test_load_album_from_project_file():
    portfolio = AlbumPortfolio()
    director.load_album_into(portfolio)(destination=resources.path("album_mp3.tgit"))
    album = portfolio[0]

    assert_that(album.type, equal_to("mp3"), "Type")
    assert_that(album.release_name, equal_to("Title"), "release name")
    assert_that(album.compilation, is_(True), "compilation")
    assert_that(album.lead_performer, equal_to("Artist"), "lead performer")
    assert_that(album.isni, equal_to("0000123456789"), "isni")
    assert_that(album.guestPerformers, equal_to([("Guitar", "Guitarist"), ("Piano", "Pianist")]), "guest performers")
    assert_that(album.label_name, equal_to("Label"), "label name")
    assert_that(album.catalogNumber, equal_to("XXX123456789"), "catalog number")
    assert_that(album.upc, equal_to("123456789999"), "upc")
    assert_that(album.comments, equal_to("Comments\n..."), "comments")
    assert_that(album.releaseTime, equal_to("2009-01-01"), "release time")
    assert_that(album.recording_time, equal_to("2008-09-15"), "recording time")
    assert_that(album.recordingStudios, equal_to("Studios"), "recording studios")
    assert_that(album.producer, equal_to("Producer"), "producer")
    assert_that(album.mixer, equal_to("Engineer"), "mixer")
    assert_that(album.primary_style, equal_to("Style"), "primary style")
    assert_that(album.images, contains(
        Image("image/jpeg", fs.binary_content_of(resources.path("front-cover.jpg")), Image.FRONT_COVER, "Front Cover")),
                "attached pictures")


def test_removes_album_from_portfolio():
    portfolio = AlbumPortfolio()
    album = build.album()
    portfolio.add_album(album)
    director.remove_album_from(portfolio)(album)
    assert_that(portfolio, empty())


def test_adds_selected_tracks_to_album_in_selection_order(recordings):
    recordings.add_mp3(track_title='Rolling in the Deep')
    recordings.add_mp3(track_title='Set Fire to the Rain')
    recordings.add_mp3(track_title='Someone Like You')

    album = build.album()
    director.add_tracks_to(album)([recording.filename for recording in recordings.entries])

    assert_that(album.tracks, contains(
        has_properties(track_title='Rolling in the Deep'),
        has_properties(track_title='Set Fire to the Rain'),
        has_properties(track_title='Someone Like You')))


def test_imports_album_from_track(recordings, tmpdir):
    track_location = recordings.add_mp3(track_title="Smash Smash",
                                        release_name="Honeycomb", lead_performer="Joel Miller",
                                        front_cover=("image/jpeg", "front cover", b"front.jpeg"))

    portfolio = AlbumPortfolio()
    director.create_album_into(portfolio)(
        AlbumCreationProperties(Album.Type.MP3, "album", tmpdir.strpath, track_location=track_location))
    album = portfolio[0]

    assert_that(album.release_name, equal_to("Honeycomb"), "imported release name")
    assert_that(album.images, contains(has_property("data", b"front.jpeg")), "imported images")
    assert_that(album.type, equal_to("mp3"))
    assert_that(album.tracks, contains(has_properties(track_title="Smash Smash")))


def test_adds_to_album_all_album_compatible_audio_files_found_in_selected_folder(recordings):
    recordings.add_mp3(track_title='Rolling in the Deep')
    recordings.add_flac(track_title='Someone Like Me')
    recordings.add_mp3(track_title='Set Fire to the Rain')

    album = build.album(of_type="mp3")
    director.add_tracks_to(album)([recordings.root])

    assert_that(album.tracks, contains_inanyorder(
        has_properties(track_title='Rolling in the Deep'),
        has_properties(track_title='Set Fire to the Rain')))


def test_tags_copy_of_original_recording_with_complete_metadata(mp3):
    album = build.album(release_name='Album Title',
                        lead_performer='Album Artist',
                        images=[build.image(mime='image/jpeg', data=b'<image data>')])
    track = build.track(filename=mp3(),
                        track_title='Track Title',
                        album=album)

    destination_file = os.path.join(os.path.dirname(track.filename), 'tagged.mp3')
    director.record_track(destination_file, track, NOW)

    metadata = tagging.load_metadata(destination_file)
    assert_that(metadata, has_entries(release_name='Album Title', lead_performer='Album Artist'), 'metadata tags')
    assert_that(metadata.images, contains(Image(mime='image/jpeg', data=b'<image data>')), 'attached pictures')


def test_does_not_update_track_with_album_lead_performer_when_album_is_a_compilation(mp3):
    album = build.album(lead_performer='Various Artists', compilation=True)
    track = build.track(filename=mp3(), lead_performer='Track Artist', album=album)

    tagged_file = mp3()
    director.record_track(tagged_file, track, NOW)

    metadata = tagging.load_metadata(tagged_file)
    assert_that(metadata, has_entries(lead_performer='Track Artist'), 'metadata tags')


def test_adds_version_information_to_tags(mp3):
    track = build.track(filename=mp3(), album=build.album())

    tagged_file = mp3()
    director.record_track(tagged_file, track, NOW)

    metadata = tagging.load_metadata(tagged_file)
    assert_that(metadata, has_entries(tagger='TGiT', tagger_version=tgit.__version__,
                                      tagging_time="2014-03-23 16:44:33 +0000"))


def test_gracefully_handles_when_tagging_original_recording(mp3):
    original_file = mp3()
    track = build.track(filename=original_file, album=build.album())

    director.record_track(original_file, track, datetime.now())


def test_tags_file_to_same_directory_under_artist_and_title_name():
    album = build.album(lead_performer='artist')
    track = build.track(filename='track.mp3', track_title='title')
    for t in (build.track(), build.track(), track):
        album.addTrack(t)

    assert_that(director.tagged_name(track), equal_to('artist - 03 - title.mp3'), 'name of tagged file')


def test_exports_album_as_csv_encoded_file(tmpdir):
    album = build.album(tracks=[build.track(track_title="Les Comédiens")])
    destination_file = tmpdir.join("french.csv").strpath

    director.export_as_csv(album)(destination_file)

    def read_lines(file):
        content = open(file, 'r', encoding="windows-1252").read()
        return content.split("\n")

    assert_that(read_lines(destination_file), has_item(contains_string("Les Comédiens")))


def test_changes_main_album_cover_to_specified_image_file():
    album = build.album()
    album.addFrontCover(mime='image/gif', data='old cover')

    cover_file = resources.path('front-cover.jpg')
    director.change_cover_of(album)(cover_file)

    assert_that(album.images, contains(has_properties(mime='image/jpeg',
                                                      data=fs.binary_content_of(cover_file),
                                                      type=Image.FRONT_COVER,
                                                      desc='Front Cover')), 'images')


def test_stops_playing_track_if_already_playing():
    player = doubles.audio_player()
    track = build.track()
    player.play(track)

    director.play_or_stop(player)(track)

    assert_that(player.is_playing(track), is_(False), 'stopped playing')


def test_plays_track_if_not_already_playing():
    player = doubles.audio_player()
    track = build.track()

    director.play_or_stop(player)(track)

    assert_that(player.is_playing(track), is_(True), 'started playing')


def test_moves_track_of_album():
    chevere = build.track(track_title='Chevere!')
    salsa_coltrane = build.track(track_title='Salsa Coltrane')
    honeycomb = build.album(tracks=[salsa_coltrane, chevere])

    director.move_track_of(honeycomb)(salsa_coltrane, 1)
    assert_that(honeycomb.tracks, contains(chevere, salsa_coltrane), 'reordered tracks')


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
                             track_title='Title', lead_performer='Artist', versionInfo='Version',
                             featuredGuest='Featuring', lyricist='Lyricist', composer='Composer',
                             publisher='Publisher', isrc='ZZZ123456789', labels='Tags', lyrics='Lyrics\nLyrics\n...',
                             language='und')

        assert_that(track.track_title, equal_to('Title'), 'track title')
        assert_that(track.lead_performer, equal_to('Artist'), 'lead performer')
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
                             release_name='Title', compilation=True, lead_performer='Artist', isni='0000123456789',
                             guestPerformers=[('Guitar', 'Guitarist')], label_name='Label',
                             catalogNumber='XXX123456789', upc='123456789999', comments='Comments\n...',
                             releaseTime='2009-01-01', recording_time='2008-09-15', recordingStudios='Studios',
                             producer='Producer', mixer='Engineer', primary_style='Style')

        assert_that(album.release_name, equal_to('Title'), 'release name')
        assert_that(album.compilation, is_(True), 'compilation')
        assert_that(album.lead_performer, equal_to('Artist'), 'lead performer')
        assert_that(album.isni, equal_to('0000123456789'), 'isni')
        assert_that(album.guestPerformers, equal_to([('Guitar', 'Guitarist')]), 'guest performers')
        assert_that(album.label_name, equal_to('Label'), 'label name')
        assert_that(album.catalogNumber, equal_to('XXX123456789'), 'catalog number')
        assert_that(album.upc, equal_to('123456789999'), 'upc')
        assert_that(album.comments, equal_to('Comments\n...'), 'comments')
        assert_that(album.releaseTime, equal_to('2009-01-01'), 'release time')
        assert_that(album.recording_time, equal_to('2008-09-15'), 'recording time')
        assert_that(album.recordingStudios, equal_to('Studios'), 'recording studios')
        assert_that(album.producer, equal_to('Producer'), 'producer')
        assert_that(album.mixer, equal_to('Engineer'), 'mixer')
        assert_that(album.primary_style, equal_to('Style'), 'primary style')

    def testUpdatesTracksLeadPerformerWhenAlbumIsNotACompilation(self):
        album = build.album(tracks=[build.track(), build.track(), build.track()])
        director.updateAlbum(album, compilation=False, lead_performer='Album Artist')

        for track in album.tracks:
            assert_that(track.lead_performer, equal_to('Album Artist'), 'track artist')

    def testClearsAlbumImages(self):
        album = build.album(images=[build.image('image/jpeg', 'image data')])
        director.removeAlbumCover(album)
        assert_that(album.images, equal_to([]), 'images')

    def testReplacesInvalidCharactersForFileNamesWithUnderscores(self):
        assert_that(director.sanitize('1/2<3>4:5"6/7\\8?9*10|'), equal_to('1_2_3_4_5_6_7_8_9_10_'), 'sanitized name')

    def testStripsLeadingAndTrailingWhitespaceFromFileNames(self):
        assert_that(director.sanitize('  filename   '), equal_to('filename'), 'sanitized name')

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
        track = build.track(lead_performer='artist')
        album = build.album(tracks=[track], compilation=False)

        director.selectISNI(identity, album)
        assert_that(album.lead_performer, equal_to(name), 'lead performer')
        assert_that(track.lead_performer, equal_to(name), 'lead performer')

    def testClearsLeadPerformerISNIFromAlbum(self):
        album = build.album(isni='0000123456789')
        director.clearISNI(album)
        assert_that(album.isni, none(), 'isni')

    def testAssignsISNIToLeadPerformerUsingTheAlbumTitle(self):
        class NameRegistry:
            def assign(self, forename, surname, titleOfWorks):
                if forename == 'Paul' and surname == 'McCartney' and titleOfWorks[0] == 'Memory Almost Full':
                    return '0000123456789'
                return None

        album = build.album(lead_performer='Paul McCartney', release_name='Memory Almost Full')
        assert_that(director.assign_isni(NameRegistry(), album), equal_to('0000123456789'), 'isni assigned')

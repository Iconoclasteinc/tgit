# -*- coding: utf-8 -*-
import os
import unittest

from hamcrest import (assert_that, equal_to, is_, contains, has_properties, none, has_item, empty, contains_string,
                      has_key, has_property)

from hamcrest.core.helpers.wrap_matcher import wrap_matcher
import pytest

from test.util import builders as build, resources, doubles
from test.util.builders import make_album, make_track
from test.util.workspace import AlbumWorkspace
from tgit import album_director as director
from tgit.album import Album
from tgit.album_portfolio import AlbumPortfolio
from tgit.metadata import Image, Metadata
from tgit.util import fs


@pytest.yield_fixture
def recordings(tmpdir):
    library = doubles.recording_library(tmpdir.mkdir("library"))
    yield library
    library.delete()


@pytest.yield_fixture
def workspace(tmpdir):
    album_workspace = AlbumWorkspace(tmpdir.mkdir("workspace"))
    yield album_workspace
    album_workspace.delete()


@pytest.fixture
def track_catalog():
    class Catalog:
        def __init__(self):
            self.tracks = {}

        def add_track(self, filename='track.mp3', metadata=None, **meta):
            track = make_track(filename, metadata, **meta)
            self.tracks[filename] = track
            return track

        def load_track(self, filename):
            try:
                return self.tracks[filename]
            except:
                raise Exception("{} not found".format(filename))

    return Catalog()


@pytest.fixture
def album_catalog():
    class Catalog:
        def __init__(self):
            self._albums = {}

        def album_exists(self, filename):
            return filename in self._albums

        def load_album(self, filename):
            return self._albums[filename]

        def save_album(self, album):
            self._albums[album.filename] = album

        add = save_album

        def assert_contains(self, album):
            assert_that(self._albums, has_key(album.filename), "list of albums in catalog")
            assert_that(self._albums[album.filename], wrap_matcher(album), "album {}".format(album.filename))

    return Catalog()


@pytest.fixture
def portfolio():
    return AlbumPortfolio()


def make_filename(location, name):
    return os.path.join(location, name, "{0}.tgit".format(name))


def test_creates_and_adds_album_to_porfolio_and_catalog(portfolio, album_catalog):
    director.create_album_into(portfolio, to_catalog=album_catalog)(type_=Album.Type.MP3, name="album",
                                                                    location="workspace")

    assert_that(portfolio,
                contains(has_properties(type="mp3", filename=make_filename("workspace", "album"))),
                "albums in portfolio")
    album_catalog.assert_contains(portfolio[0])


def test_creates_album_using_the_name_as_release_name(portfolio, album_catalog):
    director.create_album_into(portfolio, to_catalog=album_catalog)(type_="...", name="album", location="...")

    assert_that(portfolio[0], has_property("release_name", "album"), "album with release name")


def test_imports_album_from_an_existing_track(portfolio, album_catalog, track_catalog):
    track_catalog.add_track(filename="smash", metadata=Metadata(release_name="Honeycomb"), track_title="Smash Smash")

    director.create_album_into(portfolio, to_catalog=album_catalog, from_catalog=track_catalog)(
        type_=Album.Type.MP3, name="album", location="workspace", reference_track_file="smash")

    assert_that(portfolio, contains(has_properties(type="mp3", release_name="album",
                                                   tracks=contains(has_properties(track_title="Smash Smash")))),
                "imported albums in portfolio")


def test_loads_album_from_catalog_into_portfolio(portfolio, album_catalog):
    target_album = build.album("album.tgit")
    album_catalog.add(target_album)

    director.load_album_into(portfolio, from_catalog=album_catalog)(filename="album.tgit")

    assert_that(portfolio, contains(target_album), "album portfolio")


def test_checks_if_album_exists_in_catalog(album_catalog):
    album_catalog.save_album(make_album(make_filename("workspace", "existing")))
    assert_that(director.album_exists("existing", "workspace", in_catalog=album_catalog), is_(True),
                "found existing album")
    assert_that(director.album_exists("new", "workspace", in_catalog=album_catalog), is_(False),
                "found brand new album")


def test_removes_album_from_portfolio(portfolio):
    album = build.album()
    portfolio.add_album(album)
    director.remove_album_from(portfolio)(album)
    assert_that(portfolio, empty(), "album portfolio")


def test_adds_selected_tracks_to_album_in_order(track_catalog):
    tracks = [track_catalog.add_track(filename) for filename in ("first.mp3", "second.mp3", "third.mp3")]

    album = build.album()
    director.add_tracks(album, "first.mp3", "second.mp3", "third.mp3", from_catalog=track_catalog)

    assert_that(album.tracks, contains(*tracks), "tracks added to album")


def test_ignores_invalid_tracks(track_catalog):
    valid_track = track_catalog.add_track("valid.mp3")

    album = build.album()
    director.add_tracks(album, "invalid.mp3", "valid.mp3", from_catalog=track_catalog)

    assert_that(album.tracks, contains(valid_track), "valid tracks in album")


def test_exports_album_as_csv_encoded_file(workspace):
    album = build.album(tracks=[build.track(track_title="Les Comédiens")])
    destination_file = workspace.file("french.csv")

    director.export_as_csv(album, destination_file)

    def read_lines(file):
        content = open(file, "r", encoding="windows-1252").read()
        return content.split("\n")

    assert_that(read_lines(destination_file), has_item(contains_string("Les Comédiens")))


def test_changes_main_album_cover_to_specified_image_file():
    album = build.album()
    album.addFrontCover(mime='image/gif', data='old cover')

    cover_file = resources.path('front-cover.jpg')
    director.change_cover_of(album)(cover_file)

    assert_that(album.images, contains(has_properties(mime='image/jpeg',
                                                      data=fs.read(cover_file),
                                                      type=Image.FRONT_COVER,
                                                      desc='Front Cover')), 'images')


def test_moves_track_of_album():
    chevere = build.track(track_title='Chevere!')
    salsa_coltrane = build.track(track_title='Salsa Coltrane')
    honeycomb = build.album(tracks=[salsa_coltrane, chevere])

    director.move_track_of(honeycomb)(salsa_coltrane, 1)
    assert_that(honeycomb.tracks, contains(chevere, salsa_coltrane), 'reordered tracks')


class AlbumDirectorTest(unittest.TestCase):
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

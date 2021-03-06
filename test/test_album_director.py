# -*- coding: utf-8 -*-
import os

import pytest
from flexmock import flexmock as mock
from hamcrest import (assert_that, equal_to, is_, contains, has_properties, has_key, has_property,
                      match_equality)
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from cute.prober import PollingProber
from test.test_signal import Subscriber
from testing import builders as build, doubles
from testing.builders import make_album, make_track
from testing.workspace import AlbumWorkspace
from tgit import album_director as director
from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.unit


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

        def add_track(self, filename="track.mp3", metadata=None, **meta):
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
            self._projects = {}

        def project_exists(self, filename):
            return filename in self._projects

        def load_project(self, filename):
            return self._projects[filename]

        def save_project(self, album):
            self._projects[album.filename] = album

        add = save_project

        def assert_contains(self, album):
            assert_that(self._projects, has_key(album.filename), "list of albums in catalog")
            assert_that(self._projects[album.filename], wrap_matcher(album), "album {}".format(album.filename))

    return Catalog()


@pytest.fixture()
def prober():
    return PollingProber()


def make_filename(location, name):
    return os.path.join(location, name, "{0}.tgit".format(name))


def test_checks_if_album_exists_in_catalog(album_catalog):
    album_catalog.save_project(make_album(make_filename("workspace", "existing")))
    assert_that(director.album_exists("existing", "workspace", in_catalog=album_catalog), is_(True),
                "found existing album")
    assert_that(director.album_exists("new", "workspace", in_catalog=album_catalog), is_(False),
                "found brand new album")


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


def test_moves_track_of_album():
    chevere = build.track(track_title="Chevere!")
    salsa_coltrane = build.track(track_title="Salsa Coltrane")
    honeycomb = build.album(tracks=[salsa_coltrane, chevere])

    director.move_track_of(honeycomb)(0, 1)
    assert_that(honeycomb.tracks, contains(chevere, salsa_coltrane), "reordered tracks")


def test_updates_album_metadata():
    album = build.album()
    director.update_album_from(album)(release_name="Title", compilation=False, lead_performer="Artist",
                                      guestPerformers=[("Guitar", "Guitarist")], label_name="Label",
                                      catalogNumber="XXX123456789", upc="123456789999", comments="Comments\n...",
                                      releaseTime="2009-01-01", recording_time="2008-09-15", recordingStudios="Studios",
                                      music_producer="Producer", mixer="Engineer", primary_style="Style")

    assert_that(album.release_name, equal_to("Title"), "release name")
    assert_that(album.compilation, is_(False), "compilation")
    assert_that(album.lead_performer, equal_to("Artist"), "lead performer")
    assert_that(album.guestPerformers, equal_to([("Guitar", "Guitarist")]), "guest performers")
    assert_that(album.label_name, equal_to("Label"), "label name")
    assert_that(album.catalogNumber, equal_to("XXX123456789"), "catalog number")
    assert_that(album.upc, equal_to("123456789999"), "upc")
    assert_that(album.comments, equal_to("Comments\n..."), "comments")
    assert_that(album.releaseTime, equal_to("2009-01-01"), "release time")
    assert_that(album.recording_time, equal_to("2008-09-15"), "recording time")
    assert_that(album.recordingStudios, equal_to("Studios"), "recording studios")
    assert_that(album.music_producer, equal_to("Producer"), "producer")
    assert_that(album.mixer, equal_to("Engineer"), "mixer")
    assert_that(album.primary_style, equal_to("Style"), "primary style")


def test_updates_album_main_artist_when_album_is_a_compilation():
    album = build.album()
    director.update_album_from(album)(compilation=True, lead_performer="Artist")

    assert_that(album.compilation, is_(True), "compilation")
    assert_that(album.lead_performer, equal_to(""), "lead performer")


def test_updates_album_main_artist_region_when_album_is_a_compilation():
    album = build.album()
    director.update_album_from(album)(compilation=True, lead_performer_region=("CA", "MTL"))

    assert_that(album.compilation, is_(True), "compilation")
    assert_that(album.lead_performer_region, is_(None), "lead performer region")


def test_updates_album_main_artist_date_of_birth_when_album_is_a_compilation():
    album = build.album()
    director.update_album_from(album)(compilation=True, lead_performer_date_of_birth="2009-05-06")

    assert_that(album.compilation, is_(True), "compilation")
    assert_that(album.lead_performer_date_of_birth, equal_to("2000-01-01"), "lead performer date of birth")


def test_updates_tracks_main_artist_when_album_is_not_a_compilation():
    album = build.album(tracks=[build.track(), build.track(), build.track()])
    director.update_album_from(album)(lead_performer="Album Artist")

    for track in album.tracks:
        assert_that(track.lead_performer, equal_to("Album Artist"), "track artist")


def test_clears_album_images():
    album = build.album(images=[build.image("image/jpeg", "image data")])
    director.remove_album_cover_from(album)()
    assert_that(album.images, equal_to([]), "images")


def test_returns_isni_from_local_map():
    album = make_album(isnis={"Joel Miller": "00000000123456789"})

    assert_that(director.lookup_isni_in(album)("Joel Miller"), equal_to("00000000123456789"), "isni")


def test_returns_none_when_name_not_found_in_local_map():
    album = make_album(isnis={"Joel Miller": "00000000123456789"})

    assert_that(director.lookup_isni_in(album)("Rebecca Ann Maloy"), equal_to(""), "isni")


def test_signals_when_adding_ipi_to_local_map():
    project = make_album()
    subscriber = Subscriber()
    project.metadata_changed.subscribe(subscriber)

    director.add_ipi_to(project)("Joel Miller", "0000000123456789")

    assert_that(subscriber.events, contains(contains(has_property("ipis", {"Joel Miller": "0000000123456789"}))),
                "project changed events")


def test_updates_preferences():
    preferences = UserPreferences()

    director.update_preferences(preferences)({"locale": "fr_CA"})

    assert_that(preferences.locale, equal_to("fr_CA"), "preferred locale")


def _to_joel_miller():
    return {
        "id": "0000000121707484",
        "type": "individual",
        "firstName": "Joel",
        "lastName": "Miller",
        "works": [
            {"title": "Chevere!"}
        ]
    }


def _that_is_joel_miller():
    return has_properties(id="0000000121707484",
                          type="individual",
                          first_name="Joel",
                          last_name="Miller",
                          works=contains(has_property("title", "Chevere!")))

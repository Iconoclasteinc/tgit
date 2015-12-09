# -*- coding: utf-8 -*-
from concurrent.futures import Future
import os

from hamcrest import (assert_that, equal_to, is_, contains, has_properties, none, has_item, empty, contains_string,
                      has_key, has_property)

from hamcrest.core.helpers.wrap_matcher import wrap_matcher
import pytest

from cute.prober import PollingProber
from cute.probes import ValueMatcherProbe
from tgit.identity import IdentityCard
from test.util import builders as build, resources, doubles
from test.util.builders import make_album, make_track
from test.util.workspace import AlbumWorkspace
from tgit import album_director as director
from tgit.album import Album
from tgit.album_portfolio import AlbumPortfolio
from tgit.auth import Session, User
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


@pytest.fixture()
def prober():
    return PollingProber()


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
    album.add_front_cover(mime="image/gif", data="old cover")

    cover_file = resources.path("front-cover.jpg")
    director.change_cover_of(album)(cover_file)

    assert_that(album.images, contains(has_properties(mime="image/jpeg",
                                                      data=fs.read(cover_file),
                                                      type=Image.FRONT_COVER,
                                                      desc="Front Cover")), "images")


def test_moves_track_of_album():
    chevere = build.track(track_title="Chevere!")
    salsa_coltrane = build.track(track_title="Salsa Coltrane")
    honeycomb = build.album(tracks=[salsa_coltrane, chevere])

    director.move_track_of(honeycomb)(0, 1)
    assert_that(honeycomb.tracks, contains(chevere, salsa_coltrane), "reordered tracks")


def test_updates_track_metadata():
    track = make_track()
    director.update_track(track)(track_title="Title", lead_performer=("Artist",), versionInfo="Version",
                                 featuredGuest="Featuring", lyricist=("Lyricist", "0000123456"), composer="Composer",
                                 publisher="Publisher", isrc="ZZZ123456789", labels="Tags",
                                 lyrics="Lyrics\nLyrics\n...", language="und")

    assert_that(track.track_title, equal_to("Title"), "track title")
    assert_that(track.lead_performer, equal_to(("Artist",)), "lead performer")
    assert_that(track.versionInfo, equal_to("Version"), "version info")
    assert_that(track.featuredGuest, equal_to("Featuring"), "featured guest")
    assert_that(track.lyricist, equal_to(("Lyricist", "0000123456")), "lyricist")
    assert_that(track.composer, equal_to("Composer"), "composer")
    assert_that(track.publisher, equal_to("Publisher"), "publisher")
    assert_that(track.isrc, equal_to("ZZZ123456789"), "isrc")
    assert_that(track.labels, equal_to("Tags"), "tags")
    assert_that(track.lyrics, equal_to("Lyrics\nLyrics\n..."), "lyrics")
    assert_that(track.language, equal_to("und"), "language")


def test_signs_user_in():
    session = Session()
    director.sign_in_using(lambda *_: {"email": "the_email", "token": "the_token"}, session)("...", "...")
    assert_that(session.current_user.email, equal_to("the_email"))


def test_signs_user_out():
    session = build.make_registered_session("...", "...")
    director.sign_out_using(session)()
    assert_that(session.current_user.email, none())


def test_returns_list_of_identities_when_isni_found_in_registry(prober):
    class FakeCheddar:
        @staticmethod
        def get_identities(phrase, token):
            future = Future()
            if token == "the token" and phrase == "Rebecca Ann Maloy":
                future.set_result([{"id": "0000000115677274", "type": "individual", "works": []}])
            else:
                future.set_result([])
            return future

    success_signal = ValueMatcherProbe("The identities", contains(has_property("id", "0000000115677274")))
    director.lookup_isni_using(FakeCheddar(), User(api_key="the token"))("Rebecca Ann Maloy", success_signal.received)
    prober.check(success_signal)


def test_returns_empty_list_when_isni_is_not_found_in_registry(prober):
    class FakeCheddar:
        @staticmethod
        def get_identities(*_):
            future = Future()
            future.set_result([])
            return future

    success_signal = ValueMatcherProbe("The identities", empty())
    director.lookup_isni_using(FakeCheddar(), User(api_key="the token"))("Rebecca Ann Maloy", success_signal.received)
    prober.check(success_signal)


def test_updates_isni_from_selected_identity():
    identity = IdentityCard(id="0000000115677274", firstName="Joel", lastName="Miller", type=IdentityCard.INDIVIDUAL)
    album = build.album(compilation=False)

    director.select_isni_in(album)(identity)
    assert_that(album.lead_performer, equal_to(("Joel Miller", "0000000115677274")), "lead performer")


def test_updates_lead_performer_from_selected_identity():
    identity = IdentityCard(id="0000000115677274", firstName="Paul", lastName="McCartney", type=IdentityCard.INDIVIDUAL)
    track = build.track(lead_performer=("artist",))
    album = build.album(tracks=[track], compilation=False)

    director.select_isni_in(album)(identity)
    assert_that(album.lead_performer, equal_to(("Paul McCartney", "0000000115677274")), "lead performer")
    assert_that(track.lead_performer, equal_to(("Paul McCartney", "0000000115677274")), "lead performer")


def test_updates_album_metadata():
    album = build.album()
    director.update_album_from(album)(release_name="Title", compilation=True, lead_performer=("Artist", "000123456789"),
                                      guestPerformers=[("Guitar", "Guitarist")], label_name="Label",
                                      catalogNumber="XXX123456789", upc="123456789999", comments="Comments\n...",
                                      releaseTime="2009-01-01", recording_time="2008-09-15", recordingStudios="Studios",
                                      music_producer="Producer", mixer="Engineer", primary_style="Style")

    assert_that(album.release_name, equal_to("Title"), "release name")
    assert_that(album.compilation, is_(True), "compilation")
    assert_that(album.lead_performer, equal_to(("Artist", "000123456789")), "lead performer")
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


def test_updates_tracks_lead_performer_when_album_is_not_a_compilation():
    album = build.album(tracks=[build.track(), build.track(), build.track()])
    director.update_album_from(album)(compilation=False, lead_performer=("Album Artist",))

    for track in album.tracks:
        assert_that(track.lead_performer, equal_to(("Album Artist",)), "track artist")


def test_clears_album_images():
    album = build.album(images=[build.image("image/jpeg", "image data")])
    director.remove_album_cover_from(album)()
    assert_that(album.images, equal_to([]), "images")


def test_assigns_isni_to_main_artist(prober):
    class FakeCheddar:
        @staticmethod
        def assign_identifier(name, type_, works, token):
            future = Future()
            if token == "the token" and name == "Joel Miller" and type_ == "individual" and works[0] == "Chevere!":
                future.set_result(_to_joel_miller())
            else:
                future.set_result(None)
            return future

    album = build.album(lead_performer=("Joel Miller",))
    album.add_track(build.track(track_title="Chevere!"))

    success_signal = ValueMatcherProbe("An identity", _that_is_joel_miller())

    director.assign_isni_to_main_artist_using(FakeCheddar(), User(api_key="the token"))(album, "individual",
                                                                                        success_signal.received)
    prober.check(success_signal)


def test_assigns_isni_to_lyricist(prober):
    class FakeCheddar:
        @staticmethod
        def assign_identifier(name, type_, works, token):
            future = Future()
            if token == "the token" and name == "Joel Miller" and type_ == "individual" and works[0] == "Chevere!":
                future.set_result(_to_joel_miller())
            else:
                future.set_result(None)
            return future

    track = build.track(track_title="Chevere!", lyricist=("Joel Miller",))
    success_signal = ValueMatcherProbe("An identity", _that_is_joel_miller())

    director.assign_isni_to_lyricist_using(FakeCheddar(), User(api_key="the token"))(track, success_signal.received)
    prober.check(success_signal)


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

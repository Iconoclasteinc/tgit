# -*- coding: utf-8 -*-
import os

import pytest
from hamcrest import assert_that, contains, has_property, equal_to, empty, is_, has_entry, has_entries

from testing import builders as build, mp3_file
from testing import resources
from testing.builders import make_track, make_metadata
from tgit import fs
from tgit.album import Album
from tgit.local_storage import local_project
from tgit.local_storage.local_project import TRACKS_FOLDER_NAME, ARTWORK_FOLDER_NAME
from tgit.metadata import Image

pytestmark = pytest.mark.unit

sample_front_cover = "image/jpeg", fs.read(resources.path("front-cover.jpg")), Image.FRONT_COVER, "Front Cover"


def simple_naming(track):
    return track.track_title + ".mp3"


@pytest.yield_fixture
def project_file(tmpdir):
    folder = tmpdir.join("album")

    def filename(*paths):
        return folder.join(*paths).strpath

    yield filename
    folder.remove()


@pytest.yield_fixture
def mp3(tmpdir):
    folder = tmpdir.mkdir("mp3s")

    def maker(**tags):
        return mp3_file.make(to=folder.strpath, **tags).filename

    yield maker
    folder.remove()


def has_filename(filename):
    return has_property('filename', filename)


def test_round_trips_album_metadata_and_tracks_to_disk(project_file, mp3):
    album_file = project_file("album.tgit")
    original_tracks = (build.track(mp3(), track_title=title) for title in ("1st", "2nd", "3rd"))

    original_album = build.album(filename=album_file,
                                 version="1.11.0",
                                 type=Album.Type.FLAC,
                                 lead_performer="Artist",
                                 images=[sample_front_cover],
                                 tracks=original_tracks)

    local_project.save_project(original_album, track_name=lambda track: track.track_title + ".mp3")
    delete_from_disk(*original_tracks)
    stored_album = local_project.load_project(album_file)

    assert_that(stored_album.type, equal_to(Album.Type.FLAC), "type")
    assert_that(stored_album.lead_performer, equal_to("Artist"), "lead performer")
    assert_that(stored_album.images, contains(Image(*sample_front_cover)), "images")
    assert_that(stored_album.tracks, contains(has_filename(project_file(TRACKS_FOLDER_NAME, "1st.mp3")),
                                              has_filename(project_file(TRACKS_FOLDER_NAME, "2nd.mp3")),
                                              has_filename(project_file(TRACKS_FOLDER_NAME, "3rd.mp3")), ), "tracks")


def test_round_trips_chain_of_title_to_disk(project_file, mp3):
    album_file = project_file("album.tgit")
    metadata = make_metadata(track_title="Chevere!", lyricist=["Joel Miller"], composer=["John Roney"],
                             publisher=["Effendi Records"])

    original_filename = mp3()
    original_track = make_track(original_filename, metadata_from=metadata)
    original_track.load_chain_of_title({
        "authors_composers": {"Joel Miller": joel_miller(), "John Roney": john_roney()},
        "publishers": {"Effendi Records": effendi_records()}
    })

    original_album = build.album(filename=album_file, version="2.4.0", type=Album.Type.FLAC,
                                 lead_performer="Joel Miller", tracks=[original_track])

    local_project.save_project(original_album, track_name=lambda current_track: current_track.track_title + ".mp3")
    os.remove(original_filename)
    track = local_project.load_project(album_file).tracks[0]

    assert_that(track.chain_of_title.contributors, has_author_composer("Joel Miller", joel_miller()),
                "The contributors")
    assert_that(track.chain_of_title.contributors, has_author_composer("John Roney", john_roney()), "The contributors")
    assert_that(track.chain_of_title.contributors, has_publisher("Effendi Records", effendi_records()),
                "The contributors")


def test_remove_previous_artwork_and_tracks(project_file, mp3):
    album_file = project_file("album.tgit")
    tracks = (build.track(mp3(), track_title=title) for title in ("1st", "2nd", "3rd"))
    album = build.album(filename=album_file,
                        images=[sample_front_cover],
                        tracks=tracks)

    local_project.save_project(album, simple_naming)

    for position in reversed(range(len(album))):
        album.remove_track(position)

    album.remove_images()

    local_project.save_project(album, simple_naming)

    assert_that(fs.list_dir(project_file(TRACKS_FOLDER_NAME)), empty(), "track files left")
    assert_that(fs.list_dir(project_file(ARTWORK_FOLDER_NAME)), empty(), "artwork files left")


def test_migrates_to_v1_11():
    stored_album = local_project.load_project(resources.path("album-v1.9.tgit"))

    assert_that(stored_album.isnis, has_entry("Artist", "0000000123456789"), "lead performer identity")


def test_checks_if_album_exists_in_catalog(project_file):
    album_file = project_file("existing.tgit")
    touch(album_file)

    assert_that(local_project.project_exists(album_file), is_(True), "found existing album file on disk")
    assert_that(local_project.project_exists(project_file("missing.tgit")), is_(False), "found new album file on disk")


def delete_from_disk(*tracks):
    for track in tracks:
        os.remove(track.filename)


def touch(filename):
    fs.mkdirs(os.path.dirname(filename))
    fs.write(filename, b"")


def has_author_composer(name, contributor):
    return has_entry("authors_composers", has_entry(name, has_entries(contributor)))


def has_publisher(name, contributor):
    return has_entry("publishers", has_entry(name, has_entries(contributor)))


def joel_miller():
    return dict(name="Joel Miller", affiliation="SOCAN", publisher="Effendi Records", share="25")


def john_roney():
    return dict(name="John Roney", affiliation="ASCAP", publisher="Effendi Records", share="25")


def effendi_records():
    return dict(name="Effendi Records", share="25")

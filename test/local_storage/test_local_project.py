# -*- coding: utf-8 -*-
import os

from hamcrest import assert_that, contains, has_property, equal_to
import pytest

from test.util import builders as build, mp3_file, resources
from tgit.album import Album
from tgit.local_storage import local_project
from tgit.metadata import Image
from tgit.util import fs

sample_front_cover = "image/jpeg", fs.read(resources.path("front-cover.jpg")), Image.FRONT_COVER, "Front Cover"


@pytest.yield_fixture
def project_file(tmpdir):
    folder = tmpdir.mkdir("album")

    def path(filename):
        return folder.join(filename).strpath

    yield path
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
                                 type=Album.Type.FLAC,
                                 lead_performer="Artist",
                                 images=[sample_front_cover],
                                 tracks=original_tracks)

    local_project.save_album(original_album, track_name=lambda track: track.track_title + ".mp3")
    delete_from_disk(*original_tracks)
    stored_album = local_project.load_album(album_file)

    assert_that(stored_album.type, equal_to(Album.Type.FLAC), "type")
    assert_that(stored_album.lead_performer, equal_to("Artist"), "lead performer")
    assert_that(stored_album.images, contains(Image(*sample_front_cover)), "images")
    assert_that(stored_album.tracks, contains(has_filename(project_file("1st.mp3")),
                                              has_filename(project_file("2nd.mp3")),
                                              has_filename(project_file("3rd.mp3")), ), "tracks")


def delete_from_disk(*tracks):
    for track in tracks:
        os.remove(track.filename)

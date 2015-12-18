# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta

import pytest
from hamcrest import has_properties, has_entries, contains, equal_to, assert_that, is_not, has_key

import tgit
from test.util import builders as build, mp3_file
from tgit.metadata import Image
from tgit.tagging import tagging

NOW = datetime(2014, 3, 23, 16, 44, 33, tzinfo=timezone(-timedelta(hours=4)))


@pytest.yield_fixture
def mp3(tmpdir):
    def maker(**tags):
        return mp3_file.make(to=tmpdir.strpath, **tags).filename

    yield maker
    tmpdir.remove()


def test_loads_track_from_metadata_embedded_in_file(mp3):
    track_file = mp3(track_title='Chaconne')
    track = tagging.load_track(track_file)
    assert_that(track, has_properties(track_title='Chaconne'))


def test_round_trips_track_and_album_metadata(mp3):
    album = build.album(release_name="Album Title", lead_performer=("Album Artist",),
                        isnis={"Album Artist": "0000000123456789"},
                        images=[build.image(mime="image/jpeg", data=b"<image data>")])
    track = build.track(filename=mp3(), track_title="Track Title", album=album)

    tagging.save_track(track)

    track = tagging.load_track(track.filename)
    assert_that(track.metadata, has_entries(release_name="Album Title",
                                            lead_performer=("Album Artist",),
                                            isnis={"Album Artist": "0000000123456789"},
                                            track_title="Track Title"), "metadata tags")
    assert_that(track.metadata, is_not(has_key("isni")), "metadata tags")
    assert_that(track.metadata.images, contains(Image(mime="image/jpeg", data=b"<image data>")), "attached pictures")


def test_does_not_update_track_with_album_lead_performer_when_album_is_a_compilation(mp3):
    album = build.album(lead_performer=("Various Artists",), compilation=True)
    track = build.track(filename=mp3(), lead_performer=("Track Artist",), album=album)

    tagging.save_track(track)

    track = tagging.load_track(track.filename)
    assert_that(track.lead_performer, equal_to(("Track Artist",)), "lead performer")


def test_adds_version_information_to_tags(mp3):
    track = build.track(filename=mp3(), album=build.album())

    tagging.save_track(track, at_time=NOW)

    track = tagging.load_track(track.filename)
    assert_that(track, has_properties(tagger='TGiT',
                                      tagger_version=tgit.__version__,
                                      tagging_time="2014-03-23 20:44:33"))

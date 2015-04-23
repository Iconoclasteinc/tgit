# -*- coding: utf-8 -*-

import pytest

from test.util import resources, doubles
from test.drivers.application_runner import ApplicationRunner


@pytest.yield_fixture
def library(tmpdir):
    recordings = doubles.recording_library(tmpdir.strpath)
    yield recordings
    recordings.delete()


@pytest.yield_fixture
def app():
    runner = ApplicationRunner()
    runner.start()
    yield runner
    runner.stop()


def test_tagging_an_mp3_track(app, library):
    track = library.add_mp3(release_name="???", lead_performer="???", track_title="???")

    app.new_album(track, of_type='mp3')

    app.shows_album_metadata(release_name="???", lead_performer="???")
    app.change_album_metadata(front_cover=resources.path("honeycomb.jpg"),
                              release_name="Honeycomb", lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Rashers")

    library.contains("Joel Miller - 01 - Rashers.mp3",
                     front_cover=(resources.path("honeycomb.jpg"), "Front Cover"),
                     release_name="Honeycomb",
                     lead_performer="Joel Miller",
                     track_title="Rashers")


def test_tagging_a_flac_track(app, library):
    track = library.add_flac(release_name="???", lead_performer="???", track_title="???")

    app.new_album(track, of_type='flac')

    app.shows_album_metadata(release_name="???", lead_performer="???")
    app.change_album_metadata(release_name="St-Henri", lead_performer="John Roney")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Squareboy")

    library.contains("John Roney - 01 - Squareboy.flac",
                     release_name="St-Henri",
                     lead_performer="John Roney",
                     track_title="Squareboy")


def test_tagging_an_album_with_several_tracks(app, library):
    tracks = (library.add_mp3(track_title="1 - ???", lead_performer="???"),
              library.add_mp3(track_title="2 - ???", lead_performer="???"),
              library.add_mp3(track_title="3 - ???", lead_performer="???"))

    app.new_album(*tracks)
    app.shows_album_content(["1 - ???"], ["2 - ???"], ["3 - ???"])

    app.shows_album_metadata(lead_performer="???")
    app.change_album_metadata(lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="1 - ???")
    app.change_track_metadata(track_title="Chevere!")

    app.shows_next_track_metadata(track_title="2 - ???")
    app.change_track_metadata(track_title="Zumbar")

    app.shows_next_track_metadata(track_title="3 - ???")
    app.change_track_metadata(track_title="Salsa Coltrane")

    library.contains("Joel Miller - 01 - Chevere!.mp3", lead_performer="Joel Miller", track_title="Chevere!")
    library.contains("Joel Miller - 02 - Zumbar.mp3", lead_performer="Joel Miller", track_title="Zumbar")
    library.contains("Joel Miller - 03 - Salsa Coltrane.mp3", lead_performer="Joel Miller", track_title="Salsa Coltrane")
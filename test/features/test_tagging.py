# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSettings
import pytest

from tgit.preferences import Preferences
from test.util import resources, doubles
from test.drivers.application_runner import ApplicationRunner


@pytest.yield_fixture
def recordings(tmpdir):
    library = doubles.recording_library(tmpdir.strpath)
    yield library
    library.delete()


@pytest.yield_fixture
def app():
    runner = ApplicationRunner()
    runner.start(Preferences(QSettings()))
    yield runner
    runner.stop()


def test_tagging_an_mp3_track(app, recordings):
    track = recordings.add_mp3(release_name="???", lead_performer="???", track_title="???")

    app.import_album(track, of_type='mp3')

    app.shows_album_metadata(release_name="???", lead_performer="???")
    app.change_album_metadata(front_cover=resources.path("honeycomb.jpg"),
                              release_name="Honeycomb", lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Rashers")

    recordings.contains("Joel Miller - 01 - Rashers.mp3",
                        front_cover=(resources.path("honeycomb.jpg"), "Front Cover"),
                        release_name="Honeycomb",
                        lead_performer="Joel Miller",
                        track_title="Rashers")


def test_tagging_an_album_with_several_tracks(app, recordings):
    tracks = (recordings.add_mp3(track_title="1 - ???", lead_performer="???"),
              recordings.add_mp3(track_title="2 - ???", lead_performer="???"),
              recordings.add_mp3(track_title="3 - ???", lead_performer="???"))

    app.import_album(*tracks)
    app.shows_album_content(["1 - ???"], ["2 - ???"], ["3 - ???"])

    app.shows_album_metadata(lead_performer="???")
    app.change_album_metadata(lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="1 - ???")
    app.change_track_metadata(track_title="Chevere!")

    app.shows_next_track_metadata(track_title="2 - ???")
    app.change_track_metadata(track_title="Zumbar")

    app.shows_next_track_metadata(track_title="3 - ???")
    app.change_track_metadata(track_title="Salsa Coltrane")

    recordings.contains("Joel Miller - 01 - Chevere!.mp3", lead_performer="Joel Miller", track_title="Chevere!")
    recordings.contains("Joel Miller - 02 - Zumbar.mp3", lead_performer="Joel Miller", track_title="Zumbar")
    recordings.contains("Joel Miller - 03 - Salsa Coltrane.mp3", lead_performer="Joel Miller",
                        track_title="Salsa Coltrane")


def test_tagging_a_flac_track(app, recordings):
    track = recordings.add_flac(release_name="???", lead_performer="???", track_title="???")

    app.import_album(track, of_type='flac')

    app.shows_album_metadata(release_name="???", lead_performer="???")
    app.change_album_metadata(release_name="St-Henri", lead_performer="John Roney")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Squareboy")

    recordings.contains("John Roney - 01 - Squareboy.flac",
                        release_name="St-Henri",
                        lead_performer="John Roney",
                        track_title="Squareboy")


def test_tagging_a_compilation(app, recordings):
    tracks = (recordings.add_mp3(track_title="Big Ideas", lead_performer="???"),
              recordings.add_mp3(track_title="Partways", lead_performer="???"),
              recordings.add_mp3(track_title="Horse Power", lead_performer="???"))

    app.import_album(*tracks)

    app.shows_album_metadata(compilation=False)
    app.change_album_metadata(toggle_compilation=True)

    app.shows_next_track_metadata(track_title="Big Ideas", lead_performer="???")
    app.change_track_metadata(lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="Partways", lead_performer="???")
    app.change_track_metadata(lead_performer="John Roney")

    app.shows_next_track_metadata(track_title="Horse Power", lead_performer="???")
    app.change_track_metadata(lead_performer="Joel Miller")

    recordings.contains("Joel Miller - 01 - Big Ideas.mp3", lead_performer="Joel Miller")
    recordings.contains("John Roney - 02 - Partways.mp3", lead_performer="John Roney")
    recordings.contains("Joel Miller - 03 - Horse Power.mp3", lead_performer="Joel Miller")
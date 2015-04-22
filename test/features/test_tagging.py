# -*- coding: utf-8 -*-

import pytest

from tgit.util import fs
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


def test_tagging_a_new_album_with_several_tracks(app, library):
    tracks = (library.add_mp3(track_title="Ma préférence",
                              releaseName="Jaloux",
                              frontCover=("image/jpeg", "Cover", fs.binary_content_of(resources.path("jaloux.jpg"))),
                              lead_performer="Julien Clerc",
                              labelName="EMI",
                              releaseTime="1978"),
              library.add_mp3(track_title="Fais moi une place",
                              releaseName="Fais moi une place",
                              frontCover=("image/jpeg", "Cover", fs.binary_content_of(resources.path("une-place.jpg"))),
                              labelName="Virgin",
                              releaseTime="1990",
                              upc="3268440307258"),
              library.add_mp3(track_title="Ce n'est rien",
                              releaseName="Niagara",
                              frontCover=("image/jpeg", "Cover", fs.binary_content_of(resources.path("niagara.jpg"))),
                              releaseTime="1971",
                              lyricist="Étienne Roda-Gil"))

    app.new_album('mp3', *tracks)
    app.shows_album_content(["Ma préférence"],
                            ["Fais moi une place"],
                            ["Ce n'est rien"])

    app.shows_album_metadata(releaseName="Jaloux", lead_performer="Julien Clerc", labelName="EMI", releaseTime="1978")
    app.change_album_metadata(releaseName="Best Of", frontCover=resources.path("best-of.jpg"),
                              labelName="EMI Music France", releaseTime="2009-04-06")

    app.shows_next_track_metadata(track_title="Ma préférence")
    app.change_track_metadata(composer="Julien Clerc", lyricist="Jean-Loup Dabadie")

    app.shows_next_track_metadata(track_title="Fais moi une place")
    app.change_track_metadata(composer="Julien Clerc", lyricist="Francoise Hardy")

    app.shows_next_track_metadata(track_title="Ce n'est rien")
    app.change_track_metadata(composer="Julien Clerc")

    library.contains("Julien Clerc - 01 - Ma préférence.mp3",
                     frontCover=(resources.path("best-of.jpg"), "Front Cover"),
                     releaseName="Best Of",
                     lead_performer="Julien Clerc",
                     labelName="EMI Music France",
                     releaseTime="2009-04-06",
                     track_title="Ma préférence",
                     composer="Julien Clerc",
                     lyricist="Jean-Loup Dabadie")
    library.contains("Julien Clerc - 02 - Fais moi une place.mp3",
                     frontCover=(resources.path("best-of.jpg"), "Front Cover"),
                     releaseName="Best Of",
                     lead_performer="Julien Clerc",
                     labelName="EMI Music France",
                     releaseTime="2009-04-06",
                     track_title="Fais moi une place",
                     composer="Julien Clerc",
                     lyricist="Francoise Hardy")
    library.contains("Julien Clerc - 03 - Ce n'est rien.mp3",
                     frontCover=(resources.path("best-of.jpg"), "Front Cover"),
                     releaseName="Best Of",
                     lead_performer="Julien Clerc",
                     labelName="EMI Music France",
                     releaseTime="2009-04-06",
                     track_title="Ce n'est rien",
                     composer="Julien Clerc",
                     lyricist="Étienne Roda-Gil")


def test_tagging_a_flac_track(app, library):
    track = library.add_flac(release_name="???", lead_performer="???", track_title="???")

    app.new_album('flac', track)

    app.shows_album_metadata(release_name="???", lead_performer="???")
    app.change_album_metadata(release_name="St-Henri", lead_performer="John Roney")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Squareboy")

    library.contains("John Roney - 01 - Squareboy.flac",
                     releaseName="St-Henri",
                     lead_performer="John Roney",
                     track_title="Squareboy")
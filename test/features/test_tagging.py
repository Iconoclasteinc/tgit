# -*- coding: utf-8 -*-

import tgit
from test.util import resources


def test_tagging_an_mp3_track(app, recordings, workspace):
    app.new_album("Honeycomb", of_type="mp3")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_album(track)

    app.shows_album_metadata(release_name="Honeycomb", lead_performer="")
    app.change_album_metadata(front_cover=resources.path("honeycomb.jpg"),
                              release_name="Honeycomb", lead_performer="Joel Miller", isni="0000000123456789")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Rashers")

    app.save_album()
    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Rashers.mp3",
                             front_cover=(resources.path("honeycomb.jpg"), "Front Cover"),
                             release_name="Honeycomb",
                             lead_performer=("Joel Miller", "0000000123456789"),
                             track_title="Rashers",
                             track_number=1,
                             tagger_version=tgit.__version__)


def test_tagging_a_flac_track(app, recordings, workspace):
    app.new_album("St-Henri", of_type="flac")

    track = recordings.add_flac(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_album(track)

    app.shows_album_metadata(release_name="St-Henri", lead_performer="")
    app.change_album_metadata(release_name="St-Henri", front_cover=resources.path("st-henri.jpg"),
                              lead_performer="John Roney", isni="0000000123456789")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Squareboy")

    app.save_album()
    workspace.contains_track(album="St-Henri",
                             filename="John Roney - 01 - Squareboy.flac",
                             front_cover=(resources.path("st-henri.jpg"), "Front Cover"),
                             release_name="St-Henri",
                             lead_performer=("John Roney", "0000000123456789"),
                             track_title="Squareboy",
                             track_number=1,
                             tagger_version=tgit.__version__)


def test_tagging_an_album_with_several_tracks(app, recordings, workspace):
    app.new_album("Honeycomb", of_type="mp3")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_album(*tracks)

    app.shows_album_metadata()
    app.change_album_metadata(lead_performer="Joel Miller", isni="0000000123456789")

    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")

    app.save_album()
    workspace.contains_track(album="Honeycomb", filename="Joel Miller - 01 - Chevere!.mp3",
                             lead_performer=("Joel Miller", "0000000123456789"), track_number=1, total_tracks=3)
    workspace.contains_track(album="Honeycomb", filename="Joel Miller - 02 - Zumbar.mp3",
                             lead_performer=("Joel Miller", "0000000123456789"), track_number=2, total_tracks=3)
    workspace.contains_track(album="Honeycomb", filename="Joel Miller - 03 - Salsa Coltrane.mp3",
                             lead_performer=("Joel Miller", "0000000123456789"), track_number=3, total_tracks=3)


def test_tagging_a_compilation(app, recordings, workspace):
    app.new_album("St-Henri", of_type="mp3")

    tracks = (recordings.add_mp3(track_title="Big Ideas"),
              recordings.add_mp3(track_title="Partways"),
              recordings.add_mp3(track_title="Horse Power"))

    app.add_tracks_to_album(*tracks)

    app.shows_album_metadata(compilation=False)
    app.change_album_metadata(lead_performer="???")
    app.change_album_metadata(toggle_compilation=True)

    app.shows_next_track_metadata(track_title="Big Ideas", lead_performer="???")
    app.change_track_metadata(lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="Partways", lead_performer="???")
    app.change_track_metadata(lead_performer="John Roney")

    app.shows_next_track_metadata(track_title="Horse Power", lead_performer="???")
    app.change_track_metadata(lead_performer="Joel Miller")

    app.save_album()
    workspace.contains_track(album="St-Henri", filename="Joel Miller - 01 - Big Ideas.mp3",
                             lead_performer=("Joel Miller",))
    workspace.contains_track(album="St-Henri", filename="John Roney - 02 - Partways.mp3",
                             lead_performer=("John Roney",))
    workspace.contains_track(album="St-Henri", filename="Joel Miller - 03 - Horse Power.mp3",
                             lead_performer=("Joel Miller",))

import pytest

import tgit
from testing import resources

pytestmark = pytest.mark.feature


def test_tagging_an_mp3_track(app, recordings, workspace):
    app.new_project("Honeycomb", of_type="mp3")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_project(track)

    app.shows_project_metadata(release_name="Honeycomb", lead_performer="")
    app.change_project_metadata(front_cover=resources.path("honeycomb.jpg"),
                                release_name="Honeycomb", lead_performer="Joel Miller", isni="0000000121707484")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Rashers", lyricist="Rebecca Ann Maloy", lyricist_ipi="9876543210000000")

    app.save_project()
    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Rashers.mp3",
                             front_cover=(resources.path("honeycomb.jpg"), "Front Cover"),
                             release_name="Honeycomb",
                             lead_performer="Joel Miller",
                             lyricist="Rebecca Ann Maloy",
                             isnis={"Joel Miller": "0000000121707484"},
                             ipis={"Rebecca Ann Maloy": "9876543210000000"},
                             track_title="Rashers",
                             track_number=1,
                             tagger_version=tgit.__version__)


def test_tagging_a_flac_track(app, recordings, workspace):
    app.new_project("St-Henri", of_type="flac")

    track = recordings.add_flac(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_project(track)

    app.shows_project_metadata(release_name="St-Henri", lead_performer="")
    app.change_project_metadata(release_name="St-Henri", front_cover=resources.path("st-henri.jpg"),
                                lead_performer="John Roney", isni="0000000121707484")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Squareboy", lyricist="Rebecca Ann Maloy", lyricist_ipi="9876543210000000")

    app.save_project()
    workspace.contains_track(album="St-Henri",
                             filename="John Roney - 01 - Squareboy.flac",
                             front_cover=(resources.path("st-henri.jpg"), "Front Cover"),
                             release_name="St-Henri",
                             lead_performer="John Roney",
                             lyricist="Rebecca Ann Maloy",
                             isnis={"John Roney": "0000000121707484"},
                             ipis={"Rebecca Ann Maloy": "9876543210000000"},
                             track_title="Squareboy",
                             track_number=1,
                             tagger_version=tgit.__version__)


def test_tagging_an_album_with_several_tracks(app, recordings, workspace):
    app.new_project("Honeycomb", of_type="mp3")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_project(*tracks)

    app.shows_project_metadata()
    app.change_project_metadata(lead_performer="Joel Miller", isni="0000000121707484")

    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")

    app.save_project()
    workspace.contains_track(album="Honeycomb", filename="Joel Miller - 01 - Chevere!.mp3",
                             lead_performer="Joel Miller", isnis={"Joel Miller": "0000000121707484"}, track_number=1,
                             total_tracks=3)
    workspace.contains_track(album="Honeycomb", filename="Joel Miller - 02 - Zumbar.mp3",
                             lead_performer="Joel Miller", isnis={"Joel Miller": "0000000121707484"}, track_number=2,
                             total_tracks=3)
    workspace.contains_track(album="Honeycomb", filename="Joel Miller - 03 - Salsa Coltrane.mp3",
                             lead_performer="Joel Miller", isnis={"Joel Miller": "0000000121707484"}, track_number=3,
                             total_tracks=3)


def test_tagging_a_compilation(app, recordings, workspace):
    app.new_project("St-Henri", of_type="mp3")

    tracks = (recordings.add_mp3(track_title="Big Ideas"),
              recordings.add_mp3(track_title="Partways"),
              recordings.add_mp3(track_title="Horse Power"))

    app.add_tracks_to_project(*tracks)

    app.shows_project_metadata(compilation=False)
    app.change_project_metadata(lead_performer="???")
    app.change_project_metadata(toggle_compilation=True)

    app.shows_next_track_metadata(track_title="Big Ideas", lead_performer="")
    app.change_track_metadata(lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="Partways", lead_performer="")
    app.change_track_metadata(lead_performer="John Roney")

    app.shows_next_track_metadata(track_title="Horse Power", lead_performer="")
    app.change_track_metadata(lead_performer="Joel Miller")

    app.save_project()
    workspace.contains_track(album="St-Henri", filename="Joel Miller - 01 - Big Ideas.mp3",
                             lead_performer="Joel Miller")
    workspace.contains_track(album="St-Henri", filename="John Roney - 02 - Partways.mp3",
                             lead_performer="John Roney")
    workspace.contains_track(album="St-Henri", filename="Joel Miller - 03 - Horse Power.mp3",
                             lead_performer="Joel Miller")

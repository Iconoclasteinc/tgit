import pytest

pytestmark = pytest.mark.feature


def test_navigating_through_the_album_non_linearly(app, recordings):
    app.new_project(of_type="mp3")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_project(*tracks)

    app.shows_track_metadata(track_number=3, track_title="Salsa Coltrane")
    app.shows_track_list(["Chevere!"], ["Zumbar"], ["Salsa Coltrane"])
    app.shows_track_metadata(track_number=2, track_title="Zumbar")
    app.shows_project_metadata()
    app.shows_track_metadata(track_number=1, track_title="Chevere!")

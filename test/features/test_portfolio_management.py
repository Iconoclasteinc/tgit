import pytest

pytestmark = pytest.mark.feature


def test_closing_and_starting_a_new_album(app, recordings):
    app.new_project("album1", of_type="mp3")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_project(track)
    app.shows_track_list(["???"])
    app.close_project()

    app.new_project("album2", of_type="mp3")
    app.shows_track_list()


def test_saving_and_loading_an_album(app, recordings):
    app.new_project("Honeycomb")

    tracks = (recordings.add_mp3(track_title="Chevere!", lead_performer="???"),
              recordings.add_mp3(track_title="Zumbar", lead_performer="???"),
              recordings.add_mp3(track_title="Salsa Coltrane", lead_performer="???"))

    app.add_tracks_to_project(*tracks)
    app.shows_project_metadata()
    app.change_project_metadata(release_name="Honeycomb")
    app.save()
    app.close_project()

    app.load_project("Honeycomb")

    app.shows_track_list(("Chevere!",), ("Zumbar",), ("Salsa Coltrane",))
    app.shows_project_metadata(release_name="Honeycomb")
    app.shows_next_track_metadata(track_title="Chevere!")
    app.shows_next_track_metadata(track_title="Zumbar")
    app.shows_next_track_metadata(track_title="Salsa Coltrane")


def test_importing_an_album_from_an_existing_track(app, recordings):
    track = recordings.add_mp3(release_name="Honeycomb", lead_performer="Joel Miller", track_title="Rashers")

    app.import_project("Honeycomb", from_track=track, of_type="mp3")

    app.shows_project_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.shows_next_track_metadata(track_title="Rashers")


def test_opening_a_recent_project(app):
    app.shows_recent_projects()
    app.new_project("Honeycomb", of_type="mp3")
    app.close_project()
    app.shows_recent_projects("Honeycomb")
    app.new_project("Miron Noir", of_type="flac")
    app.close_project()
    app.shows_recent_projects("Miron Noir", "Honeycomb")
    app.stop()

    app.start()
    app.shows_recent_projects("Miron Noir", "Honeycomb")
    app.open_recent_project("Honeycomb")
    app.shows_project_metadata(release_name="Honeycomb")
    app.change_project_metadata(release_name="Honeycomber")
    app.save_project()
    app.close_project()
    app.shows_recent_projects("Honeycomber", "Miron Noir")

import pytest


@pytest.mark.wip
def test_export_to_soproq_file(app, recordings, workspace):
    app.new_album("Honeycomb", of_type="mp3")

    track = recordings.add_mp3(release_name="ignore", lead_performer="ignore", track_title="???")
    app.add_tracks_to_album(track)

    app.shows_album_metadata(release_name="Honeycomb", lead_performer="")
    app.change_album_metadata(release_name="Honeycomb", lead_performer="Joel Miller")

    app.shows_next_track_metadata(track_title="???")
    app.change_track_metadata(track_title="Rashers",
                              isrc="CA-A01-12-00001")

    app.declare_album_to_soproq(filename="soproq.xlsx")
    workspace.contains_soproq_transmission_file(filename="soproq.xlsx",
                                                track_title="Rashers",
                                                lead_performer="Joel Miller",
                                                isrc="CA-A01-12-00001",
                                                duration="00:00:09")

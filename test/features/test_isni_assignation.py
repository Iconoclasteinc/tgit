import pytest

pytestmark = pytest.mark.feature


@pytest.mark.skip
def test_assigning_an_isni_to_the_main_artist(app, recordings, workspace, platform):
    track = recordings.add_mp3(track_title="Salsa Coltrane", release_name="Honeycomb", lead_performer="Joel Miller")
    platform.token_queue = iter(["TheSuperToken"])
    platform.allowed_bearer_token = "TheSuperToken"
    platform.identities["Joel Miller"] = {
        "id": "0000000121707484",
        "type": "individual",
        "firstName": "Joel",
        "lastName": "Miller",
        "works": [
            {"title": "Honeycombs"}
        ]
    }

    app.sign_in()
    app.import_project("Honeycomb", from_track=track)
    app.shows_track_list(["Salsa Coltrane"])
    app.shows_project_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.assign_isni_to_main_artist()

    app.save_project()
    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Salsa Coltrane.mp3",
                             release_name="Honeycomb",
                             lead_performer="Joel Miller",
                             isnis={"Joel Miller": "0000000121707484"},
                             track_title="Salsa Coltrane")

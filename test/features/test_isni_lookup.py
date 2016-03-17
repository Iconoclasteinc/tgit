import pytest

pytestmark = pytest.mark.feature


def test_finding_the_isni_of_the_main_artist(app, platform, recordings, workspace):
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
    app.import_project("Honeycomb", track)
    app.shows_track_list(["Salsa Coltrane"])
    app.shows_project_metadata(release_name="Honeycomb", lead_performer="Joel Miller")
    app.find_isni_of_main_artist("Joel Miller")

    app.save_project()
    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Salsa Coltrane.mp3",
                             release_name="Honeycomb",
                             lead_performer="Joel Miller",
                             isnis={"Joel Miller": "0000000121707484"},
                             track_title="Salsa Coltrane")

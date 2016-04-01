import pytest

pytestmark = pytest.mark.feature


@pytest.fixture(autouse=True)
def configured_platform(platform):
    platform.token_queue = iter(["TheSuperToken"])
    platform.allowed_bearer_token = "TheSuperToken"
    platform.identities_for_assignation["Joel Miller"] = {
        "id": "0000000123456789",
        "type": "individual",
        "firstName": "Joel",
        "lastName": "Miller",
        "works": [
            {"title": "Chevere!"}
        ]
    }

    return platform


def test_assigning_an_isni_to_the_main_artist(app, recordings, workspace):
    track = recordings.add_mp3(track_title="Chevere!", release_name="Honeycomb", lead_performer="Joel Miller")

    app.sign_in()
    app.import_project("Honeycomb", from_track=track)
    app.assign_isni_to_main_artist()
    app.save_project()

    workspace.contains_track(album="Honeycomb",
                             filename="Joel Miller - 01 - Chevere!.mp3",
                             release_name="Honeycomb",
                             lead_performer="Joel Miller",
                             isnis={"Joel Miller": "0000000123456789"},
                             track_title="Chevere!")

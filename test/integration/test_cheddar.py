import pytest
import requests
from hamcrest import assert_that, empty, contains, has_entries, instance_of

from tgit.cheddar import Cheddar, PermissionDeniedError, AuthenticationError, InsufficientInformationError

pytestmark = pytest.mark.integration


@pytest.yield_fixture
def platform():
    from test.util import cheddar

    server_thread = cheddar.start()
    yield cheddar
    cheddar.stop(server_thread)


@pytest.yield_fixture()
def cheddar(platform):
    cheddar_platform = Cheddar(host=platform.host(), port=platform.port(), secure=False)
    yield cheddar_platform
    cheddar_platform.stop()


def test_authenticates_by_returning_the_token(cheddar, platform):
    platform.token_queue = iter(["token12345"])
    token = cheddar.authenticate("test@example.com", "passw0rd")
    assert_that(token, "token12345", "token")


def test_raises_authentication_error(cheddar):
    with pytest.raises(AuthenticationError):
        wait_for_completion(cheddar.authenticate("test@example.com", "wrong_password"))


def test_returns_unauthorized_when_getting_identities(cheddar, platform):
    platform.allowed_bearer_token = "token"
    identities = cheddar.get_identities("reb an mal", "...")
    assert_that(identities.exception(), instance_of(AuthenticationError), "Authentication error.")


def test_raises_system_error_on_remote_server_error_when_getting_identities(cheddar, platform):
    platform.response_code_queue = [503]
    platform.allowed_bearer_token = "token"
    identities = cheddar.get_identities("...", "token")
    assert_that(identities.exception(), instance_of(requests.exceptions.ConnectionError), "Connection error.")


def test_raises_insufficient_information_error_when_getting_identities(cheddar, platform):
    platform.response_code_queue = [422]
    platform.allowed_bearer_token = "token"
    identities = cheddar.get_identities("...", "token")
    assert_that(identities.exception(), instance_of(InsufficientInformationError), "Insufficient information error.")


def test_returns_empty_array_of_identities(cheddar, platform):
    platform.allowed_bearer_token = "token"
    identities = cheddar.get_identities("reb an mal", "token").result()
    assert_that(identities, empty())


def test_returns_array_of_identities(cheddar, platform):
    platform.allowed_bearer_token = "token"
    platform.identities["reb an mal"] = {
        "id": "0000000115677274",
        "type": "individual",
        "firstName": "Rebecca Ann",
        "lastName": "Maloy",
        "dateOfBirth": "1980",
        "dateOfDeath": "",
        "works": [
            {"title": "Music and meaning in old Hispanic lenten chants psalmi, threni and the Easter vigil canticles"}
        ]
    }

    identities = cheddar.get_identities("reb an mal", "token")
    assert_that(identities.result(), contains(
        has_entries(id="0000000115677274",
                    firstName="Rebecca Ann",
                    lastName="Maloy",
                    dateOfBirth="1980",
                    dateOfDeath="",
                    works=contains(has_entries(
                        title="Music and meaning in old Hispanic lenten chants psalmi, "
                              "threni and the Easter vigil canticles")))))


def test_returns_unauthorized_when_assigning_an_identifier(cheddar):
    identity = cheddar.assign_identifier("Joel Miller", "individual", ["Chevere!", "That is that"], "token")
    assert_that(identity.exception(), instance_of(AuthenticationError), "Authentication error.")


def test_raises_system_error_on_remote_server_error_when_assigning_an_identifier(cheddar, platform):
    platform.response_code_queue = [503]
    platform.allowed_bearer_token = "token"
    identity = cheddar.assign_identifier("Joel Miller", "individual", ["Chevere!", "That is that"], "token")
    assert_that(identity.exception(), instance_of(requests.exceptions.ConnectionError), "Connection error.")


def test_returns_empty_identity(cheddar, platform):
    platform.allowed_bearer_token = "token"
    identity = cheddar.assign_identifier("Joel Miller", "individual", ["Chevere!", "That is that"], "token").result()
    assert_that(identity, empty())


def test_returns_identity_of_newly_assigned_identifier(cheddar, platform):
    platform.allowed_bearer_token = "token"
    platform.identities["Joel Miller"] = {
        "id": "0000000121707484",
        "type": "individual",
        "firstName": "Joel",
        "lastName": "Miller",
        "dateOfBirth": "1969",
        "dateOfDeath": "",
        "works": [
            {"title": "Chevere!"},
            {"title": "That is that"}
        ]
    }

    identity = cheddar.assign_identifier("Joel Miller", "individual", ["Chevere!", "That is that"], "token").result()
    assert_that(identity, has_entries(
        id="0000000121707484",
        firstName="Joel",
        lastName="Miller",
        dateOfBirth="1969",
        dateOfDeath="",
        works=contains(has_entries(title="Chevere!"), has_entries(title="That is that"))))


def test_raises_permission_denied_error_on_402(cheddar, platform):
    platform.response_code_queue = [402]
    platform.allowed_bearer_token = "token"
    identities = cheddar.get_identities("...", "token")
    assert_that(identities.exception(), instance_of(PermissionDeniedError), "Permission denied error.")


def wait_for_completion(future):
    return future.result(2000)

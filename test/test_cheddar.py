import pytest
from hamcrest import assert_that, empty, contains, has_entries, instance_of, equal_to, has_entry

from tgit.cheddar import Cheddar, PermissionDeniedError, AuthenticationError, InsufficientInformationError, \
    PlatformConnectionError

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


def test_authenticates_to_cheddar_and_then_returns_user_details(cheddar, platform):
    platform.token_queue = iter(["token12345"])
    user_details = wait_for_completion(cheddar.authenticate("test@example.com", "passw0rd"))
    assert_that(user_details['email'], "test@example.com", "email")
    assert_that(user_details['token'], "token12345", "token")
    assert_that(user_details['permissions'], contains("isni.lookup", "isni.assign"), "token")


def test_raises_authentication_error_if_credentials_are_invalid(cheddar):
    with pytest.raises(AuthenticationError):
        wait_for_completion(cheddar.authenticate("test@example.com", "wrong_password"))


def test_raises_unauthorized_when_getting_identities_and_not_signed_in(cheddar, platform):
    platform.allowed_bearer_token = "token"
    with pytest.raises(AuthenticationError):
        wait_for_completion(cheddar.get_identities("reb an mal", "..."))


def test_raises_system_error_when_getting_identities(cheddar, platform):
    platform.response_code_queue = [503]
    platform.allowed_bearer_token = "token"
    with pytest.raises(PlatformConnectionError):
        wait_for_completion(cheddar.get_identities("...", "token"))


def test_raises_insufficient_information_error_when_getting_identities(cheddar, platform):
    platform.response_code_queue = [422]
    platform.allowed_bearer_token = "token"
    with pytest.raises(InsufficientInformationError):
        wait_for_completion(cheddar.get_identities("...", "token"))


def test_returns_empty_array_of_identities(cheddar, platform):
    platform.allowed_bearer_token = "token"
    identities = wait_for_completion(cheddar.get_identities("reb an mal", "token"))
    assert_that(identities, has_entry("identities", empty()), "The identities")


def test_returns_array_of_identities(cheddar, platform):
    platform.allowed_bearer_token = "token"
    platform.identities["jo mil"] = [{
        "id": "0000000123456789",
        "type": "individual",
        "firstName": "Joel",
        "lastName": "Miller",
        "dateOfBirth": "1969",
        "dateOfDeath": "",
        "works": [
            {"title": "Chevere!"}
        ]
    }]

    identities = wait_for_completion(cheddar.get_identities("jo mil", "token"))
    assert_that(identities, has_entry("identities",
                                      contains(has_entries(id="0000000123456789",
                                                           firstName="Joel",
                                                           lastName="Miller",
                                                           dateOfBirth="1969",
                                                           dateOfDeath="",
                                                           works=contains(has_entries(title="Chevere!"))))))


def test_returns_hit_count(cheddar, platform):
    platform.allowed_bearer_token = "token"
    platform.identities["reb an mal"] = [{
        "id": "0000000115677274",
        "type": "individual"
    }, {
        "id": "0000000123456789",
        "type": "individual"
    }]

    identities = wait_for_completion(cheddar.get_identities("reb an mal", "token"))
    assert_that(identities["total_count"], equal_to("2"), "The total amount of results")


def test_returns_unauthorized_when_assigning_an_identifier(cheddar):
    identity = cheddar.assign_identifier("Joel Miller", "individual", ["Chevere!", "That is that"], "token")
    assert_that(identity.exception(), instance_of(AuthenticationError), "Authentication error.")


def test_raises_system_error_on_remote_server_error_when_assigning_an_identifier(cheddar, platform):
    platform.response_code_queue = [503]
    platform.allowed_bearer_token = "token"
    identity = cheddar.assign_identifier("Joel Miller", "individual", ["Chevere!", "That is that"], "token")
    assert_that(identity.exception(), instance_of(PlatformConnectionError), "Connection error.")


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
    with pytest.raises(PermissionDeniedError):
        wait_for_completion(cheddar.get_identities("...", "token"))


def wait_for_completion(future):
    return future.result(2)

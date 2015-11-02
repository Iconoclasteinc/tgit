# -*- coding: utf-8 -*-
from hamcrest import assert_that, empty, contains, has_entries
import pytest
import requests

from tgit.authentication_error import AuthenticationError
from tgit.cheddar import Cheddar


@pytest.yield_fixture
def platform():
    from test.util import cheddar

    server_thread = cheddar.start()
    yield cheddar
    cheddar.stop(server_thread)


@pytest.fixture
def cheddar(platform):
    return Cheddar(host=platform.host(), port=platform.port(), secure=False)


def test_authenticates_by_returning_the_token(cheddar, platform):
    platform.token_queue = iter(["token12345"])
    token = cheddar.authenticate("test@example.com", "passw0rd")
    assert_that(token, "token12345", "token")


def test_raises_authentication_error(cheddar):
    with pytest.raises(AuthenticationError):
        cheddar.authenticate("test@example.com", "wrong_password")


def test_returns_unauthorized_when_sending_invalid_token(cheddar, platform):
    platform.allowed_bearer_token = "token"
    with pytest.raises(AuthenticationError):
        cheddar.get_identities("reb an mal", "...")


def test_raises_system_error_on_remote_server_error(cheddar, platform):
    platform.response_code_queue = [503]
    platform.allowed_bearer_token = "token"
    with pytest.raises(requests.exceptions.ConnectionError):
        cheddar.get_identities("...", "token")


def test_returns_empty_array_of_identities(cheddar, platform):
    platform.allowed_bearer_token = "token"
    identities = cheddar.get_identities("reb an mal", "token")
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
    assert_that(identities, contains(
        has_entries(id="0000000115677274",
                    firstName="Rebecca Ann",
                    lastName="Maloy",
                    dateOfBirth="1980",
                    dateOfDeath="",
                    works=contains(has_entries(
                        title="Music and meaning in old Hispanic lenten chants psalmi, "
                              "threni and the Easter vigil canticles")))))

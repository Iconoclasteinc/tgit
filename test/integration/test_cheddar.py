# -*- coding: utf-8 -*-
from hamcrest import assert_that
import pytest

from tgit.authentication_error import AuthenticationError
from tgit.cheddar import Cheddar


@pytest.yield_fixture
def platform():
    from test.util import cheddar

    server_thread = cheddar.start("", 0)
    yield cheddar
    cheddar.stop(server_thread)


@pytest.fixture
def cheddar(platform):
    return Cheddar(host=platform.host(), port=platform.port(), secure=False)


def test_authenticates_by_returning_the_token(cheddar, platform):
    platform.token_queue = iter(["token12345"])
    token = cheddar.authenticate("jonathan", "passw0rd")
    assert_that(token, "token12345", "token")


def test_raises_authentication_error(cheddar):
    with pytest.raises(AuthenticationError):
        cheddar.authenticate("jonathan", "wrong_password")

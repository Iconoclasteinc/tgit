import pytest
from flexmock import flexmock as mock

from tgit.auth import sign_in
from tgit.cheddar import AuthenticationError
from . import exception_with_message

pytestmark = pytest.mark.unit


@pytest.fixture()
def login():
    return mock()


@pytest.fixture()
def authenticator():
    return mock()


def test_authenticates_using_credentials_and_then_reports_success(login, authenticator):
    authenticator.should_receive("authenticate").with_args("email", "password").and_return(
            {"email": "email", "token": "token", "permissions": ["permission"]}).once()
    login.should_receive("authentication_succeeded").with_args("email", "token", ["permission"]).once()

    sign_in(login, authenticator)("email", "password")


def test_reports_authentication_failure_if_credentials_are_rejected(login, authenticator):
    authenticator.should_receive("authenticate").and_raise(AuthenticationError, "invalid credentials")
    login.should_receive("authentication_failed").with_args(exception_with_message("invalid credentials")).once()

    sign_in(login, authenticator)("email", "invalid password")

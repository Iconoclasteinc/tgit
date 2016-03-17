import pytest
from flexmock import flexmock as mock

from test.auth import exception_with_message
from tgit.auth import sign_in
from tgit.cheddar import AuthenticationError
from tgit.promise import Promise

pytestmark = pytest.mark.unit


@pytest.fixture()
def login():
    return mock()


@pytest.fixture()
def authenticator():
    return mock()


def test_authenticates_using_credentials_and_then_reports_progress(login, authenticator):
    auth = Promise()
    authenticator.should_receive("authenticate").with_args("email", "password").and_return(auth).once()

    login.should_receive("authentication_started").ordered().once()
    login.should_receive("authentication_succeeded").with_args({"token": "api-key"}).ordered().once()
    login.should_receive("authentication_failed").never()

    sign_in(login, authenticator)("email", "password")
    auth.complete({"token": "api-key"})


def test_reports_authentication_failure_if_credentials_are_rejected(login, authenticator):
    auth = Promise()
    authenticator.should_receive("authenticate").and_return(auth)

    login.should_receive("authentication_failed").with_args(exception_with_message("invalid credentials")).once()
    login.should_receive("authentication_started")
    login.should_receive("authentication_succeeded").never()

    sign_in(login, authenticator)("email", "invalid password")
    auth.error(AuthenticationError("invalid credentials"))

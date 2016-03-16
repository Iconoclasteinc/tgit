import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, is_, equal_to, contains_inanyorder, not_none

from test.util.builders import make_anonymous_session
from tgit.auth import Login
from . import exception_with_message

pytestmark = pytest.mark.unit


@pytest.fixture()
def listener():
    return mock()


@pytest.fixture()
def session():
    return make_anonymous_session()


def test_logs_user_in_and_reports_success_when_authentication_succeeds(session, listener):
    login = Login(session)

    listener.should_receive("login_successful").with_args("test@example.com").once()
    login.login_successful.subscribe(listener.login_successful)

    login.authentication_succeeded("test@example.com", "api-token", ("isni.lookup", "isni.assign"))

    current_user = session.current_user
    assert_that(current_user, not_none(), "current user")
    assert_that(current_user.email, equal_to("test@example.com"), "user email")
    assert_that(current_user.api_key, equal_to("api-token"), "user key")
    assert_that(current_user.permissions, contains_inanyorder("isni.lookup", "isni.assign"), "user permissions")


def test_reports_failure_but_does_not_log_user_in_when_authentication_fails(session, listener):
    login = Login(session)

    listener.should_receive("login_failed").with_args(exception_with_message("error")).once()
    login.login_failed.subscribe(listener.login_failed)

    login.authentication_failed(Exception("error"))

    assert_that(session.opened, is_(False), "session opened?")

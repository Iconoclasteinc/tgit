import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, is_, has_property, match_equality as matching, equal_to

from testing.builders import make_anonymous_session, make_registered_session

pytestmark = pytest.mark.unit


@pytest.fixture()
def listener():
    return mock()


def test_is_initially_signed_out():
    session = make_anonymous_session()

    assert_that(session.opened, is_(False), "opened?")
    assert_that(session.current_user, has_property("registered", is_(False)), "current user")


def test_knows_user_currently_signed_in():
    session = make_registered_session("previous@example.com", "...")

    session.login_as("current@example.com", "api-key", ())

    assert_that(session.current_user, has_property("email", "current@example.com"))


def test_signals_when_user_signs_in(listener):
    session = make_anonymous_session()

    listener.should_receive("user_signed_in").with_args(
            matching(has_property("email", equal_to("test@example.com")))).once()
    session.user_signed_in.subscribe(listener.user_signed_in)

    session.login_as("test@example.com", "api-key", ())


def test_signals_when_user_signs_out(listener):
    session = make_registered_session("test@example.com", "api-key")

    listener.should_receive("user_signed_out").with_args(
            matching(has_property("email", equal_to("test@example.com")))).once()
    session.user_signed_out.subscribe(listener.user_signed_out)

    session.logout()



import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, match_equality as matching, contains, is_
from hamcrest import has_properties

from testing.builders import make_registered_user
from tgit.auth import load_session_from, User


@pytest.fixture()
def store():
    return mock()


def tests_loads_user_information_from_settings_store_and_logs_user_in(store):
    store.should_receive("load_user").and_return(make_registered_user(email="user@example.com",
                                                                      api_key="token",
                                                                      permissions=("isni.lookup", "isni.assign")))
    session = load_session_from(store)

    assert_that(session.current_user, has_properties(email="user@example.com",
                                                     api_key="token",
                                                     permissions=contains("isni.lookup", "isni.assign")))


def tests_does_not_log_user_if_anonymous(store):
    store.should_receive("load_user").and_return(User.anonymous())

    session = load_session_from(store)

    assert_that(session.opened, is_(False), "session opened?")


def tests_removes_user_credentials_from_settings_store_on_sign_out(store):
    store.should_receive("load_user").and_return(make_registered_user(email="user@example.com",
                                                                      api_key="token",
                                                                      permissions=("isni.lookup", "isni.assign")))
    session = load_session_from(store)

    store.should_receive("remove_user").once()
    session.logout()


def tests_stores_user_credentials_in_settings_store_on_sign_in(store):
    store.should_receive("load_user").and_return(User.anonymous())
    session = load_session_from(store)

    store.should_receive("store_user").with_args(
        matching(has_properties(email="user@example.com",
                                api_key="token",
                                permissions=contains("isni.lookup", "isni.assign")))).once()

    session.login_as("user@example.com", "token", ("isni.lookup", "isni.assign"))

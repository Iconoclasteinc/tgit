# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, is_, equal_to, contains_inanyorder, not_none

from test import exception_with_message
from test.util.builders import make_anonymous_session
from tgit.auth import Login

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
    login.on_success.subscribe(listener.login_successful)

    user_details = dict(email="test@example.com", token="api-token", permissions=("isni.lookup", "isni.assign"))
    login.authentication_succeeded(user_details)

    current_user = session.current_user
    assert_that(current_user, not_none(), "current user")
    assert_that(current_user.email, equal_to("test@example.com"), "user email")
    assert_that(current_user.api_key, equal_to("api-token"), "user key")
    assert_that(current_user.permissions, contains_inanyorder("isni.lookup", "isni.assign"), "user permissions")


def test_reports_failure_but_does_not_log_user_in_when_authentication_fails(session, listener):
    login = Login(session)

    listener.should_receive("login_failed").with_args(exception_with_message("error")).once()
    login.on_failure.subscribe(listener.login_failed)

    login.authentication_failed(Exception("error"))

    assert_that(session.opened, is_(False), "session opened?")


def test_reports_login_in_progress_when_authentication_start(session, listener):
    login = Login(session)

    listener.should_receive("login_in_progress").once()
    login.on_start.subscribe(listener.login_in_progress)

    login.authentication_started()

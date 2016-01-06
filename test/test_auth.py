# -*- coding: utf-8 -*-

from hamcrest import assert_that, is_, has_property, equal_to

from test.util.builders import make_anonymous_user, make_registered_user, make_anonymous_session, \
    make_registered_session
from tgit.auth import Permission


class SessionChangedSubscriber:
    user = None

    def user_changed(self, user):
        self.user = user


def test_user_has_permission_to_lookup_isni_when_registered():
    anonymous = make_anonymous_user()
    assert_that(anonymous.has_permission(Permission.lookup_isni), is_(False), "grant to anonymous")

    registered = make_registered_user()
    assert_that(registered.has_permission(Permission.lookup_isni), is_(True), "grant to registered")


def test_user_knows_its_email():
    anonymous = make_anonymous_user()
    assert_that(anonymous.email, is_(None), "anonymous email")

    registered = make_registered_user(email="test@example.com")
    assert_that(registered.email, is_("test@example.com"), "test email")


def test_user_knows_its_api_key():
    anonymous = make_anonymous_user()
    assert_that(anonymous.api_key, is_(None), "anonymous api key")

    registered = make_registered_user(token="0123456789")
    assert_that(registered.api_key, is_("0123456789"), "test api key")


def test_user_knows_its_permissions():
    anonymous = make_anonymous_user()
    assert_that(anonymous.has_permission(Permission.lookup_isni), is_(False), "anonymous permissions")

    registered = make_registered_user(permissions=["lookup_isni"])
    assert_that(registered.has_permission(Permission.lookup_isni), is_(True), "test permissions")
    assert_that(registered.has_permission(Permission.assign_isni), is_(False), "test permissions")


def test_session_signals_when_user_signs_in():
    session = make_anonymous_session()
    assert_that(session.current_user, has_property("registered", is_(False)))

    subscriber = SessionChangedSubscriber()
    session.user_signed_in.subscribe(subscriber.user_changed)

    session.login_as("test@example.com", "api-key", [])
    assert_that(subscriber.user, has_property("email", equal_to("test@example.com")))


def test_session_signals_when_user_signs_out():
    session = make_registered_session("test@example.com", "api-key")
    assert_that(session.current_user, has_property("registered", is_(True)))

    subscriber = SessionChangedSubscriber()
    session.user_signed_out.subscribe(subscriber.user_changed)

    session.logout()
    assert_that(subscriber.user, has_property("email", equal_to("test@example.com")))

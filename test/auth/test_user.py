import pytest
from hamcrest import assert_that, is_

from test.util.builders import make_anonymous_user, make_registered_user
from tgit.auth import Permission

pytestmark = pytest.mark.unit


def test_anonymous_user_cannot_lookup_isni():
    anonymous = make_anonymous_user()
    assert_that(anonymous.has_permission(Permission.lookup_isni), is_(False), "grant to anonymous")


def test_anonymous_user_has_no_email():
    anonymous = make_anonymous_user()
    assert_that(anonymous.email, is_(None), "anonymous email")


def test_anonymous_user_has_no_api_key():
    anonymous = make_anonymous_user()
    assert_that(anonymous.api_key, is_(None), "anonymous api key")


def test_registered_user_has_permission_to_lookup_isni():
    registered = make_registered_user()
    assert_that(registered.has_permission(Permission.lookup_isni), is_(True), "grant to registered")


def test_registered_user_knows_its_email():
    registered = make_registered_user(email="test@example.com")
    assert_that(registered.email, is_("test@example.com"), "registered email")


def test_registered_user_knows_its_api_key():
    registered = make_registered_user(token="0123456789")
    assert_that(registered.api_key, is_("0123456789"), "registered api key")


def test_registered_user_knows_its_permissions():
    registered = make_registered_user(permissions=[Permission.lookup_isni.value])
    assert_that(registered.has_permission(Permission.lookup_isni), is_(True), "isni lookup?")
    assert_that(registered.has_permission(Permission.assign_isni), is_(False), "isni assign?")

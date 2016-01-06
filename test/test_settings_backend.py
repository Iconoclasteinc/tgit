# -*- coding: utf-8 -*-

import sip

from PyQt5.QtCore import QLocale
from PyQt5.QtWidgets import QApplication
from hamcrest import assert_that, has_properties, equal_to
import pytest

from test.drivers.application_settings_driver import ApplicationSettingsDriver
from tgit.tagger import SettingsBackend


@pytest.yield_fixture()
def qt():
    app = QApplication([])
    yield app
    app.quit()
    # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
    # Never ever remove this!!
    sip.delete(app)


@pytest.fixture
def settings_file(tmpdir):
    return tmpdir.join("settings.ini").strpath


@pytest.fixture
def settings_backend(qt, settings_file):
    return SettingsBackend(settings_file)


@pytest.fixture
def settings_driver(settings_file):
    return ApplicationSettingsDriver(settings_file)


def tests_loads_anonymous_user_if_user_credentials_missing_from_settings_file(settings_backend, settings_driver):
    session = settings_backend.load_session()

    assert_that(session.current_user, has_properties(email=None, api_key=None))


def tests_loads_user_information_from_settings_file(settings_backend, settings_driver):
    settings_driver["user.email"] = "user@example.com"
    settings_driver["user.api_key"] = "token"
    settings_driver["user.permissions"] = "permission1;permission2"

    session = settings_backend.load_session()

    assert_that(session.current_user, has_properties(email="user@example.com",
                                                     api_key="token",
                                                     permissions=["permission1", "permission2"]))


def tests_removes_user_credentials_from_settings_file_on_sign_out(settings_backend, settings_driver):
    settings_driver["user.email"] = "user@example.com"
    settings_driver["user.api_key"] = "token"
    settings_driver["user.permissions"] = "permission1;permission2"

    session = settings_backend.load_session()
    session.logout()

    settings_driver.has_no("user.email")
    settings_driver.has_no("user.api_key")
    settings_driver.has_no("user.permissions")


def tests_stores_user_credentials_in_settings_file_on_sign_in(settings_backend, settings_driver):
    session = settings_backend.load_session()
    session.login_as("user@example.com", "token", ["permission1", "permission2"])

    settings_driver.has_stored("user.email", "user@example.com")
    settings_driver.has_stored("user.api_key", "token")
    settings_driver.has_stored("user.permissions", "permission1;permission2")


def tests_defaults_to_english_locale(settings_backend, settings_driver):
    user_preferences = settings_backend.load_user_preferences()

    assert_that(user_preferences.locale, equal_to(QLocale("en")))


def tests_loads_user_preferences_from_settings_file(settings_backend, settings_driver):
    settings_driver["preferences.locale"] = "fr_CA"
    preferences = settings_backend.load_user_preferences()

    assert_that(preferences.locale, equal_to(QLocale("fr_CA")))


def tests_stores_preferences_in_settings_file_on_change(settings_backend, settings_driver):
    preferences = settings_backend.load_user_preferences()
    preferences.locale = QLocale("fr_FR")

    settings_driver.has_stored("preferences.locale", "fr_FR")

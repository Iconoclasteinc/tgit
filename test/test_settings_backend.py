# -*- coding: utf-8 -*-

from PyQt5.QtCore import QSettings
from hamcrest import assert_that, has_properties
import pytest

from test.drivers.application_settings_driver import ApplicationSettingsDriver
from tgit.tagger import SettingsBackend


@pytest.fixture
def settings_file(tmpdir):
    return tmpdir.join("settings.ini").strpath


@pytest.fixture
def settings_backend(settings_file):
    return SettingsBackend(QSettings(settings_file, QSettings.IniFormat))


@pytest.fixture
def settings_driver(settings_file):
    return ApplicationSettingsDriver(settings_file)


def tests_loads_anonymous_user_if_user_credentials_missing_from_settings_file(settings_backend, settings_driver):
    session = settings_backend.load_session()

    assert_that(session.current_user, has_properties(email=None, api_key=None))


def tests_loads_user_information_from_settings_file(settings_backend, settings_driver):
    settings_driver["user.email"] = "user@example.com"
    settings_driver["user.api_key"] = "token"

    session = settings_backend.load_session()

    assert_that(session.current_user, has_properties(email="user@example.com", api_key="token"))


def tests_removes_user_credentials_from_settings_file_on_sign_out(settings_backend, settings_driver):
    settings_driver["user.email"] = "user@example.com"
    settings_driver["user.api_key"] = "token"

    session = settings_backend.load_session()
    session.logout()

    settings_driver.has_no("user.email")
    settings_driver.has_no("user.api_key")


def tests_stores_user_credentials_in_settings_file_on_sign_in(settings_backend, settings_driver):
    session = settings_backend.load_session()
    session.login_as("user@example.com", "token")

    settings_driver.has_stored("user.email", "user@example.com")
    settings_driver.has_stored("user.api_key", "token")

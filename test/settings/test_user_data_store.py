# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, empty, has_properties, contains

from test.drivers.application_settings_driver import ApplicationSettingsDriver
from tgit.auth import User
from tgit.settings import UserDataStore

pytestmark = pytest.mark.unit


@pytest.yield_fixture
def store(settings):
    backend = UserDataStore(settings)
    yield backend
    backend.close()


@pytest.fixture
def driver(settings):
    return ApplicationSettingsDriver(settings)


def test_returns_anonymous_user_if_user_data_missing_from_settings_file(store):
    user = store.load_user()

    assert_that(user, has_properties(email=None, api_key=None, permissions=empty()))


def tests_loads_user_data_from_settings_file_user_group(store, driver):
    driver["user/email"] = "user@example.com"
    driver["user/api_key"] = "token"
    driver["user/permissions/size"] = 2
    driver["user/permissions/1/value"] = "isni.lookup"
    driver["user/permissions/2/value"] = "isni.assign"

    user = store.load_user()

    assert_that(user, has_properties(email="user@example.com",
                                     api_key="token",
                                     permissions=contains("isni.lookup", "isni.assign")))


def tests_stores_user_data_under_user_group_in_settings_file(store, driver):
    store.store_user(User(email="user@example.com", api_key="token", permissions=("isni.lookup", "isni.assign")))

    driver.has_stored("user/email", "user@example.com")
    driver.has_stored("user/api_key", "token")
    driver.has_stored("user/permissions/size", 2)
    driver.has_stored("user/permissions/1/value", "isni.lookup")
    driver.has_stored("user/permissions/2/value", "isni.assign")


def tests_deletes_user_data_from_settings_file_on_remove(store, driver):
    driver["user/email"] = "user@example.com"
    driver["user/api_key"] = "token"
    driver["user/permissions/size"] = 2
    driver["user/permissions/1/value"] = "isni.lookup"
    driver["user/permissions/2/value"] = "isni.assign"

    store.remove_user()

    driver.has_no("user/email")
    driver.has_no("user/api_key")
    driver.has_no("user/permissions/size")
    driver.has_no("user/permissions/1/value")
    driver.has_no("user/permissions/2/value")

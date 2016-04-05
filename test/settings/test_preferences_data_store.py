# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, has_properties
from test.drivers.application_settings_driver import ApplicationSettingsDriver

from testing.builders import make_preferences
from testing.matchers import preferences_with
from tgit.settings import PreferencesDataStore

pytestmark = pytest.mark.unit


@pytest.yield_fixture
def store(settings):
    backend = PreferencesDataStore(settings)
    yield backend
    backend.close()


@pytest.fixture
def driver(settings):
    return ApplicationSettingsDriver(settings)


def test_returns_default_preferences_if_data_missing_from_settings_file(store):
    preferences = store.load_preferences()

    assert_that(preferences, has_properties(locale="en"))


def tests_loads_data_from_settings_file_preferences_group(store, driver):
    driver["preferences/locale"] = "fr"

    preferences = store.load_preferences()

    assert_that(preferences, has_properties(locale="fr"))


def tests_stores_data_under_preferences_group_in_settings_file(store, driver):
    preferences = make_preferences(locale="fr")

    store.store_preferences(preferences)

    driver.has_stored("preferences/locale", "fr")


def tests_deletes_preferences_data_from_settings_file_on_remove(store, driver):
    driver["preferences/locale"] = "fr"

    store.remove_preferences()

    driver.has_no("preferences/locale")


def tests_round_trips_preferences_to_settings_file(store):
    store.store_preferences(make_preferences(locale="fr"))

    persisted_preferences = store.load_preferences()

    assert_that(persisted_preferences, preferences_with(locale="fr"))


def tests_overwrites_previous_preferences_data_on_store(store):
    store.store_preferences(make_preferences(locale="fr"))
    store.store_preferences(make_preferences(locale="en"))

    overwritten_preferences = store.load_preferences()

    assert_that(overwritten_preferences, preferences_with(locale="en"), "overwritten preferences")

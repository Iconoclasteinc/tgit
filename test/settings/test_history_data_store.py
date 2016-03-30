# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, empty, contains

from test.drivers.application_settings_driver import ApplicationSettingsDriver
from test.util.builders import make_project_history, make_snapshot
from testing.matchers import snapshot_with
from tgit.settings import HistoryDataStore

pytestmark = pytest.mark.unit


@pytest.yield_fixture
def store(settings):
    backend = HistoryDataStore(settings)
    yield backend
    backend.close()


@pytest.fixture
def driver(settings):
    return ApplicationSettingsDriver(settings)


def test_returns_no_history_if_project_history_data_missing_from_settings_file(store):
    data = store.load_history()

    assert_that(data, empty())


def tests_loads_history_data_from_settings_file_history_group(store, driver):
    driver["history/size"] = 3
    driver["history/1/name"] = "Last"
    driver["history/1/path"] = "last.tgit"
    driver["history/2/name"] = "Previous"
    driver["history/2/path"] = "previous.tgit"
    driver["history/3/name"] = "Oldest"
    driver["history/3/path"] = "oldest.tgit"

    history = store.load_history()

    assert_that(history, contains(snapshot_with(name="Last", path="last.tgit"),
                                  snapshot_with(name="Previous", path="previous.tgit"),
                                  snapshot_with(name="Oldest", path="oldest.tgit")))


def tests_stores_history_data_under_history_group_in_settings_file(store, driver):
    store.store_history(make_project_history(make_snapshot(name="Last", path="last.tgit"),
                                             make_snapshot(name="Previous", path="previous.tgit"),
                                             make_snapshot(name="Oldest", path="oldest.tgit")))

    driver.has_stored("history/size", 3)
    driver.has_stored("history/1/name", "Last")
    driver.has_stored("history/1/path", "last.tgit")
    driver.has_stored("history/2/name", "Previous")
    driver.has_stored("history/2/path", "previous.tgit")
    driver.has_stored("history/3/name", "Oldest")
    driver.has_stored("history/3/path", "oldest.tgit")


def tests_deletes_history_data_from_settings_file_on_remove(store, driver):
    driver["history/size"] = 3
    driver["history/1/path"] = "last.tgit"
    driver["history/2/path"] = "previous.tgit"
    driver["history/3/path"] = "oldest.tgit"

    store.remove_history()

    driver.has_no("history")
    driver.has_no("history/size")
    driver.has_no("history/1/path")
    driver.has_no("history/2/path")
    driver.has_no("history/3/path")

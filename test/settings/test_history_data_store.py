# -*- coding: utf-8 -*-
import os

import pytest
from hamcrest import assert_that, empty, contains

from test.drivers.application_settings_driver import ApplicationSettingsDriver
from test.util import resources
from test.util.builders import make_project_history, make_snapshot
from testing.matchers import snapshot_with, image_with
from tgit import fs
from tgit.metadata import Image
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
    driver["history/1/type"] = "flac"
    driver["history/2/name"] = "Previous"
    driver["history/2/path"] = "previous.tgit"
    driver["history/2/type"] = "mp3"
    driver["history/3/name"] = "Oldest"
    driver["history/3/path"] = "oldest.tgit"
    driver["history/3/type"] = "mp3"

    history = store.load_history()

    assert_that(history, contains(snapshot_with(name="Last", type_="flac", path="last.tgit"),
                                  snapshot_with(name="Previous", type_="mp3", path="previous.tgit"),
                                  snapshot_with(name="Oldest", type_="mp3", path="oldest.tgit")))


def tests_stores_history_data_under_history_group_in_settings_file(store, driver):
    store.store_history(make_project_history(make_snapshot(name="Last", type_="flac", path="last.tgit"),
                                             make_snapshot(name="Previous", type_="mp3", path="previous.tgit"),
                                             make_snapshot(name="Oldest", type_="mp3", path="oldest.tgit")))

    driver.has_stored("history/size", 3)
    driver.has_stored("history/1/name", "Last")
    driver.has_stored("history/1/path", "last.tgit")
    driver.has_stored("history/1/type", "flac")
    driver.has_stored("history/2/name", "Previous")
    driver.has_stored("history/2/path", "previous.tgit")
    driver.has_stored("history/2/type", "mp3")
    driver.has_stored("history/3/name", "Oldest")
    driver.has_stored("history/3/path", "oldest.tgit")
    driver.has_stored("history/3/type", "mp3")


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


def test_round_trips_history_including_cover_thumbnail_to_settings_file(store):
    cover_art = image_file(resources.path("front-cover.jpg"))
    store.store_history(make_project_history(make_snapshot(name="Last", path="last.tgit", cover_art=cover_art),
                                             make_snapshot(name="Previous", path="previous.tgit")))

    persisted_history = store.load_history()

    assert_that(persisted_history, contains(
        snapshot_with(name="Last", path="last.tgit", cover_art=image_with(mime=cover_art.mime, data=cover_art.data,
                                                                          desc=cover_art.desc, type_=cover_art.type)),
        snapshot_with(name="Previous", path="previous.tgit")), "persisted history")


def image_file(path):
    return Image(mime=fs.guess_mime_type(path), data=fs.read(path), desc=os.path.basename(path))

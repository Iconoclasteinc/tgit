# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog
from hamcrest import assert_that, same_instance
import pytest

from cute.matchers import named
from cute.widgets import window, FileDialogDriver
from test.drivers.load_album_dialog_driver import LoadAlbumDialogDriver
from test.drivers.select_album_destination_dialog_driver import SelectAlbumDestinationDialogDriver
from test.drivers import TrackSelectionDialogDriver, ReferenceTrackSelectionDialogDriver
from test.util import builders as make
from tgit import album_director
from tgit.ui import Dialogs


@pytest.fixture()
def dialogs(main_window):
    dialogs = Dialogs(album_director, native=True)
    dialogs.parent = main_window
    return dialogs


@pytest.yield_fixture()
def track_selection_dialog_driver(prober, automaton):
    driver = FileDialogDriver(window(QFileDialog, named("track-selection-dialog")), prober, automaton)
    yield driver
    driver.close()


@pytest.yield_fixture()
def reference_track_selection_dialog_driver(prober, automaton):
    driver = FileDialogDriver(window(QFileDialog, named("import_album_from_track_dialog")), prober, automaton)
    yield driver
    driver.close()


@pytest.yield_fixture()
def select_album_destination_dialog_driver(prober, automaton):
    driver = FileDialogDriver(window(QFileDialog, named("select_album_destination_dialog")), prober, automaton)
    yield driver
    driver.close()


@pytest.yield_fixture()
def select_album_to_load_dialog_driver(prober, automaton):
    driver = FileDialogDriver(window(QFileDialog, named("load_album_dialog")), prober, automaton)
    yield driver
    driver.close()


def test_creates_a_single_reference_track_selection_dialog(dialogs, reference_track_selection_dialog_driver):
    dialogs.select_reference_track()(lambda: None)
    reference_track_selection_dialog_driver.is_showing_on_screen()

    dialogs.select_reference_track()(lambda: None)
    reference_track_selection_dialog_driver.is_showing_on_screen()


def test_creates_a_single_album_destination_selection_dialog(dialogs, select_album_destination_dialog_driver):
    dialogs.select_album_destination()(lambda: None)
    select_album_destination_dialog_driver.is_showing_on_screen()

    dialogs.select_album_destination()(lambda: None)
    select_album_destination_dialog_driver.is_showing_on_screen()


def test_creates_a_single_album_to_load_selection_dialog(dialogs, select_album_to_load_dialog_driver):
    dialogs.select_album_to_load()(lambda: None)
    select_album_to_load_dialog_driver.is_showing_on_screen()

    dialogs.select_album_to_load()(lambda: None)
    select_album_to_load_dialog_driver.is_showing_on_screen()


def test_creates_a_single_track_selection_dialog_for_a_given_album(dialogs, track_selection_dialog_driver):
    album = make.album()
    dialogs.add_tracks(album)()
    track_selection_dialog_driver.is_showing_on_screen()

    dialogs.add_tracks(album)()
    track_selection_dialog_driver.is_showing_on_screen()


def test_creates_a_single_picture_selection_dialog_for_a_given_album(dialogs):
    album = make.album()
    picture_dialog = dialogs.select_cover(album)

    assert_that(dialogs.select_cover(album), same_instance(picture_dialog))


def test_creates_a_new_picture_selection_dialog_for_each_album(dialogs):
    album = make.album()
    picture_dialog = dialogs.select_cover(album)
    dialogs.clear()

    assert_that(dialogs.select_cover(make.album()), not same_instance(picture_dialog))


def test_creates_a_new_track_selection_dialog_for_each_album(dialogs):
    album = make.album()
    track_dialog = dialogs.add_tracks(album)
    dialogs.clear()

    assert_that(dialogs.add_tracks(make.album()), not same_instance(track_dialog))


def test_creates_a_single_export_dialog_for_a_given_album(dialogs):
    album = make.album()
    export_dialog = dialogs.export(album)

    assert_that(dialogs.export(album), same_instance(export_dialog))


def test_creates_a_new_export_dialog_for_each_album(dialogs):
    album = make.album()
    export_dialog = dialogs.export(album)
    dialogs.clear()

    assert_that(dialogs.export(make.album()), not same_instance(export_dialog))

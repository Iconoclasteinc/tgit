# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.widgets import window, FileDialogDriver
from tgit import album_director
from tgit.album import Album
from tgit.ui import Dialogs


ignore = lambda *_, **__: None


@pytest.fixture()
def dialogs(qt):
    return Dialogs(native=False)


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


@pytest.yield_fixture()
def export_dialog_driver(prober, automaton):
    driver = FileDialogDriver(window(QFileDialog, named("export-as-dialog")), prober, automaton)
    yield driver
    driver.close()


@pytest.yield_fixture()
def picture_selection_dialog_driver(prober, automaton):
    driver = FileDialogDriver(window(QFileDialog, named("picture-selection-dialog")), prober, automaton)
    yield driver
    driver.close()


def test_creates_a_single_album_destination_selection_dialog(dialogs, select_album_destination_dialog_driver):
    dialogs.select_album_destination(ignore)
    select_album_destination_dialog_driver.is_showing_on_screen()
    select_album_destination_dialog_driver.reject()

    dialogs.select_album_destination(ignore)
    select_album_destination_dialog_driver.is_showing_on_screen()
    select_album_destination_dialog_driver.reject()


def test_creates_a_single_album_to_load_selection_dialog(dialogs, select_album_to_load_dialog_driver):
    dialogs.select_album_to_load(ignore)
    select_album_to_load_dialog_driver.is_showing_on_screen()
    select_album_to_load_dialog_driver.reject()

    dialogs.select_album_to_load(ignore)
    select_album_to_load_dialog_driver.is_showing_on_screen()
    select_album_to_load_dialog_driver.reject()


def test_creates_a_single_track_selection_dialog(dialogs, track_selection_dialog_driver):
    dialogs.select_tracks(Album.Type.MP3, ignore)
    track_selection_dialog_driver.is_showing_on_screen()
    track_selection_dialog_driver.reject()

    dialogs.select_tracks(Album.Type.MP3, ignore)
    track_selection_dialog_driver.is_showing_on_screen()
    track_selection_dialog_driver.reject()


def test_creates_a_single_picture_selection_dialog_for_a_given_album(dialogs, picture_selection_dialog_driver):
    dialogs.select_cover(ignore)
    picture_selection_dialog_driver.is_showing_on_screen()
    picture_selection_dialog_driver.reject()

    dialogs.select_cover(ignore)
    picture_selection_dialog_driver.is_showing_on_screen()
    picture_selection_dialog_driver.reject()


def test_creates_a_single_export_dialog_for_a_given_album(dialogs, export_dialog_driver):
    dialogs.export(ignore)
    export_dialog_driver.is_showing_on_screen()
    export_dialog_driver.reject()

    dialogs.export(ignore)
    export_dialog_driver.is_showing_on_screen()
    export_dialog_driver.reject()

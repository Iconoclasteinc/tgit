import os

import pytest
from PyQt5.QtWidgets import QFileDialog
from hamcrest import contains_string

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from testing import resources
from testing.drivers import SaveAsDialogDriver
from tgit import platforms
from tgit.ui.dialogs.save_as_dialog import SaveAsDialog, make_save_as_excel_dialog, make_save_as_csv_dialog

pytestmark = pytest.mark.ui


def show_dialog(*mime_type_filters, on_select=ignore, default_file_name="", title="Save As", default_suffix="csv"):
    dialog = SaveAsDialog(default_file_name=default_file_name,
                          title=title,
                          default_suffix=default_suffix,
                          mime_type_filters=list(mime_type_filters),
                          parent=None,
                          native=False,
                          delete_on_close=False)
    dialog.on_select(on_select)
    show_(dialog)
    return dialog


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = SaveAsDialogDriver(window(QFileDialog, named("save_as_dialog")), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


@pytest.mark.skipif(platforms.windows, reason="not supported on Windows")
@pytest.mark.skipif(platforms.linux, reason="not supported on Linux")
def test_only_accepts_files_from_mime_type_filters(driver):
    _ = show_dialog("text/csv")
    driver.rejects_selection_of(resources.path("base.mp3"))


def test_signals_save_as_destination(tmpdir, driver):
    destination = tmpdir.join("album.csv").strpath
    save_as_signal = ValueMatcherProbe("save as", destination)

    _ = show_dialog(on_select=lambda dest: save_as_signal.received(os.path.abspath(dest)))

    driver.save_as(destination)
    driver.check(save_as_signal)


def test_adds_extension_when_none_was_specified(tmpdir, driver):
    destination = tmpdir.join("album").strpath
    save_as_signal = ValueMatcherProbe("save as", destination + ".csv")

    _ = show_dialog(on_select=lambda dest: save_as_signal.received(os.path.abspath(dest)), default_suffix="csv")

    driver.save_as(destination)
    driver.check(save_as_signal)


@pytest.mark.skipif(platforms.mac, reason="not supported on OSX")
def test_shows_title(driver):
    _ = show_dialog(title="New Title")
    driver.has_window_title("New Title")


def test_shows_default_file_name(driver):
    _ = show_dialog(default_file_name="album")
    driver.has_filename("album")


def test_shows_mime_type_filters(driver):
    _ = show_dialog("text/csv")
    driver.filter_files_of_type(contains_string("*.csv"))


def test_make_save_as_excel_dialog(driver):
    dialog = make_save_as_excel_dialog(on_select=ignore, default_file_name="album", parent=None, native=False)
    show_(dialog)

    driver.has_window_title("Save As")
    driver.has_filename("album")
    driver.filter_files_of_type(contains_string("*.xlsx"))


def test_make_save_as_csv_dialog(driver):
    dialog = make_save_as_csv_dialog(on_select=ignore, default_file_name="album", parent=None, native=False)
    show_(dialog)

    driver.has_window_title("Export As")
    driver.has_filename("album")
    driver.filter_files_of_type(contains_string("*.csv"))

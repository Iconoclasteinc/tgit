# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.export_as_dialog_driver import ExportAsDialogDriver
from test.util import resources
from tgit.ui.export_as_dialog import ExportAsDialog


def show_dialog(on_select=lambda *_: None, default_file_name=""):
    dialog = ExportAsDialog(default_file_name=default_file_name, native=False)
    dialog.select(on_select)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = ExportAsDialogDriver(window(QFileDialog, named("export-as-dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_only_accepts_csv_files(driver):
    _ = show_dialog()
    driver.rejects_selection_of(resources.path("base.mp3"))


def test_signals_export_destination(tmpdir, driver):
    destination = tmpdir.join("album.csv").strpath
    export_as_signal = ValueMatcherProbe("export as", destination)

    _ = show_dialog(lambda dest: export_as_signal.received(os.path.abspath(dest)))

    driver.export_as(destination)
    driver.check(export_as_signal)


def test_adds_extension_when_none_was_specified(tmpdir, driver):
    destination = tmpdir.join("album").strpath
    export_as_signal = ValueMatcherProbe("export as", destination + ".csv")

    _ = show_dialog(lambda dest: export_as_signal.received(os.path.abspath(dest)))

    driver.export_as(destination)
    driver.check(export_as_signal)


@pytest.mark.skipif(sys.platform.startswith("darwin"), reason="not supported on OSX")
def test_shows_export_as_title(driver):
    _ = show_dialog()
    driver.has_window_title("Export As")


def test_shows_default_file_name(driver):
    _ = show_dialog(default_file_name="album")
    driver.has_filename("album")

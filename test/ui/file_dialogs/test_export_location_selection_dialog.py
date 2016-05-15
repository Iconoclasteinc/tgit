# -*- coding: utf-8 -*-
import os

import pytest
from PyQt5.QtWidgets import QFileDialog

from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from testing.builders import make_album
from testing.drivers import FileDialogDriver
from tgit.export import ExportLocationSelection
from tgit.ui.dialogs.file_dialogs import make_export_location_selection_dialog
from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.ui


def show_dialog(model, on_select=ignore):
    dialog = make_export_location_selection_dialog(export_location_selection=model, on_file_selected=on_select,
                                                   native=False)
    show_(dialog)
    return dialog


@pytest.fixture()
def export_location_selection():
    return ExportLocationSelection(make_album(release_name="Honeycomb"), UserPreferences())


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = FileDialogDriver(window(QFileDialog), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


def test_signals_when_location_selected(driver, export_location_selection, tmpdir):
    destination = tmpdir.strpath

    signal = ValueMatcherProbe("file selected", os.path.join(destination, "Honeycomb.xml"))
    _ = show_dialog(export_location_selection, lambda dest: signal.received(os.path.abspath(dest)))

    driver.navigate_to_dir(destination)
    driver.accept()
    driver.check(signal)

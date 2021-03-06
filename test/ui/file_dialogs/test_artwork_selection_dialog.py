# -*- coding: utf-8 -*-
import os

import pytest
from PyQt5.QtWidgets import QFileDialog

from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from testing import resources
from testing.builders import make_studio
from testing.drivers import FileDialogDriver
from tgit.artwork import ArtworkSelection
from tgit.ui.dialogs.file_dialogs import make_artwork_selection_dialog
from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.ui


def show_dialog(model, on_select=ignore):
    dialog = make_artwork_selection_dialog(artwork_selection=model, on_file_selected=on_select, native=False)
    show_(dialog)
    return dialog


@pytest.fixture()
def artwork_selection():
    return ArtworkSelection(make_studio(), UserPreferences())


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = FileDialogDriver(window(QFileDialog), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


def test_signals_when_artwork_selected(driver, artwork_selection):
    signal = ValueMatcherProbe("file selected", resources.path("front-cover.jpg"))
    _ = show_dialog(artwork_selection, lambda destination: signal.received(os.path.abspath(destination)))

    driver.select(resources.path("front-cover.jpg"))
    driver.check(signal)

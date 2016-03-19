# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.file_dialog_driver import FileDialogDriver
from test.integration.ui import ignore
from test.util import resources
from test.util.builders import make_portfolio
from tgit.artwork import ArtworkSelection
from tgit.ui import locations
from tgit.ui.dialogs.file_dialog import open_artwork_selection_dialog

pytestmark = pytest.mark.ui


def show_dialog(model, on_select=ignore):
    dialog = open_artwork_selection_dialog(picture_selection=model, on_file_selected=on_select, native=False)
    dialog.open()
    return dialog


@pytest.fixture()
def artwork_selection():
    return ArtworkSelection(make_portfolio(), locations.Pictures)


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = FileDialogDriver(window(QFileDialog), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_artwork_selected(driver, artwork_selection):
    signal = ValueMatcherProbe("file selected", resources.path("front-cover.jpg"))
    _ = show_dialog(artwork_selection, lambda destination: signal.received(os.path.abspath(destination)))

    driver.select(resources.path("front-cover.jpg"))
    driver.check(signal)

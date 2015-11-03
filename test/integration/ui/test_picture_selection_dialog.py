# -*- coding: utf-8 -*-
import os

import sys

from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import PictureSelectionDialogDriver
from test.util import resources
from tgit.platforms import windows
from tgit.ui.picture_selection_dialog import PictureSelectionDialog


def show_dialog(on_select=lambda: None):
    dialog = PictureSelectionDialog(native=False)
    dialog.select(on_select)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    driver = PictureSelectionDialogDriver(window(QFileDialog, named("picture-selection-dialog")), prober, automaton)
    yield driver
    driver.close()


def test_signals_when_picture_selected(driver):
    signal = ValueMatcherProbe("picture selected", resources.path("front-cover.jpg"))
    _ = show_dialog(lambda destination: signal.received(os.path.abspath(destination)))

    driver.select_picture(resources.path("front-cover.jpg"))
    driver.check(signal)


@pytest.mark.skipif(windows, reason="not supported on Windows")
def test_only_accepts_picture_files(driver):
    _ = show_dialog()
    driver.rejects_selection_of(resources.path("base.mp3"))


def test_initially_starts_in_user_pictures_folder(driver):
    _ = show_dialog()
    driver.has_current_directory(ends_with("Pictures"))

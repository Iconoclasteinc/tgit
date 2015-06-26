# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import PictureSelectionDialogDriver
from test.util import resources
from tgit.ui.picture_selection_dialog import PictureSelectionDialog


@pytest.fixture()
def dialog(qt):
    return PictureSelectionDialog(native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    driver = PictureSelectionDialogDriver(window(QFileDialog, named('picture-selection-dialog')), prober, automaton)
    yield driver
    driver.close()


def test_signals_when_picture_selected(dialog, driver):
    picture_selected_signal = ValueMatcherProbe('picture selected', resources.path('front-cover.jpg'))
    dialog.picture_selected.connect(picture_selected_signal.received)
    dialog.open()

    driver.select_picture(resources.path('front-cover.jpg'))
    driver.check(picture_selected_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_only_accepts_picture_files(dialog, driver):
    dialog.open()

    driver.rejects_selection_of(resources.path('base.mp3'))


def test_initially_starts_in_user_pictures_folder(driver):
    driver.has_current_directory(ends_with("Pictures"))

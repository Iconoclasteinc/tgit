# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog
import pytest

from cute.matchers import named
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from cute.widgets import window
from test.drivers.picture_selection_dialog_driver import PictureSelectionDialogDriver
from test.integration.ui import show_widget
from test.util import resources
from tgit.ui.picture_selection_dialog import PictureSelectionDialog


@pytest.yield_fixture()
def picture_dialog(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    yield PictureSelectionDialog(main_window, native=False)
    main_window.close()


@pytest.yield_fixture()
def driver(picture_dialog):
    driver = PictureSelectionDialogDriver(window(QFileDialog, named('picture-selection-dialog')),
                                          EventProcessingProber(), Robot())
    yield driver
    driver.close()


def test_signals_when_picture_selected(picture_dialog, driver):
    picture_selected_signal = ValueMatcherProbe('picture selected', resources.path('front-cover.jpg'))
    picture_dialog.picture_selected.connect(picture_selected_signal.received)
    picture_dialog.open()

    driver.select_picture(resources.path('front-cover.jpg'))
    driver.check(picture_selected_signal)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="not supported on Windows")
def test_only_accepts_picture_files(picture_dialog, driver):
    picture_dialog.open()

    driver.rejects_selection_of(resources.path('base.mp3'))
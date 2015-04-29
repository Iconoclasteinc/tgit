# -*- coding: utf-8 -*-

from hamcrest import equal_to

from PyQt5.QtWidgets import QMainWindow, QFileDialog
import pytest

from cute.matchers import named
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from cute.widgets import window
from test.drivers.export_as_dialog_driver import ExportAsDialogDriver
from test.integration.ui import show_widget
from tgit.ui.export_as_dialog import ExportAsDialog


@pytest.yield_fixture()
def export_dialog(qt):
    main_window = QMainWindow()
    show_widget(main_window)
    yield ExportAsDialog(main_window, native=False)
    main_window.close()


@pytest.yield_fixture()
def driver(export_dialog):
    driver = ExportAsDialogDriver(window(QFileDialog, named('export-as-dialog')), EventProcessingProber(), Robot())
    yield driver
    driver.close()


def test_signals_export_as_destination(tmpdir, export_dialog, driver):
    destination = tmpdir.join("album.csv").strpath
    export_as_signal = ValueMatcherProbe('export as', equal_to(destination))

    export_dialog.export_as.connect(export_as_signal.received)
    export_dialog.display()

    driver.export_as(destination)
    driver.check(export_as_signal)
# -*- coding: utf-8 -*-

from hamcrest import equal_to
from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.export_as_dialog_driver import ExportAsDialogDriver
from tgit.ui.export_as_dialog import ExportAsDialog


@pytest.fixture()
def dialog(main_window):
    return ExportAsDialog(main_window, native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = ExportAsDialogDriver(window(QFileDialog, named('export-as-dialog')), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_export_destination(tmpdir, dialog, driver):
    destination = tmpdir.join("album.csv").strpath
    export_as_signal = ValueMatcherProbe('export as', equal_to(destination))

    dialog.export_as.connect(export_as_signal.received)
    dialog.open()

    driver.export_as(destination)
    driver.check(export_as_signal)
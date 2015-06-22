# -*- coding: utf-8 -*-
import os

from hamcrest import equal_to
from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.export_as_dialog_driver import ExportAsDialogDriver
from tgit.ui.export_as_dialog import ExportAsDialog


@pytest.fixture()
def dialog(qt):
    return ExportAsDialog(native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = ExportAsDialogDriver(window(QFileDialog, named('export-as-dialog')), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_export_destination(tmpdir, dialog, driver):
    destination = tmpdir.join("album.csv").strpath
    export_as_signal = ValueMatcherProbe('export as', equal_to(destination))

    dialog.select(lambda dest: export_as_signal.received(os.path.abspath(dest)))

    driver.export_as(destination)
    driver.check(export_as_signal)

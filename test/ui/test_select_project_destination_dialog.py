import os

import pytest
from PyQt5.QtWidgets import QFileDialog
from hamcrest import equal_to

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from testing.drivers import SelectProjectDestinationDialogDriver
from tgit.ui.dialogs.select_album_destination_dialog import make_select_project_destination_dialog

pytestmark = pytest.mark.ui


@pytest.fixture()
def show_dialog(on_select=ignore):
    dialog = make_select_project_destination_dialog(on_select, native=False, delete_on_close=False)
    show_(dialog)
    return dialog


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = SelectProjectDestinationDialogDriver(
        window(QFileDialog, named("select_project_destination_dialog")),
        prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


def test_signals_select_album_destination(tmpdir, driver):
    destination = tmpdir.strpath
    select_album_destination_signal = ValueMatcherProbe("select destination", equal_to(destination))

    _ = show_dialog(on_select=lambda dest: select_album_destination_signal.received(os.path.abspath(dest)))

    driver.select_destination(destination)
    driver.check(select_album_destination_signal)

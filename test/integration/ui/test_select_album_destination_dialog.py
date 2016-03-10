import os

from hamcrest import equal_to
from PyQt5.QtWidgets import QFileDialog
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.select_album_destination_dialog_driver import SelectProjectDestinationDialogDriver
from tgit.ui.dialogs.select_album_destination_dialog import SelectProjectDestinationDialog

pytestmark = pytest.mark.ui


@pytest.fixture()
def dialog(qt):
    return SelectProjectDestinationDialog(native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = SelectProjectDestinationDialogDriver(
        window(QFileDialog, named("select_project_destination_dialog")),
        prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_select_album_destination(tmpdir, dialog, driver):
    destination = tmpdir.strpath
    select_album_destination_signal = ValueMatcherProbe("select destination", equal_to(destination))

    dialog.select(lambda dest: select_album_destination_signal.received(os.path.abspath(dest)))

    driver.select_destination(destination)
    driver.check(select_album_destination_signal)

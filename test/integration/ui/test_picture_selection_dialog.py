import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with
import pytest

from cute.matchers import named
from cute.platforms import linux
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import PictureSelectionDialogDriver
from test.integration.ui import ignore
from test.util import resources
from tgit.platforms import windows
from tgit.ui.dialogs.picture_selection_dialog import PictureSelectionDialog

pytestmark = pytest.mark.ui


def show_dialog(on_select=ignore):
    dialog = PictureSelectionDialog(native=False)
    dialog.select(on_select)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = PictureSelectionDialogDriver(window(QFileDialog, named("picture-selection-dialog")), prober,
                                                 automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_picture_selected(driver):
    signal = ValueMatcherProbe("picture selected", resources.path("front-cover.jpg"))
    _ = show_dialog(lambda destination: signal.received(os.path.abspath(destination)))

    driver.select_picture(resources.path("front-cover.jpg"))
    driver.check(signal)


@pytest.mark.skipif(windows, reason="not supported on Windows")
@pytest.mark.skipif(linux, reason="not supported on Linux")
def test_only_accepts_picture_files(driver):
    _ = show_dialog()
    driver.rejects_selection_of(resources.path("base.mp3"))


def test_initially_starts_in_user_pictures_folder(driver):
    _ = show_dialog()
    driver.has_current_directory(ends_with("Pictures"))

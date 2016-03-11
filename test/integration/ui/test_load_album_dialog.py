import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.load_album_dialog_driver import LoadProjectDialogDriver
from test.util import resources
from tgit.platforms import windows, linux
from tgit.ui.dialogs.load_album_dialog import LoadProjectDialog

pytestmark = pytest.mark.ui

do_nothing = lambda *_: None

DISPLAY_DELAY = 250


@pytest.fixture()
def dialog(qt):
    return LoadProjectDialog(native=False)


@pytest.yield_fixture()
def driver(dialog, prober, automaton):
    dialog_driver = LoadProjectDialogDriver(window(QFileDialog, named("load_project_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def ignore(*args):
    pass


def test_signals_when_album_selected(dialog, driver):
    album_selected_signal = ValueMatcherProbe("album file selected", resources.path("album.tgit"))
    dialog.select(lambda dest: album_selected_signal.received(os.path.abspath(dest)))

    driver.load(resources.path("album.tgit"))
    driver.check(album_selected_signal)


@pytest.mark.skipif(windows, reason="not supported on Windows")
@pytest.mark.skipif(linux, reason="not supported on Linux")
def test_only_accepts_tgit_album_files(dialog, driver):
    dialog.select(ignore)

    driver.rejects_selection_of(resources.path("base.mp3"))


def test_initially_starts_in_documents_folder(driver):
    driver.has_current_directory(ends_with("Documents"))

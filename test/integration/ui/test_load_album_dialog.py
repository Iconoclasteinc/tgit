import os

from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers.load_album_dialog_driver import LoadProjectDialogDriver
from test.integration.ui import ignore
from test.util import resources
from tgit.platforms import windows, linux
from tgit.ui.dialogs.load_album_dialog import LoadProjectDialog

pytestmark = pytest.mark.ui


def show_dialog(on_select=ignore):
    dialog = LoadProjectDialog(native=False)
    dialog.select(on_select)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = LoadProjectDialogDriver(window(QFileDialog, named("load_project_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_signals_when_project_selected(driver):
    project_selected_signal = ValueMatcherProbe("project file selected", resources.path("album.tgit"))
    _ = show_dialog(on_select=lambda dest: project_selected_signal.received(os.path.abspath(dest)))

    driver.load(resources.path("album.tgit"))
    driver.check(project_selected_signal)


def test_initially_starts_in_documents_folder(driver):
    _ = show_dialog()
    driver.has_current_directory(ends_with("Documents"))


@pytest.mark.skipif(windows, reason="not supported on Windows")
@pytest.mark.skipif(linux, reason="not supported on Linux")
def test_only_accepts_tgit_project_files(driver):
    _ = show_dialog()

    driver.rejects_selection_of(resources.path("base.mp3"))

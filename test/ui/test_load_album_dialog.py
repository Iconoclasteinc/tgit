import os

import pytest
from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.ui import ignore, show_, close_
from test.util import resources
from testing.drivers import LoadProjectDialogDriver
from tgit.platforms import windows, linux
from tgit.ui.dialogs.load_album_dialog import make_load_project_dialog

pytestmark = pytest.mark.ui


def show_dialog(on_select=ignore):
    dialog = make_load_project_dialog(on_select, native=False, delete_on_close=False)
    show_(dialog)
    return dialog


@pytest.yield_fixture()
def driver(prober, automaton):
    dialog_driver = LoadProjectDialogDriver(window(QFileDialog, named("load_project_dialog")), prober, automaton)
    yield dialog_driver
    close_(dialog_driver)


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

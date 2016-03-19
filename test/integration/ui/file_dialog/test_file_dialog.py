# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog
from hamcrest import ends_with, assert_that, equal_to
import pytest

from cute.widgets import QFileDialogDriver, window
from tgit.ui import locations
from tgit.ui.dialogs.file_dialog import make_file_dialog, name_filter

pytestmark = pytest.mark.ui


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = QFileDialogDriver(window(QFileDialog), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def show_dialog(name_filters="", file_mode=QFileDialog.ExistingFile, directory="", parent=None):
    dialog = make_file_dialog(name_filters, file_mode, directory, parent, False)
    dialog.open()
    return dialog


def test_shows_name_filters(driver):
    _ = show_dialog("PNG Images (*.png)")
    driver.filter_files_of_type("PNG Images (*.png)")


def test_initially_starts_in_directory(driver):
    _ = show_dialog(directory=locations.Documents)
    driver.has_current_directory(ends_with("Documents"))


def test_builds_name_filters():
    assert_that(name_filter(["type1", "type2"], "caption"), equal_to("caption (*.type1 *.type2)"), "The name filters")
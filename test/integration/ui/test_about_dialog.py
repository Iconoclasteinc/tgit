import sys

import mutagen
import pytest
from PyQt5.QtCore import Qt, QT_VERSION_STR, PYQT_VERSION_STR

from cute.matchers import named
from cute.widgets import window
from test.drivers.about_dialog_driver import AboutDialogDriver
from tgit import __version__
from tgit.platforms import mac
from tgit.ui.dialogs.about_dialog import AboutDialog

pytestmark = pytest.mark.ui

DISPLAY_DELAY = 200 if mac else 0


def show_dialog():
    dialog = AboutDialog()
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.show()
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = AboutDialogDriver(window(AboutDialog, named("about_tgit_dialog")), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_shows_application_version(driver):
    _ = show_dialog()
    driver.shows_tgit_version(__version__)


def test_shows_mutagen_version(driver):
    _ = show_dialog()
    driver.shows_mutagen_version(mutagen.version_string)


def test_shows_python_version(driver):
    _ = show_dialog()
    driver.shows_python_version("{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))


def test_shows_qt_version(driver):
    _ = show_dialog()
    driver.shows_qt_version(QT_VERSION_STR)


def test_shows_pyqt_version(driver):
    _ = show_dialog()
    driver.shows_pyqt_version(PYQT_VERSION_STR)


def test_closes_dialog(driver):
    _ = show_dialog()
    driver.pause(DISPLAY_DELAY)
    driver.click_ok()
    driver.is_hidden()

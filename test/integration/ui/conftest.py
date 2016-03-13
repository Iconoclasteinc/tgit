import sip
from traceback import format_exception
import sys

from PyQt5.QtWidgets import QApplication
import pytest

from cute.animatron import Animatron
from cute.prober import EventProcessingProber
from cute.robot import Robot


def _print_unhandled_exceptions():
    def exception_hook(exctype, value, traceback):
        for line in format_exception(exctype, value, traceback):
            print(line, file=sys.stderr)

    sys.excepthook = exception_hook


@pytest.yield_fixture()
def qt():
    app = QApplication([])
    _print_unhandled_exceptions()
    yield app
    app.quit()
    # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
    # Never ever remove this!!
    sip.delete(app)


@pytest.fixture()
def prober():
    return EventProcessingProber()


@pytest.fixture()
def automaton():
    return Animatron()


@pytest.fixture()
def robot():
    return Robot()


@pytest.fixture()
def animaton():
    return Animatron()

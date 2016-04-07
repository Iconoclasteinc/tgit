# -*- coding: utf-8 -*-
import sip
import sys
from traceback import format_exception

import pytest
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from cute import event_loop
from cute.platforms import linux

END_OF_TEST_PAUSE = 50 if linux else 0


def _print_unhandled_exceptions():
    def exception_hook(exctype, value, traceback):
        for line in format_exception(exctype, value, traceback):
            print(line, file=sys.stderr)

    sys.excepthook = exception_hook


def pytest_collection_modifyitems(session, config, items):
    unit = [item for item in items if item.get_marker("unit")]
    integration = [item for item in items if item.get_marker("integration")]
    ui = [item for item in items if item.get_marker("ui")]
    feature = [item for item in items if item.get_marker("feature")]
    unmarked = [item for item in items if
                item not in unit and item not in integration and item not in ui and item not in feature]

    items.clear()
    items.extend(unit + integration + ui + feature + unmarked)


@pytest.yield_fixture()
def qt():
    _print_unhandled_exceptions()
    application = QApplication([])
    yield application
    event_loop.process_events_for(END_OF_TEST_PAUSE)
    # If we don't force deletion of the C++ wrapped object, it causes the test suite to eventually crash
    # Never ever remove this!!
    sip.delete(application)


@pytest.fixture
def settings(qt, tmpdir):
    return QSettings(tmpdir.join("settings.ini").strpath, QSettings.IniFormat)

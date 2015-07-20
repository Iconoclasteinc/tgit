# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
import pytest

from cute.probes import ValueMatcherProbe
from cute.widgets import WidgetDriver, window
from tgit.ui.closeable import Closeable


@Closeable
class CloseableWidget(QWidget):
    closed = pyqtSignal()


@pytest.fixture()
def driver(qt, prober, automaton):
    return WidgetDriver(window(QWidget), prober, automaton)


def test_signals_close_event_on_close(driver):
    closed_signal = ValueMatcherProbe("closed signal")

    widget = CloseableWidget()
    widget.on_close(closed_signal.received)

    widget.close()

    driver.check(closed_signal)


# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from cute.probes import ValueMatcherProbe
from tgit.ui.closeable import Closeable


@Closeable
class CloseableWidget(QWidget):
    closed = pyqtSignal()


def test_signals_close_event_on_close(widget_driver):
    closed_signal = ValueMatcherProbe("closed signal")

    widget = CloseableWidget()
    widget.closed.connect(closed_signal.received)

    widget.close()

    widget_driver.check(closed_signal)

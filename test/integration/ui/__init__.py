# -*- coding: utf-8 -*-

import os
import unittest

from PyQt5.QtWidgets import QApplication

from cute.prober import EventProcessingProber
from cute.robot import Robot
from tgit import ui
from tgit.ui.main_window import StyleSheet

SIZE = (1100, 745)


def show_widget(widget):
    widget.setStyleSheet(StyleSheet)
    widget.setFixedSize(*SIZE)
    ui.showCenteredOnScreen(widget)


END_OF_TEST_PAUSE = int(os.environ.get('END_OF_TEST_PAUSE', 0))


class WidgetTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeout_in_ms=1000)
        self.gesture_performer = Robot()
        self.driver = None

    def show(self, widget):
        widget.setStyleSheet(StyleSheet)
        widget.setFixedSize(*SIZE)
        ui.showCenteredOnScreen(widget)

    def check(self, probe):
        self.prober.check(probe)

    def pause(self, ms):
        self.gesture_performer.delay(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        if self.driver:
            self.driver.close()
            del self.driver

        del self.gesture_performer
        del self.prober
        self.app.quit()
        del self.app
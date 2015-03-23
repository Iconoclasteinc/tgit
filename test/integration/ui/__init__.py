# -*- coding: utf-8 -*-

import os
import unittest

from PyQt5.QtWidgets import QApplication

from test.cute.events import MainEventLoop
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot
from tgit.ui import showCenteredOnScreen
from tgit.ui.main_window import MainWindow, StyleSheet


END_OF_TEST_PAUSE = int(os.environ.get('END_OF_TEST_PAUSE', 0))


class WidgetTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()
        self.driver = None

    def show(self, widget):
        widget.setStyleSheet(StyleSheet)
        widget.setFixedSize(*MainWindow.SIZE)
        showCenteredOnScreen(widget)

    def check(self, probe):
        self.prober.check(probe)

    def pause(self, ms):
        MainEventLoop.processEventsFor(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        if self.driver:
            self.driver.close()
            del self.driver

        del self.gesturePerformer
        del self.prober
        self.app.quit()
        del self.app
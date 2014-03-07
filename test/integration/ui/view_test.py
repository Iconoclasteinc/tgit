# -*- coding: utf-8 -*-

import os
import unittest

import sip
from PyQt4.QtGui import QApplication

from test.cute.events import MainEventLoop
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot

from tgit.ui import style
from tgit.ui import display
from tgit.ui.main_window import MainWindow

END_OF_TEST_PAUSE = int(os.environ.get('END_OF_TEST_PAUSE', 0))


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()
        self.driver = None

    def show(self, widget):
        widget.setStyleSheet(style.Sheet)
        widget.setFixedSize(*MainWindow.SIZE)
        display.centeredOnScreen(widget)

    def check(self, probe):
        self.prober.check(probe)

    def pause(self, ms):
        MainEventLoop.processEventsFor(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        if self.driver:
            self.driver.close()
            del self.driver

        sip.delete(self.app)
        del self.app

# -*- coding: utf-8 -*-

import os
import unittest

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
from PyQt4.QtGui import QApplication

from tests.cute.events import MainEventLoop
from tests.cute.prober import EventProcessingProber
from tests.cute.robot import Robot

END_OF_TEST_PAUSE = int(os.environ.get('END_OF_TEST_PAUSE', 0))


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()
        self.driver = None

    def view(self, widget):
        widget.show()
        widget.raise_()

    def pause(self, ms):
        MainEventLoop.processEventsFor(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        if self.driver:
            self.driver.close()
            del self.driver
        del self.app

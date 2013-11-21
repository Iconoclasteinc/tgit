# -*- coding: utf-8 -*-

import os
import unittest

import sip
# noinspection PyUnresolvedReferences
import use_sip_api_v2
from PyQt4.QtGui import QApplication

from test.cute.events import MainEventLoop
from test.cute.prober import EventProcessingProber
from test.cute.robot import Robot

from tgit.ui import constants as ui
from tgit.ui import display

END_OF_TEST_PAUSE = int(os.environ.get('END_OF_TEST_PAUSE', 0))


class BaseWidgetTest(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()

    def view(self, widget):
        widget.setFixedSize(*ui.MAIN_WINDOW_SIZE)
        display.centeredOnScreen(widget)
        widget.show()
        widget.raise_()

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

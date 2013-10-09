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

END_OF_TEST_PAUSE = int(os.environ.get('END_OF_TEST_PAUSE', 0))


class BaseWidgetTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()
        self.tagger = None

    def view(self, widget):
        widget.show()
        widget.raise_()

    def pause(self, ms):
        MainEventLoop.processEventsFor(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        if self.tagger:
            self.tagger.close()
            del self.tagger

        sip.delete(self.app)
        del self.app

# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
# todo Settle on a practice for importing Qt classes
from PyQt4.Qt import QApplication

from tests.cute.events import MainEventLoop
from tests.cute.prober import EventProcessingProber
from tests.cute.robot import Robot
from tests.cute.finders import WidgetSelector
from tests.drivers.album_panel_driver import AlbumPanelDriver

from tgit.ui.album_panel import AlbumPanel


def buildTrack(**tags):
    defaults = dict(releaseName=None,
                    frontCoverPicture=(None, None),
                    leadPerformer=None,
                    releaseDate=None,
                    upc=None)
    return flexmock(**dict(defaults.items() + tags.items()))


END_OF_TEST_PAUSE = 500


# todo Extract an abstract base class for ui integration tests
class AlbumPanelTest(unittest.TestCase):
    # todo make this configurable through an environment variable to speed up build
    # on demand

    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber()
        self.gesturePerformer = Robot()
        self.albumPanel = AlbumPanel()
        self.view(self.albumPanel)
        self.driver = self.createDriverFor(self.albumPanel)

    def createDriverFor(self, widget):
        return AlbumPanelDriver(self.selectorFor(widget), self.prober, self.gesturePerformer)

    def view(self, widget):
        widget.show()
        widget.raise_()

    def pause(self, ms):
        MainEventLoop.processEventsFor(ms)

    def tearDown(self):
        self.pause(END_OF_TEST_PAUSE)
        self.driver.close()
        del self.driver
        del self.app

    def testCanShow(self):
        pass

    def testDisplaysReleaseName(self):
        track = buildTrack(releaseName='Release Name')
        self.albumPanel.trackSelected(track)
        self.driver.showsReleaseName('Release Name')

    def selectorFor(self, widget):
        # todo Move to finders.py
        class WidgetIdentity(WidgetSelector):
            def __init__(self, widget):
                self._widget = widget

            def test(self):
                pass

            def widgets(self):
                return self._widget,

            def widget(self):
                return self._widget

            def isSatisfied(self):
                return True

            def describeTo(self, description):
                description.append_text("the exact ") \
                    .append_text(type(self._widget).__name__) \
                    .append_text(" '%s'" % repr(self._widget))

            def describeFailureTo(self, description):
                self.describeTo(description)

        return WidgetIdentity(widget)



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
from tests.drivers.track_panel_driver import TrackPanelDriver

from tgit.ui.track_panel import TrackPanel


def buildTrack(**tags):
    defaults = dict(trackTitle=None,
                    versionInfo=None,
                    featuredGuest=None,
                    isrc=None,
                    bitrate=96000,
                    duration=200)
    return flexmock(**dict(defaults.items() + tags.items()))


END_OF_TEST_PAUSE = 250


# todo Extract an abstract base class for ui integration tests
class TrackPanelTest(unittest.TestCase):
    # todo make this configurable through an environment variable to speed up build
    # on demand

    def setUp(self):
        self.app = QApplication([])
        self.prober = EventProcessingProber(timeoutInMs=1000)
        self.gesturePerformer = Robot()
        self.trackPanel = TrackPanel()
        self.view(self.trackPanel)
        self.driver = self.createDriverFor(self.trackPanel)

    def createDriverFor(self, widget):
        return TrackPanelDriver(self.selectorFor(widget), self.prober, self.gesturePerformer)

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

    def testDisplaysTrackTitle(self):
        track = buildTrack(trackTitle='Track Title')
        self.trackPanel.trackSelected(track)
        self.driver.showsTrackTitle('Track Title')

    def testDisplaysVersionInfo(self):
        track = buildTrack(versionInfo='Version Info')
        self.trackPanel.trackSelected(track)
        self.driver.showsVersionInfo('Version Info')

    def testDisplaysFeaturedGuest(self):
        track = buildTrack(featuredGuest='Featured Guest')
        self.trackPanel.trackSelected(track)
        self.driver.showsFeaturedGuest('Featured Guest')

    def testDisplaysIsrc(self):
        track = buildTrack(isrc='ISRC')
        self.trackPanel.trackSelected(track)
        self.driver.showsIsrc('ISRC')

    def testDisplaysBitrateInKbps(self):
        track = buildTrack(bitrate=128000)
        self.trackPanel.trackSelected(track)
        self.driver.showsBitrate('128 kbps')

    def testDisplaysDurationAsText(self):
        track = buildTrack(duration=275)
        self.trackPanel.trackSelected(track)
        self.driver.showsDuration('04:35')

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
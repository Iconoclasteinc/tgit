# -*- coding: utf-8 -*-

import unittest

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.drivers.track_panel_driver import TrackPanelDriver
from test.util import doubles

from tgit.ui.track_panel import TrackPanel


class TrackPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackPanelTest, self).setUp()
        self.trackPanel = TrackPanel()
        self.view(self.trackPanel)
        self.driver = self.createDriverFor(self.trackPanel)

    def createDriverFor(self, widget):
        return TrackPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    @unittest.skip("todo")
    def testHasNothingToShowWhenTrackHasNoMetadata(self):
        raise AssertionError("Not yet implemented")

    def testDisplaysTrackTitle(self):
        track = doubles.track(trackTitle='Track Title')
        self.trackPanel.setTrack(track)
        self.driver.showsTrackTitle('Track Title')

    def testDisplaysVersionInfo(self):
        track = doubles.track(versionInfo='Version Info')
        self.trackPanel.setTrack(track)
        self.driver.showsVersionInfo('Version Info')

    def testDisplaysFeaturedGuest(self):
        track = doubles.track(featuredGuest='Featured Guest')
        self.trackPanel.setTrack(track)
        self.driver.showsFeaturedGuest('Featured Guest')

    def testDisplaysIsrc(self):
        track = doubles.track(isrc='ISRC')
        self.trackPanel.setTrack(track)
        self.driver.showsIsrc('ISRC')

    def testDisplaysBitrateInKbps(self):
        track = doubles.track(bitrate=128000)
        self.trackPanel.setTrack(track)
        self.driver.showsBitrate('128 kbps')

    def testDisplaysDurationAsText(self):
        track = doubles.track(duration=275)
        self.trackPanel.setTrack(track)
        self.driver.showsDuration('04:35')

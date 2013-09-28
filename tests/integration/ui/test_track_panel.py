# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)

from tests.cute.finders import WidgetIdentity
from tests.drivers.track_panel_driver import TrackPanelDriver
from tests.integration.ui.base_widget_test import BaseWidgetTest

from tgit.ui.track_panel import TrackPanel


def buildTrack(**tags):
    defaults = dict(trackTitle=None,
                    versionInfo=None,
                    featuredGuest=None,
                    isrc=None,
                    bitrate=96000,
                    duration=200)
    return flexmock(**dict(defaults.items() + tags.items()))


class TrackPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackPanelTest, self).setUp()
        self.trackPanel = TrackPanel()
        self.view(self.trackPanel)
        self.driver = self.createDriverFor(self.trackPanel)

    def createDriverFor(self, widget):
        return TrackPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

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

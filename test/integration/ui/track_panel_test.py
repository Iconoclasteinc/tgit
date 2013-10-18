# -*- coding: utf-8 -*-

from datetime import timedelta
from hamcrest import assert_that, equal_to

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.cute.probes import AssertionProbe
from test.drivers.track_panel_driver import TrackPanelDriver
from test.util import builders

from tgit.ui.track_panel import TrackPanel


class TrackPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackPanelTest, self).setUp()
        self.track = builders.track()
        self.trackPanel = TrackPanel(self.track)
        self.view(self.trackPanel)
        self.tagger = self.createDriverFor(self.trackPanel)

    def createDriverFor(self, widget):
        return TrackPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysTrackMetadata(self):
        self.trackPanel.trackStateChanged(builders.track(
            trackTitle='Song',
            versionInfo='Remix',
            featuredGuest='Featuring',
            isrc='Code',
            bitrate=192000,
            duration=timedelta(minutes=4, seconds=35).total_seconds()))

        self.tagger.showsTrackTitle('Song')
        self.tagger.showsVersionInfo('Remix')
        self.tagger.showsFeaturedGuest('Featuring')
        self.tagger.showsBitrate('192 kbps')
        self.tagger.showsIsrc('Code')
        self.tagger.showsDuration('04:35')

    def testUpdatesTrackOnMetadataChange(self):
        self.tagger.changeTrackTitle('Song')
        self.check(AssertionProbe(self.track.trackTitle, equal_to('Song'), 'track title'))

        self.tagger.changeVersionInfo('Remix')
        self.check(AssertionProbe(self.track.versionInfo, equal_to('Remix'), 'version info'))

        self.tagger.changeFeaturedGuest('Featuring')
        self.check(AssertionProbe(self.track.featuredGuest, equal_to('Featuring'),
                                  'featured guest'))

        self.tagger.changeIsrc('Code')
        self.check(AssertionProbe(self.track.isrc, equal_to('Code'), 'isrc'))
# -*- coding: utf-8 -*-

from datetime import timedelta
from hamcrest import assert_that, equal_to

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.drivers.track_panel_driver import TrackPanelDriver
from test.util import doubles

from tgit.track import Track
from tgit.ui.track_panel import TrackPanel


class TrackPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackPanelTest, self).setUp()
        self.track = doubles.track(bitrate=192000,
                                   duration=timedelta(minutes=4, seconds=35).total_seconds())
        self.trackPanel = TrackPanel(self.track)
        self.view(self.trackPanel)
        self.tagger = self.createDriverFor(self.trackPanel)

    def createDriverFor(self, widget):
        return TrackPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysTrackTitle(self):
        self.track.trackTitle = 'Song'
        self.track.versionInfo = 'Remix'
        self.track.featuredGuest = 'Featuring'
        self.track.isrc = 'Code'

        self.trackPanel.trackStateChanged(self.track)
        self.tagger.showsTrackTitle('Song')
        self.tagger.showsVersionInfo('Remix')
        self.tagger.showsFeaturedGuest('Featuring')
        self.tagger.showsBitrate('192 kbps')
        self.tagger.showsIsrc('Code')
        self.tagger.showsDuration('04:35')

    def testUpdatesTrackMetadataWithUserEntries(self):
        self.tagger.changeTrackTitle('Song')
        self.tagger.changeVersionInfo('Remix')
        self.tagger.changeFeaturedGuest('Featuring')
        self.tagger.changeIsrc('Code')

        self.trackPanel.updateTrack()
        assert_that(self.track.trackTitle, equal_to('Song'), 'track title')
        assert_that(self.track.versionInfo, equal_to('Remix'), 'versio info')
        assert_that(self.track.featuredGuest, equal_to('Featuring'), 'featured guest')
        assert_that(self.track.isrc, equal_to('Code'), 'isrc')
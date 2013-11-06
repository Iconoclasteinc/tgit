# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import equal_to

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import AssertionProbe
from test.drivers.track_page_driver import TrackPageDriver
from test.util.builders import track

from tgit.ui.track_page import TrackPage


class TrackPageTest(BaseWidgetTest):
    def setUp(self):
        super(TrackPageTest, self).setUp()
        self.track = track(bitrate=192000,
                           duration=timedelta(minutes=4, seconds=35).total_seconds())
        self.widget = TrackPage(self.track)
        self.view(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TrackPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysTrackMetadata(self):
        self.track.trackTitle = 'Song'
        self.driver.showsTrackTitle('Song')
        self.track.versionInfo = 'Remix'
        self.driver.showsVersionInfo('Remix')
        self.track.featuredGuest = 'Featuring'
        self.driver.showsFeaturedGuest('Featuring')
        self.track.lyricist = 'Lyricist'
        self.driver.showsLyricist('Lyricist')
        self.track.composer = 'Composer'
        self.driver.showsComposer('Composer')
        self.track.publisher = 'Publisher'
        self.driver.showsPublisher('Publisher')
        self.track.isrc = 'Code'
        self.driver.showsIsrc('Code')

        self.driver.showsBitrate('192 kbps')
        self.driver.showsDuration('04:35')

    def testUpdatesTrackOnMetadataChange(self):
        self.driver.changeTrackTitle('Song')
        self.check(AssertionProbe(self.track.trackTitle, equal_to('Song'), 'track title'))

        self.driver.changeVersionInfo('Remix')
        self.check(AssertionProbe(self.track.versionInfo, equal_to('Remix'), 'version info'))

        self.driver.changeFeaturedGuest('Featuring')
        self.check(AssertionProbe(self.track.featuredGuest, equal_to('Featuring'),
                                  'featured guest'))

        self.driver.changeLyricist('Lyricist')
        self.check(AssertionProbe(self.track.lyricist, equal_to('Lyricist'), 'lyricist'))

        self.driver.changeComposer('Composer')
        self.check(AssertionProbe(self.track.composer, equal_to('Composer'),  'composer'))

        self.driver.changePublisher('Publisher')
        self.check(AssertionProbe(self.track.publisher, equal_to('Publisher'), 'publisher'))

        self.driver.changeIsrc('Code')
        self.check(AssertionProbe(self.track.isrc, equal_to('Code'), 'isrc'))
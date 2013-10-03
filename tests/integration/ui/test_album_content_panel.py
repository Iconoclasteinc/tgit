# -*- coding: utf-8 -*-

import unittest
from datetime import timedelta
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)

from tgit.ui.album_content_panel import AlbumContentPanel

from tests.integration.ui.base_widget_test import BaseWidgetTest
from tests.cute.finders import WidgetIdentity
from tests.drivers.album_content_panel_driver import AlbumContentPanelDriver
from tests.util import doubles


class FakePlayer(object):
    source = None
    playing = False

    def hasSource(self, filename):
        return self.source == filename

    def setSource(self, filename):
        self.source = filename
        self.playing = False

    def isPlaying(self):
        return self.playing

    def play(self):
        self.playing = True

    def stop(self):
        self.playing = False


class AlbumContentPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumContentPanelTest, self).setUp()
        self.player = flexmock(FakePlayer())
        self.panel = AlbumContentPanel(player=self.player)
        self.view(self.panel)
        self.driver = self.createDriverFor(self.panel)

    def tearDown(self):
        super(AlbumContentPanelTest, self).tearDown()

    def createDriverFor(self, widget):
        return AlbumContentPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    @unittest.skip("we cannot rely on widgets order")
    # we need to use a proper table
    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeadings('Track Title', 'Duration')

    @unittest.skip("we cannot rely on widgets order")
    def testDisplaysTrackDetailsInColumns(self):
        track = doubles.track(trackTitle='Banana Song',
                              duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.panel.addTrack(track)
        self.driver.showsTrackDetails(1, 'Banana Song', '03:43')

    @unittest.skip("we cannot rely on widgets order")
    def testDisplaysAllTracksInRows(self):
        self.panel.addTrack(doubles.track(trackTitle='Track 1'))
        self.panel.addTrack(doubles.track(trackTitle='Track 2'))
        self.driver.showsTrackDetails(1, 'Track 1')
        self.driver.showsTrackDetails(2, 'Track 2')

    def _notPlaying(self, track):
        return lambda: not self.player.hasSource(track)

    def _isNotPlaying(self, filename):
        return lambda: not self.player.hasSource(filename)

    def testCanPlayAndStopATrack(self):
        self.panel.addTrack(doubles.track(filename='track.mp3'))

        self.player.should_call('setSource').once().with_args('track.mp3') \
            .when(self._isNotPlaying('track.mp3'))
        self.player.should_call('play').twice().when(lambda: not self.player.isPlaying())
        self.player.should_call('stop').once().when(lambda: self.player.isPlaying())

        self.driver.playTrack(1)
        self.driver.stopTrack(1)
        self.driver.playTrack(1)

    @unittest.skip("we cannot rely on widgets order")
    def testPlayingATrackStopsCurrentlyPlayingTrack(self):
        self.panel.addTrack(doubles.track(filename='track1.mp3'))
        self.panel.addTrack(doubles.track(filename='track2.mp3'))

        self.player.should_call('setSource').with_args('track1.mp3').ordered()
        self.player.should_call('setSource').with_args('track2.mp3').ordered()
        self.player.should_call('play').twice().when(lambda: not self.player.isPlaying())

        self.driver.playTrack(1)
        self.driver.playButton(1).isDown()
#        self.driver.playButton(2).isUp()
        self.driver.playTrack(2)
#        self.driver.playButton(1).isUp()
        self.driver.playButton(2).isDown()

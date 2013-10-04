# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock

from tests.integration.ui.base_widget_test import BaseWidgetTest

from tests.cute.finders import WidgetIdentity
from tests.drivers.track_list_panel_driver import TrackListPanelDriver
from tests.util import doubles

from tgit.ui.track_list_panel import TrackListPanel


class FakePlayer(object):
    def __init__(self):
        self.playing = False

    def isPlaying(self):
        return self.playing

    def play(self, track):
        self.playing = True

    def stop(self):
        self.playing = False


class TrackListPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackListPanelTest, self).setUp()
        self.player = flexmock(FakePlayer())
        self.panel = TrackListPanel(player=self.player)
        self.view(self.panel)
        self.tagger = self.createDriverFor(self.panel)

    def tearDown(self):
        super(TrackListPanelTest, self).tearDown()

    def createDriverFor(self, widget):
        return TrackListPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.tagger.showsColumnHeaders('Track Title', 'Duration', '')

    def testDisplaysTrackDetailsInColumns(self):
        track = doubles.track(trackTitle='Banana Song',
                              duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.panel.addTrack(track)
        self.tagger.showsTrack('Banana Song', '03:43')

    def testDisplaysAllTracksInRows(self):
        self.panel.addTrack(doubles.track(trackTitle='Track 1'))
        self.panel.addTrack(doubles.track(trackTitle='Track 2'))
        self.tagger.showsTrack('Track 1')
        self.tagger.showsTrack('Track 2')

    def testCanPlayAndStopATrack(self):
        self.panel.addTrack(doubles.track(filename='track.mp3'))

        self.player.should_call('play').twice().with_args('track.mp3').when(self._notPlayingMusic())
        self.player.should_call('stop').once().when(self._playingMusic())

        self.tagger.playTrack(1)
        self.tagger.stopTrack(1)
        self.tagger.playTrack(1)

    def testPlayingATrackStopsCurrentlyPlayingTrack(self):
        self.panel.addTrack(doubles.track(filename='track1.mp3'))
        self.panel.addTrack(doubles.track(filename='track2.mp3'))

        self.player.should_call('play').with_args('track1.mp3').ordered()
        self.player.should_call('play').with_args('track2.mp3').ordered()

        self.tagger.playTrack(1)
        self.tagger.playTrack(2)

    def _notPlayingMusic(self):
        return lambda: not self.player.isPlaying()

    def _playingMusic(self):
        return lambda: self.player.isPlaying()

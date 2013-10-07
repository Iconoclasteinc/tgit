# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.drivers.track_list_panel_driver import TrackListPanelDriver
from test.util import doubles

from tgit.ui.track_list_panel import TrackListPanel


class FakePlayer(object):
    def __init__(self):
        self.track = None

    def isPlaying(self):
        return self.track is not None

    def play(self, track):
        if self.track:
            self.listener.mediaStopped(self.track)
        self.track = track

    def stop(self):
        self.track = None

    def addMediaListener(self, listener):
        self.listener = listener


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
        track = doubles.track()
        self.panel.addTrack(track)

        self.player.should_call('play').once().with_args(track).when(self._notPlayingMusic())
        self.player.should_call('stop').once().when(self._playingMusic())

        self.tagger.isNotPlayingTrack(1)
        self.tagger.clickPlayButton(1)
        self.tagger.isPlayingTrack(1)
        self.tagger.clickPlayButton(1)
        self.tagger.isNotPlayingTrack(1)

    def testPlayingATrackStopsCurrentlyPlayingTrack(self):
        firstTrack = doubles.track()
        self.panel.addTrack(firstTrack)
        secondTrack = doubles.track()
        self.panel.addTrack(secondTrack)

        self.player.should_call('play').once().with_args(firstTrack).ordered()
        self.player.should_call('play').once().with_args(secondTrack).ordered()

        self.tagger.playTrack(1)
        self.tagger.playTrack(2)
        self.tagger.isNotPlayingTrack(1)

    def testPlayButtonIsRestoredWhenTrackHasFinishedPlaying(self):
        track = doubles.track()
        self.panel.addTrack(track)
        self.tagger.playTrack(1)
        self.panel.mediaPaused(track)
        self.tagger.isNotPlayingTrack(1)

    def _notPlayingMusic(self):
        return lambda: not self.player.isPlaying()

    def _playingMusic(self):
        return lambda: self.player.isPlaying()

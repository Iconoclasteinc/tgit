# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock
from hamcrest import equal_to

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.track_list_panel_driver import TrackListPanelDriver
from test.util import doubles

from tgit.null import Null
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
        self.trackList = TrackListPanel(player=self.player, handler=Null())
        self.view(self.trackList)
        self.tagger = self.createDriverFor(self.trackList)

    def tearDown(self):
        super(TrackListPanelTest, self).tearDown()

    def createDriverFor(self, widget):
        return TrackListPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.tagger.showsColumnHeaders('Track Title', 'Duration', '')

    def testDisplaysTrackDetailsInColumns(self):
        track = doubles.track(trackTitle='Banana Song',
                              duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.trackList.addTrack(track)
        self.tagger.showsTrack('Banana Song', '03:43')

    def testDisplaysAllTracksInRows(self):
        self.trackList.addTrack(doubles.track(trackTitle='Track 1'))
        self.trackList.addTrack(doubles.track(trackTitle='Track 2'))
        self.tagger.showsTrack('Track 1')
        self.tagger.showsTrack('Track 2')

    def testCanPlayAndStopATrack(self):
        track = doubles.track()
        self.trackList.addTrack(track)

        self.player.should_call('play').once().with_args(track).when(self._notPlayingMusic())
        self.player.should_call('stop').once().when(self._playingMusic())

        self.tagger.isNotPlayingTrack(1)
        self.tagger.clickPlayButton(1)
        self.tagger.isPlayingTrack(1)
        self.tagger.clickPlayButton(1)
        self.tagger.isNotPlayingTrack(1)

    def testPlayingATrackStopsCurrentlyPlayingTrack(self):
        firstTrack = doubles.track()
        self.trackList.addTrack(firstTrack)
        secondTrack = doubles.track()
        self.trackList.addTrack(secondTrack)

        self.player.should_call('play').once().with_args(firstTrack).ordered()
        self.player.should_call('play').once().with_args(secondTrack).ordered()

        self.tagger.playTrack(1)
        self.tagger.playTrack(2)
        self.tagger.isNotPlayingTrack(1)

    def testPlayButtonIsRestoredWhenTrackHasFinishedPlaying(self):
        track = doubles.track()
        self.trackList.addTrack(track)
        self.tagger.playTrack(1)
        self.trackList.mediaPaused(track)
        self.tagger.isNotPlayingTrack(1)

    def testAddsTrackToAlbumWhenAddButtonIsClicked(self):
        addTrackButtonClicked = ValueMatcherProbe(equal_to("clicked"), "add track button")

        class SelectTrackProbe(object):
            def selectTrack(self):
                addTrackButtonClicked.setReceivedValue("clicked")

        self.trackList.setRequestHandler(SelectTrackProbe())
        self.tagger.addTrack()
        self.tagger.check(addTrackButtonClicked)

    def _notPlayingMusic(self):
        return lambda: not self.player.isPlaying()

    def _playingMusic(self):
        return lambda: self.player.isPlaying()

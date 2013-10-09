# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock
from hamcrest import equal_to, has_property

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.track_list_panel_driver import TrackListPanelDriver
from test.util import doubles

from tgit.ui.track_list_panel import TrackListPanel


class PlayerStub(object):
    def __init__(self):
        self.track = None

    def isPlaying(self):
        return self.track is not None

    def play(self, track):
        self.track = track

    def stop(self):
        self.track = None

    def addMediaListener(self, listener):
        pass


class TrackListPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackListPanelTest, self).setUp()
        self.player = flexmock(PlayerStub())
        self.trackList = TrackListPanel(player=self.player)
        self.view(self.trackList)
        self.tagger = self.createDriverFor(self.trackList)

    def tearDown(self):
        super(TrackListPanelTest, self).tearDown()

    def createDriverFor(self, widget):
        return TrackListPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.tagger.showsColumnHeaders('Track Title', 'Lead Performer', 'Release Name',
                                       'Bitrate', 'Duration', '', '')

    def testDisplaysTrackDetailsInColumns(self):
        self._addTrackToList(trackTitle='Banana Song',
                             leadPerformer='Tim, Stuart, Dave',
                             releaseName='Despicable Me',
                             bitrate=192000,
                             duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.tagger.showsTrack('Banana Song', 'Tim, Stuart, Dave', 'Despicable Me',
                               '192 kbps', '03:43')

    def testDisplaysAllTracksInRows(self):
        self._addTrackToList(trackTitle='Track 0')
        self._addTrackToList(trackTitle='Track 1')

        self.tagger.hasTrackCount(2)
        self.tagger.showsTrack('Track 0')
        self.tagger.showsTrack('Track 1')

    def testCanPlayAndStopATrack(self):
        track = self._addTrackToList()

        self.player.should_call('play').once().with_args(track).when(self._notPlayingMusic())
        self.player.should_call('stop').once().when(self._playingMusic())

        self.tagger.isNotPlayingTrack(0)
        self.tagger.clickPlayButton(0)
        self.tagger.isPlayingTrack(0)
        self.tagger.clickPlayButton(0)
        self.tagger.isNotPlayingTrack(0)

    def testRestoreListenButtonStateWhenTrackHasFinishedPlaying(self):
        track0 = self._addTrackToList()
        track1 = self._addTrackToList()

        self.tagger.playTrack(0)
        self.trackList.mediaStopped(track0)
        self.tagger.isNotPlayingTrack(0)

        self.tagger.playTrack(1)
        self.trackList.mediaPaused(track1)
        self.tagger.isNotPlayingTrack(1)

    def testSelectsTrackWhenAddButtonIsClicked(self):
        addTrackButtonClicked = ValueMatcherProbe("add track button", equal_to("clicked"))

        class SelectTrackProbe(object):
            def selectTrack(self):
                addTrackButtonClicked.setReceivedValue("clicked")

        self.trackList.setRequestHandler(SelectTrackProbe())
        self.tagger.addTrack()
        self.tagger.check(addTrackButtonClicked)

    def testRemovesTrackFromAlbumWhenRemoveButtonIsClicked(self):
        self._addTrackToList(trackTitle="Track 0")
        self._addTrackToList(trackTitle="Track 1")
        self._addTrackToList(trackTitle="Track 2")

        trackRemoved = ValueMatcherProbe("remove track")

        class RemoveTrackProbe(object):
            def removeTrack(self, index):
                trackRemoved.setReceivedValue(index)

        self.trackList.setMusicProducer(RemoveTrackProbe())

        trackRemoved.expects(has_property('trackTitle', 'Track 1'))
        self.tagger.removeTrackAt(1)
        self.tagger.hasTrackCount(2)
        self.tagger.showsTrack("Track 0")
        self.tagger.showsTrack("Track 2")
        self.tagger.check(trackRemoved)

        trackRemoved.expects(has_property('trackTitle', 'Track 0'))
        self.tagger.removeTrackAt(0)
        self.tagger.hasTrackCount(1)
        self.tagger.showsTrack("Track 2")
        self.tagger.check(trackRemoved)

        trackRemoved.expects(has_property('trackTitle', 'Track 2'))
        self.tagger.removeTrackAt(0)
        self.tagger.hasTrackCount(0)
        self.tagger.check(trackRemoved)

    def testStopsCurrentlyPlayingTrackWhenRemovedFromList(self):
        self._addTrackToList()
        self._addTrackToList()

        self.tagger.playTrack(1)
        self.player.should_call('stop').never()
        self.tagger.removeTrackAt(0)
        self.player.should_call('stop').once()
        self.tagger.removeTrackAt(0)

    def testAccountsForRemovedTracksWhenReceivingMediaUpdates(self):
        track0 = self._addTrackToList(trackTitle="Track 0")
        track1 = self._addTrackToList(trackTitle="Track 1")

        self.tagger.playTrack(1)
        self.tagger.removeTrackAt(0)
        self.tagger.isPlayingTrack(0)
        self.trackList.mediaStopped(track1)
        self.tagger.isNotPlayingTrack(0)

        self.tagger.playTrack(0)
        self.tagger.removeTrackAt(0)
        # Should be silently ignored
        self.trackList.mediaStopped(track0)

    def _addTrackToList(self, **details):
        track = doubles.track(**details)
        self.trackList.trackAdded(track)
        return track

    def _notPlayingMusic(self):
        return lambda: not self.player.isPlaying()

    def _playingMusic(self):
        return lambda: self.player.isPlaying()

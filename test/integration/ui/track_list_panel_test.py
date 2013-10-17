# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock
from hamcrest import equal_to, has_property, contains
from hamcrest.library.collection.is_empty import empty

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe, AssertionProbe
from test.drivers.track_list_panel_driver import TrackListPanelDriver
from test.util import doubles
from test.util.fake_media_player import FakeMediaPlayer

from tgit.album import Album
from tgit.track import Track
from tgit.ui.track_list_panel import TrackListPanel


def hasTitle(title):
    return has_property('trackTitle', title)


class TrackListPanelTest(BaseWidgetTest):
    def setUp(self):
        super(TrackListPanelTest, self).setUp()
        self.player = flexmock(FakeMediaPlayer())
        self.album = Album()
        self.trackListPanel = TrackListPanel(self.album, self.player)
        self.view(self.trackListPanel)
        self.tagger = self.createDriverFor(self.trackListPanel)

    def createDriverFor(self, widget):
        return TrackListPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.tagger.showsColumnHeaders(
            'Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration', '', '')

    def testDisplaysTrackDetailsInColumns(self):
        self.addTrackToAlbum(trackTitle='Banana Song',
                             leadPerformer='Tim, Stuart, Dave',
                             releaseName='Despicable Me',
                             bitrate=192000,
                             duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.tagger.showsTrack('Banana Song', 'Tim, Stuart, Dave', 'Despicable Me',
                               '192 kbps', '03:43')

    def testDisplaysAllTracksInRows(self):
        self.addTrackToAlbum(trackTitle='Track 0')
        self.addTrackToAlbum(trackTitle='Track 1')

        self.tagger.hasTrackCount(2)
        # todo test also that tracks are in order
        self.tagger.showsTrack('Track 0')
        self.tagger.showsTrack('Track 1')

    def testCanPlayAndStopATrack(self):
        track = self.addTrackToAlbum()

        self.player.should_call('play').once().with_args(track).when(self._notPlayingMusic())
        self.player.should_call('stop').once().when(self._playingMusic())

        self.tagger.isNotPlayingTrack(0)
        self.tagger.clickPlayButton(0)
        self.tagger.isPlayingTrack(0)
        self.tagger.clickPlayButton(0)
        self.tagger.isNotPlayingTrack(0)

    def testRestoresListenButtonStateWhenTrackHasFinishedPlaying(self):
        track0 = self.addTrackToAlbum()
        track1 = self.addTrackToAlbum()

        self.tagger.playTrack(0)
        self.trackListPanel.mediaStopped(track0)
        self.tagger.isNotPlayingTrack(0)

        self.tagger.playTrack(1)
        self.trackListPanel.mediaPaused(track1)
        self.tagger.isNotPlayingTrack(1)

    def testTriggersSelectTrackWhenAddButtonIsClicked(self):
        addTrackButtonClicked = ValueMatcherProbe("add track button", equal_to("clicked"))

        class SelectTrackProbe(object):
            def selectTrack(self):
                addTrackButtonClicked.setReceivedValue("clicked")

        self.trackListPanel.addRequestListener(SelectTrackProbe())
        self.tagger.addTrack()
        self.tagger.check(addTrackButtonClicked)

    def testRemovesTrackFromAlbumWhenRemoveButtonIsClicked(self):
        self.addTrackToAlbum(trackTitle='Track 0')
        self.addTrackToAlbum(trackTitle='Track 1')
        self.addTrackToAlbum(trackTitle='Track 2')

        self.tagger.removeTrack('Track 1')
        self.tagger.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 0'), hasTitle('Track 2'))),
            'album'))
        self.tagger.hasTrackCount(2)
        self.tagger.showsTrack('Track 0')
        self.tagger.showsTrack('Track 2')

        self.tagger.removeTrack('Track 0')
        self.tagger.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 2'))), 'album'))
        self.tagger.hasTrackCount(1)
        self.tagger.showsTrack('Track 2')

        self.tagger.removeTrack('Track 2')
        self.tagger.check(AssertionProbe(self.album, has_property('tracks', empty()), 'album'))
        self.tagger.hasTrackCount(0)

    def testStopsCurrentlyPlayingTrackWhenRemovedFromList(self):
        self.addTrackToAlbum()
        self.addTrackToAlbum()

        self.tagger.playTrack(1)
        self.player.should_call('stop').never()
        self.tagger.removeTrackAt(0)
        self.player.should_call('stop').once()
        self.tagger.removeTrackAt(0)

    def testAccountsForRemovedTracksWhenReceivingMediaUpdates(self):
        track0 = self.addTrackToAlbum(trackTitle="Track 0")
        track1 = self.addTrackToAlbum(trackTitle="Track 1")

        self.tagger.playTrack(1)
        self.tagger.removeTrackAt(0)
        self.tagger.isPlayingTrack(0)
        self.trackListPanel.mediaStopped(track1)
        self.tagger.isNotPlayingTrack(0)

        self.tagger.playTrack(0)
        self.tagger.removeTrackAt(0)
        # Should be silently ignored
        self.trackListPanel.mediaStopped(track0)

    def testChangesTrackPositionInAlbumWhenTrackIsMoved(self):
        self.addTrackToAlbum(trackTitle="Track 0")
        self.addTrackToAlbum(trackTitle="Track 1")
        self.addTrackToAlbum(trackTitle="Track 2")

        self.tagger.changeTrackPosition(2, 1)
        self.tagger.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 0'),
                                                        hasTitle('Track 2'),
                                                        hasTitle('Track 1'))), 'album'))
        self.tagger.hasTrackCount(3)
        self.tagger.removeTrackAt(2)
        self.tagger.showsTrack("Track 2")

        self.tagger.changeTrackPosition(1, 0)
        self.tagger.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 2'),
                                                        hasTitle('Track 0'))), 'album'))
        self.tagger.hasTrackCount(2)
        self.tagger.removeTrackAt(1)
        self.tagger.showsTrack("Track 2")

    def addTrackToAlbum(self, **details):
        track = doubles.track(**details)
        self.album.addTrack(track)
        return track

    def _notPlayingMusic(self):
        return lambda: not self.player.isPlaying()

    def _playingMusic(self):
        return lambda: self.player.isPlaying()

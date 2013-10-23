# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock
from hamcrest import equal_to, has_property, contains
from hamcrest.library.collection.is_empty import empty

from test.integration.ui.base_widget_test import BaseWidgetTest

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe, AssertionProbe
from test.drivers.track_list_page_driver import TrackListPageDriver
from test.util import builders

from tgit.album import Album
from tgit.player import SilentPlayer
from tgit.ui.track_list_page import TrackListPage
from tgit.ui.track_selector import TrackSelector


def hasTitle(title):
    return has_property('trackTitle', title)


class TrackSelectorStub(TrackSelector):
    def selectTrack(self):
        self._signalTrackSelected(self.selectedTrack)


class TrackListPageTest(BaseWidgetTest):

    def setUp(self):
        super(TrackListPageTest, self).setUp()
        self.player = flexmock(SilentPlayer())
        self.album = Album()
        self.trackSelector = TrackSelectorStub()
        self.widget = TrackListPage(self.album, self.player, self.trackSelector)
        self.view(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TrackListPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders(
            'Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration', '', '')

    def testDisplaysTrackDetailsInColumns(self):
        self.addTrackToAlbum(trackTitle='Banana Song',
                             bitrate=192000,
                             duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.album.releaseName = 'Despicable Me'
        self.album.leadPerformer = 'Tim, Stuart, Dave'
        self.widget.albumStateChanged(self.album)
        self.driver.showsTrack('Banana Song', 'Tim, Stuart, Dave', 'Despicable Me',
                               '192 kbps', '03:43')

    def testShowsUpToDateTrackInformation(self):
        track = self.addTrackToAlbum(trackTitle='')
        track.trackTitle = 'Banana Song'
        self.widget.trackStateChanged(track)
        self.driver.showsTrack('Banana Song')

    def testDisplaysAllTracksInRows(self):
        self.addTrackToAlbum(trackTitle='Track 0')
        self.addTrackToAlbum(trackTitle='Track 1')

        self.driver.hasTrackCount(2)
        # todo test also that tracks are in order
        self.driver.showsTrack('Track 0')
        self.driver.showsTrack('Track 1')

    def testCanPlayAndStopATrack(self):
        track = self.addTrackToAlbum()

        self.player.should_call('play').once().with_args(track).when(self._notPlayingMusic())
        self.player.should_call('stop').once().when(self._playingMusic())

        self.driver.isNotPlayingTrack(0)
        self.driver.clickPlayButton(0)
        self.driver.isPlayingTrack(0)
        self.driver.clickPlayButton(0)
        self.driver.isNotPlayingTrack(0)

    def testRestoresListenButtonStateWhenTrackHasFinishedPlaying(self):
        track0 = self.addTrackToAlbum()
        track1 = self.addTrackToAlbum()

        self.driver.playTrack(0)
        self.widget.mediaStopped(track0)
        self.driver.isNotPlayingTrack(0)

        self.driver.playTrack(1)
        self.widget.mediaPaused(track1)
        self.driver.isNotPlayingTrack(1)

    def testSelectsTrackAndSignalsImportTrackRequestWhenAddTrackButtonIsClicked(self):
        self.trackSelector.selectedTrack = 'track.mp3'

        importTrackRequest = ValueMatcherProbe('request to import track',
                                               equal_to(self.trackSelector.selectedTrack))

        class ImportTrackListener(object):
            def importTrack(self, filename):
                importTrackRequest.received(filename)

        self.widget.addRequestListener(ImportTrackListener())
        self.driver.addTrack()
        self.driver.check(importTrackRequest)

    def testRemovesTrackFromAlbumWhenRemoveButtonIsClicked(self):
        self.addTrackToAlbum(trackTitle='Track 0')
        self.addTrackToAlbum(trackTitle='Track 1')
        self.addTrackToAlbum(trackTitle='Track 2')

        self.driver.removeTrack('Track 1')
        self.driver.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 0'), hasTitle('Track 2'))),
            'album'))
        self.driver.hasTrackCount(2)
        self.driver.showsTrack('Track 0')
        self.driver.showsTrack('Track 2')

        self.driver.removeTrack('Track 0')
        self.driver.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 2'))), 'album'))
        self.driver.hasTrackCount(1)
        self.driver.showsTrack('Track 2')

        self.driver.removeTrack('Track 2')
        self.driver.check(AssertionProbe(self.album, has_property('tracks', empty()), 'album'))
        self.driver.hasTrackCount(0)

    def testStopsCurrentlyPlayingTrackWhenRemovedFromList(self):
        self.addTrackToAlbum()
        self.addTrackToAlbum()

        self.driver.playTrack(1)
        self.player.should_call('stop').never()
        self.driver.removeTrackAt(0)
        self.player.should_call('stop').once()
        self.driver.removeTrackAt(0)

    def testAccountsForRemovedTracksWhenReceivingMediaUpdates(self):
        track0 = self.addTrackToAlbum(trackTitle="Track 0")
        track1 = self.addTrackToAlbum(trackTitle="Track 1")

        self.driver.playTrack(1)
        self.driver.removeTrackAt(0)
        self.driver.isPlayingTrack(0)
        self.widget.mediaStopped(track1)
        self.driver.isNotPlayingTrack(0)

        self.driver.playTrack(0)
        self.driver.removeTrackAt(0)
        # Should be silently ignored
        self.widget.mediaStopped(track0)

    def testChangesTrackPositionInAlbumWhenTrackIsMoved(self):
        self.addTrackToAlbum(trackTitle="Track 0")
        self.addTrackToAlbum(trackTitle="Track 1")
        self.addTrackToAlbum(trackTitle="Track 2")

        self.driver.changeTrackPosition(2, 1)
        self.driver.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 0'),
                                                        hasTitle('Track 2'),
                                                        hasTitle('Track 1'))), 'album'))
        self.driver.hasTrackCount(3)
        self.driver.removeTrackAt(2)
        self.driver.showsTrack("Track 2")

        self.driver.changeTrackPosition(1, 0)
        self.driver.check(AssertionProbe(
            self.album, has_property('tracks', contains(hasTitle('Track 2'),
                                                        hasTitle('Track 0'))), 'album'))
        self.driver.hasTrackCount(2)
        self.driver.removeTrackAt(1)
        self.driver.showsTrack("Track 2")

    def addTrackToAlbum(self, **details):
        track = builders.track(**details)
        self.album.addTrack(track)
        return track

    def _notPlayingMusic(self):
        return lambda: not self.player.isPlaying()

    def _playingMusic(self):
        return lambda: self.player.isPlaying()

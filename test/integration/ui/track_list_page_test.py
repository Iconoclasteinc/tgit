# -*- coding: utf-8 -*-

from datetime import timedelta

from flexmock import flexmock
from hamcrest import has_property, contains
from hamcrest.library.collection.is_empty import empty

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe, AssertionProbe
from test.drivers.track_list_page_driver import TrackListPageDriver
from test.util import builders as build
from test.util.fakes import FakeAudioPlayer

from tgit.album import Album
from tgit.ui.track_list_page import TrackListPage


def hasTitle(title):
    return has_property('trackTitle', title)


class TrackListPageTest(BaseWidgetTest):

    def setUp(self):
        super(TrackListPageTest, self).setUp()
        self.player = flexmock(FakeAudioPlayer())
        self.album = Album()
        self.widget = TrackListPage(self.album, self.player)
        self.view(self.widget)
        # so that all columns are displayed and buttons are created
        self.widget.resize(800, 600)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TrackListPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders(
            'Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration', '', '')

    def testTrackListIsInitiallyEmpty(self):
        self.driver.showsTracksInOrder()

    def testDisplaysTrackDetailsInColumns(self):
        self.album.addTrack(build.track(trackTitle='My Song',
                                        bitrate=192000,
                                        duration=timedelta(minutes=3, seconds=43).total_seconds()))
        self.album.releaseName = 'My Album'
        self.album.leadPerformer = 'My Artist'
        self.driver.showsTrack('My Song', 'My Artist', 'My Album', '192 kbps', '03:43')

    def testShowsUpToDateTrackInformation(self):
        track = build.track(trackTitle='')
        self.album.addTrack(track)
        track.trackTitle = 'Banana Song'
        self.driver.showsTrack('Banana Song')

    def testDisplaysAllTracksInRows(self):
        self.album.addTrack(build.track(trackTitle='First'))
        self.album.addTrack(build.track(trackTitle='Second'))

        self.driver.hasTrackCount(2)
        self.driver.showsTracksInOrder(['First'], ['Second'])

    def testCanPlayAndStopATrack(self):
        track = build.track(trackTitle='Song')
        self.album.addTrack(track)

        self.player.should_call('play').once().with_args(track).when(self._notPlaying())
        self.player.should_call('stop').once().when(self._playing())

        self.driver.isNotPlaying('Song')
        self.driver.playOrStop('Song')
        self.driver.isPlaying('Song')
        self.driver.playOrStop('Song')
        self.driver.isNotPlaying('Song')

    def testRestoresPlayButtonStateWhenTrackHasFinishedPlaying(self):
        first = build.track(trackTitle='Song #1')
        self.album.addTrack(first)
        second = build.track(trackTitle='Song #2')
        self.album.addTrack(second)

        self.driver.play('Song #1')
        self.player.stop()
        self.driver.isNotPlaying('Song #1')

        self.driver.play('Song #2')
        self.player.stop()
        self.driver.isNotPlaying('Song #2')

    def testSignalsSelectTrackRequestWhenAddTrackButtonIsClicked(self):
        selectTrackRequest = ValueMatcherProbe('select track')

        class RequestTracker(object):
            def selectTrack(self):
                selectTrackRequest.received()

        self.widget.addRequestListener(RequestTracker())
        self.driver.addTrack()
        self.driver.check(selectTrackRequest)

    def testRemovesTrackFromAlbumWhenRemoveButtonIsClicked(self):
        self.album.addTrack(build.track(trackTitle='Song #1'))
        self.album.addTrack(build.track(trackTitle='Song #2'))
        self.album.addTrack(build.track(trackTitle='Song #3'))

        self.driver.removeTrack('Song #2')
        self.driver.check(AssertionProbe(self.album.tracks,
                                         contains(hasTitle('Song #1'), hasTitle('Song #3')),
                                         'tracks'))
        self.driver.hasTrackCount(2)
        self.driver.showsTracksInOrder(['Song #1'], ['Song #3'])

        self.driver.removeTrack('Song #1')
        self.driver.check(AssertionProbe(self.album.tracks,
                                         contains(hasTitle('Song #3')), 'tracks'))
        self.driver.hasTrackCount(1)
        self.driver.showsTrack('Song #3')

        self.driver.removeTrack('Song #3')
        self.driver.check(AssertionProbe(self.album.tracks, empty(), 'tracks'))
        self.driver.hasTrackCount(0)

    def testStopsCurrentlyPlayingTrackWhenRemovedFromList(self):
        self.album.addTrack(build.track(trackTitle='Song #1'))
        self.album.addTrack(build.track(trackTitle='Song #2'))

        self.driver.play('Song #2')
        self.player.should_call('stop').never()
        self.driver.removeTrack('Song #1')
        self.player.should_call('stop').once()
        self.driver.removeTrack('Song #2')

    def testChangesTrackPositionInAlbumWhenTrackIsMoved(self):
        self.album.addTrack(build.track(trackTitle='Song #1'))
        self.album.addTrack(build.track(trackTitle='Song #2'))
        self.album.addTrack(build.track(trackTitle='Song #3'))

        self.driver.moveTrack('Song #3', 1)
        self.driver.hasTrackCount(3)
        self.driver.showsTracksInOrder(['Song #1'], ['Song #3'], ['Song #2'])
        self.driver.check(AssertionProbe(self.album.tracks,
                                         contains(hasTitle('Song #1'),
                                                  hasTitle('Song #3'),
                                                  hasTitle('Song #2')), 'tracks'))
        self.driver.removeTrack('Song #2')

        self.driver.moveTrack('Song #3', 0)
        self.driver.hasTrackCount(2)
        self.driver.showsTracksInOrder(['Song #3'], ['Song #1'])
        self.driver.check(AssertionProbe(self.album.tracks,
                                         contains(hasTitle('Song #3'),
                                                  hasTitle('Song #1')), 'tracks'))

    def _notPlaying(self):
        return lambda: not self.player.isPlaying()

    def _playing(self):
        return lambda: self.player.isPlaying()

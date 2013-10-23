# -*- coding: utf-8 -*-

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.tagging_screen_driver import TaggingScreenDriver
from test.util.builders import track

from tgit.album import Album
from tgit.player import SilentPlayer
from tgit.ui.tagging_screen import TaggingScreen
from tgit.ui.track_selector import TrackSelector


class TaggingScreenTest(BaseWidgetTest):

    def setUp(self):
        super(TaggingScreenTest, self).setUp()
        self.album = Album()
        self.widget = TaggingScreen(self.album, SilentPlayer(), TrackSelector())
        self.view(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TaggingScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testStartsOnTrackListPage(self):
        self.driver.isShowingTrackList()

    def testSignalsRecordAlbumRequestsWhenSaveButtonClicked(self):
        recordAlbumRequest = ValueMatcherProbe('record album request')

        class RequestTracker(object):
            def recordAlbum(self):
                recordAlbumRequest.received()

        self.widget.addRequestListener(RequestTracker())
        self.album.addTrack(track())
        self.driver.nextPage()
        self.driver.saveAlbum()
        self.driver.check(recordAlbumRequest)

    def testAddsTrackPagesInTrackAlbumOrder(self):
        self.albumContains(track(trackTitle='Track 1'),
                           track(trackTitle='Track 2'),
                           track(trackTitle='Track 3'))

        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Track 1')
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Track 2')
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Track 3')

    def testStaysOnCurrentPageWhenNewTrackImported(self):
        self.albumContains(track(trackTitle='Track 1'))
        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Track 1')

        self.album.addTrack(track(trackTitle='Track 2'))
        self.driver.showsTrackMetadata(trackTitle='Track 1')

    def testDisablesNextPageButtonOnLastPage(self):
        self.albumContains(track())
        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.hasDisabledNextPageButton()

        self.album.addTrack(track())
        self.driver.nextPage()
        self.driver.hasDisabledNextPageButton()

    def testDeletesCorrespondingPageWhenTrackRemovedFromAlbum(self):
        tracks = self.albumContains(track(trackTitle='Track 1'),
                                    track(trackTitle='Track 2'),
                                    track(trackTitle='Track 3'))

        self.album.removeTrack(tracks[1])
        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Track 1')
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Track 3')

        self.album.removeTrack(tracks[2])
        self.driver.showsTrackMetadata(trackTitle='Track 1')
        self.driver.hasDisabledNextPageButton()

        self.album.removeTrack(tracks[0])
        self.driver.isShowingAlbumMetadata()
        self.driver.hasDisabledNextPageButton()

    def testOffersBackAndForthNavigationBetweenPages(self):
        self.albumContains(track(), track())

        self.driver.nextPage()
        self.driver.isShowingAlbumMetadata()
        self.driver.nextPage()
        self.driver.isShowingTrackMetadata()
        self.driver.nextPage()
        self.driver.isShowingTrackMetadata()
        self.driver.previousPage()
        self.driver.isShowingTrackMetadata()
        self.driver.previousPage()
        self.driver.isShowingAlbumMetadata()
        self.driver.previousPage()
        self.driver.isShowingTrackList()
        self.driver.nextPage()
        self.driver.isShowingAlbumMetadata()

    def albumContains(self, *tracks):
        [self.album.addTrack(track) for track in tracks]
        return tracks

# -*- coding: utf-8 -*-

from hamcrest import assert_that, described_as, anything, has_properties, contains
from flexmock import flexmock

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util import builders
from test.util.fake_audio_library import FakeAudioLibrary

from tgit.album import Album
from tgit.producer import ProductionHouse, ProductionPortfolio, ArtisticDirector
from tgit.ui.main_window import MainWindow
from tgit.ui.track_selector import TrackSelector


class MainWindowTest(BaseWidgetTest):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        # todo remove
        self.album = Album()
        # todo remove
        self.director = ArtisticDirector()
        self.productions = ProductionPortfolio()
        self.mainWindow = MainWindow(self.productions)
        self.mainWindow.setTrackSelector(TrackSelector())
        self.view(self.mainWindow)
        self.tagger = self.createDriverFor(self.mainWindow)
        self.audioLibrary = FakeAudioLibrary()

    def tearDown(self):
        self.audioLibrary.delete()
        super(MainWindowTest, self).tearDown()

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testRelaysUsersRequestsToRegisteredListeners(self):
        productionHouse = flexmock(ProductionHouse())
        self.mainWindow.addProductionHouse(productionHouse)

        productionHouse.should_receive('newAlbum').once()
        self.mainWindow.newAlbum()

    def testShowsMainScreenWhenAlbumIsCreated(self):
        self.tagger.isShowingWelcomePanel()
        self.mainWindow.productionAdded(self.director, self.album)
        self.tagger.isShowingTrackList()

    # todo move following tests to main screen tests
    def testAddsTrackPagesInTrackAlbumOrder(self):
        first = builders.track(trackTitle='Track 1')
        second = builders.track(trackTitle='Track 2')
        third = builders.track(trackTitle='Track 3')

        self.mainWindow.productionAdded(self.director, self.album)
        self.album.addTrack(first)
        self.album.addTrack(third)
        self.album.addTrack(second, 1)

        self.tagger.nextPage()
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(trackTitle='Track 2')
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')

    def testCanNavigateBackAndForthBetweenPages(self):
        self.mainWindow.productionAdded(self.director, self.album)
        self.addTrackToAlbum()
        self.addTrackToAlbum()

        self.tagger.isShowingTrackList()
        self.tagger.nextPage()
        self.tagger.isShowingAlbumMetadata()
        self.tagger.nextPage()
        self.tagger.isShowingTrackMetadata()
        self.tagger.nextPage()
        self.tagger.isShowingTrackMetadata()
        self.tagger.previousPage()
        self.tagger.isShowingTrackMetadata()
        self.tagger.previousPage()
        self.tagger.isShowingAlbumMetadata()
        self.tagger.previousPage()
        self.tagger.isShowingTrackList()
        self.tagger.nextPage()
        self.tagger.isShowingAlbumMetadata()

    def testNextButtonIsDisabledOnLastTrack(self):
        self.mainWindow.productionAdded(self.director, self.album)
        self.addTrackToAlbum()
        self.tagger.nextPage()
        self.tagger.nextPage()
        self.tagger.hasNextStepDisabled()

        self.addTrackToAlbum()
        self.tagger.nextPage()
        self.tagger.hasNextStepDisabled()

    def testStaysOnCurrentPageWhenNewTrackIsImported(self):
        self.mainWindow.productionAdded(self.director, self.album)
        self.addTrackToAlbum(trackTitle='Track 1')
        self.tagger.nextPage()
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.addTrackToAlbum()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')

    def testRecordsWithAlbumAndTracksMetadata(self):
        recordAlbumRequest = ValueMatcherProbe('record album request', described_as('', anything()))

        class RecordAlbumTracker(object):
            def recordAlbum(self):
                recordAlbumRequest.setReceivedValue(True)

        self.mainWindow.productionAdded(RecordAlbumTracker(), self.album)
        self.addTrackToAlbum()
        self.addTrackToAlbum()
        self.addTrackToAlbum()

        self.tagger.nextPage()
        self.tagger.editAlbumMetadata(releaseName='Album')
        self.tagger.nextPage()
        self.tagger.editTrackMetadata(trackTitle='Track 1')
        self.tagger.nextPage()
        self.tagger.editTrackMetadata(trackTitle='Track 2')
        self.tagger.nextPage()
        self.tagger.editTrackMetadata(trackTitle='Track 3')
        self.tagger.saveAlbum()

        self.tagger.check(recordAlbumRequest)
        assert_that(self.album, has_properties(releaseName='Album'), 'album')
        assert_that(self.album.tracks, contains(
            has_properties(trackTitle='Track 1'),
            has_properties(trackTitle='Track 2'),
            has_properties(trackTitle='Track 3')), 'album tracks')

    def testDeletesCorrespondingPageWhenTrackIsRemovedFromAlbum(self):
        self.mainWindow.productionAdded(self.director, self.album)
        track1 = self.addTrackToAlbum(trackTitle="Track 1")
        track2 = self.addTrackToAlbum(trackTitle="Track 2")
        track3 = self.addTrackToAlbum(trackTitle="Track 3")

        self.removeTrack(track2)
        self.tagger.nextPage()
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(tracktle='Track 1')
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')
        # Tracks can only be removed from track list, so go back there
        # todo when we can navigate directly to the track list, change the navigation
        self.tagger.previousPage()
        self.tagger.previousPage()
        self.tagger.previousPage()
        self.removeTrack(track1)
        self.tagger.nextPage()
        self.tagger.nextPage()
        self.tagger.showsTrackMetadata(tracktle='Track 3')
        # Let's go back again to the track list
        self.tagger.previousPage()
        self.tagger.previousPage()
        self.removeTrack(track3)
        self.tagger.hasNextStepDisabled()

    # todo move to track list panel tests
    def testTrackListShowsUpToDateTrackAndAlbumMetadata(self):
        self.mainWindow.productionAdded(self.director, self.album)
        self.addTrackToAlbum()
        self.addTrackToAlbum()
        self.addTrackToAlbum()
        self.tagger.nextPage()
        self.tagger.editAlbumMetadata(releaseName='Album')
        self.tagger.nextPage()
        self.tagger.editTrackMetadata(trackTitle='Track 1')
        self.tagger.nextPage()
        self.tagger.editTrackMetadata(trackTitle='Track 2')
        self.tagger.nextPage()
        self.tagger.editTrackMetadata(trackTitle='Track 3')
        self.tagger.previousPage()
        self.tagger.previousPage()
        self.tagger.previousPage()
        self.tagger.previousPage()

        self.tagger.showsAlbumContains(['Track 1', 'Album'],
                                       ['Track 2', 'Album'],
                                       ['Track 3', 'Album'])

    def addTrackToAlbum(self, **details):
        track = builders.track(**details)
        self.album.addTrack(track)
        return track

    def removeTrack(self, track):
        self.album.removeTrack(track)
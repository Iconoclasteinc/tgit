# -*- coding: utf-8 -*-

from cute.finders import WidgetIdentity
from test.drivers import AlbumScreenDriver
from test.integration.ui import WidgetTest
from test.util import builders as build, doubles
from tgit.preferences import Preferences

from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.album_edition_page import AlbumEditionPage

from tgit.ui.album_screen import AlbumScreen
from tgit.ui.track_edition_page import TrackEditionPage


class AlbumScreenTest(WidgetTest):
    def setUp(self):
        super(AlbumScreenTest, self).setUp()
        self.album = build.album()
        self.view = AlbumScreen(AlbumCompositionPage(self.album, doubles.audio_player()), AlbumEditionPage(Preferences(), self.album),
                                self.createTrackEditionPage)
        self.show(self.view)
        self.driver = self.createDriverFor(self.view)

    def createTrackEditionPage(self, track):
        page = TrackEditionPage()
        page.display(self.album, track)
        return page

    def createDriverFor(self, widget):
        return AlbumScreenDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testIncludesHelpLinkInHeader(self):
        self.driver.linksHelpTo("http://tagyourmusic.com/#style-guide")

    def testIncludesFeatureRequestLinkInHeader(self):
        self.driver.linksFeatureRequestTo("mailto:iconoclastejr@gmail.com")

    def testInitiallyContainsOnlyAlbumCompositionAndEditionPages(self):
        self.driver.showsAlbumCompositionPage()
        self.driver.hidesPreviousPageButton()
        self.driver.nextPage()
        self.driver.showsAlbumEditionPage()
        self.driver.hidesNextPageButton()

    def testAddsTrackEditionPageForEachNewTrackInAlbum(self):
        self.album.addAlbumListener(self.view)
        self.album.addTrack(build.track(track_title="Bone Machine"))
        self.album.addTrack(build.track(track_title="Where is My Mind?"))
        self.album.addTrack(build.track(track_title="Cactus"))
        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Bone Machine")
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Where is My Mind?")
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Cactus")

    def testRemovesCorrespondingTrackPageWhenTrackRemovedFromAlbum(self):
        surfer_rosa = (
            build.track(track_title="Bone Machine"),
            build.track(track_title="Where is My Mind?"),
            build.track(track_title="Cactus")
        )

        self.album.addAlbumListener(self.view)

        for track in surfer_rosa:
            self.album.addTrack(track)

        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Bone Machine")
        self.album.removeTrack(surfer_rosa[0])
        self.driver.shows_track_metadata(track_title="Where is My Mind?")
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Cactus")
        self.album.removeTrack(surfer_rosa[2])
        self.driver.shows_track_metadata(track_title="Where is My Mind?")
        self.album.removeTrack(surfer_rosa[1])
        self.driver.showsAlbumEditionPage()

    def testOffersBackAndForthNavigationBetweenPages(self):
        self.album.addAlbumListener(self.view)
        self.album.addTrack(build.track())

        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.hidesNextPageButton()
        self.driver.previousPage()
        self.driver.previousPage()
        self.driver.hidesPreviousPageButton()
        self.driver.nextPage()
# -*- coding: utf-8 -*-

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import AlbumScreenDriver
from test.integration.ui import WidgetTest
from test.util import builders as build

from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.album_edition_page import AlbumEditionPage

from tgit.ui.album_screen import AlbumScreen
from tgit.ui.track_edition_page import TrackEditionPage


class AlbumScreenTest(WidgetTest):
    def setUp(self):
        super(AlbumScreenTest, self).setUp()
        self.album = build.album()
        self.view = AlbumScreen(AlbumCompositionPage(), AlbumEditionPage(self.album), self.createTrackEditionPage)
        self.show(self.view)
        self.driver = self.createDriverFor(self.view)

    def createTrackEditionPage(self, track):
        page = TrackEditionPage(self.album, track)
        page.display(self.album, track)
        return page

    def createDriverFor(self, widget):
        return AlbumScreenDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testIncludesHelpLinkInHeader(self):
        self.driver.linksHelpTo("http://tagtamusique.com/2013/12/03/tgit_style_guide/")

    def testIncludesFeatureRequestLinkInHeader(self):
        self.driver.linksFeatureRequestTo("mailto:iconoclastejr@gmail.com")

    def testInitiallyContainsOnlyAlbumCompositionAndEditionPages(self):
        self.driver.showsAlbumCompositionPage()
        self.driver.hidesPreviousPageButton()
        self.driver.hidesSaveButton()
        self.driver.nextPage()
        self.driver.showsAlbumEditionPage()
        self.driver.hidesNextPageButton()
        self.driver.hidesSaveButton()

    def testAddsTrackEditionPageForEachNewTrackInAlbum(self):
        self.album.addAlbumListener(self.view)
        self.album.addTrack(build.track(track_title='Bone Machine'))
        self.album.addTrack(build.track(track_title='Where is My Mind?'))
        self.album.addTrack(build.track(track_title='Cactus'))
        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title='Bone Machine')
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title='Where is My Mind?')
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title='Cactus')

    def testRemovesCorrespondingTrackPageWhenTrackRemovedFromAlbum(self):
        surferRosa = (
            build.track(track_title='Bone Machine'),
            build.track(track_title='Where is My Mind?'),
            build.track(track_title='Cactus')
        )

        self.album.addAlbumListener(self.view)

        for track in surferRosa:
            self.album.addTrack(track)

        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title='Bone Machine')
        self.album.removeTrack(surferRosa[0])
        self.driver.shows_track_metadata(track_title='Where is My Mind?')
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title='Cactus')
        self.album.removeTrack(surferRosa[2])
        self.driver.shows_track_metadata(track_title='Where is My Mind?')
        self.album.removeTrack(surferRosa[1])
        self.driver.showsAlbumEditionPage()
        self.driver.hidesSaveButton()

    def testSignalsWhenSaveButtonClicked(self):
        self.album.addAlbumListener(self.view)

        self.album.addTrack(build.track())
        saveAlbumSignal = ValueMatcherProbe('save album signal')
        self.view.recordAlbum.connect(saveAlbumSignal.received)

        self.driver.save()
        self.driver.check(saveAlbumSignal)

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
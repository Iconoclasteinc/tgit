# -*- coding: utf-8 -*-
from tgit.util import sip_api
sip_api.use_v2()

from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.album_screen_driver import AlbumScreenDriver
from test.integration.ui import ViewTest
from test.util import builders as build
from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.album_edition_page import AlbumEditionPage

from tgit.ui.album_screen import AlbumScreen
from tgit.ui.track_edition_page import TrackEditionPage


class AlbumScreenTest(ViewTest):
    def setUp(self):
        super(AlbumScreenTest, self).setUp()
        self.album = build.album()
        self.view = AlbumScreen(AlbumCompositionPage(), AlbumEditionPage(self.album), self.createTrackEditionPage)
        self.show(self.view)
        self.driver = self.createDriverFor(self.view)

    def createTrackEditionPage(self, track):
        page = TrackEditionPage(self.album, track)
        track.addTrackListener(page)
        page.display(self.album, track)
        return page

    def createDriverFor(self, widget):
        return AlbumScreenDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

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
        self.album.addTrack(build.track(trackTitle='Bone Machine'))
        self.album.addTrack(build.track(trackTitle='Where is My Mind?'))
        self.album.addTrack(build.track(trackTitle='Cactus'))
        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Bone Machine')
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Where is My Mind?')
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Cactus')

    def testRemovesCorrespondingTrackPageWhenTrackRemovedFromAlbum(self):
        surferRosa = (
            build.track(trackTitle='Bone Machine'),
            build.track(trackTitle='Where is My Mind?'),
            build.track(trackTitle='Cactus')
        )

        self.album.addAlbumListener(self.view)

        for track in surferRosa:
            self.album.addTrack(track)

        self.driver.nextPage()
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Bone Machine')
        self.album.removeTrack(surferRosa[0])
        self.driver.showsTrackMetadata(trackTitle='Where is My Mind?')
        self.driver.nextPage()
        self.driver.showsTrackMetadata(trackTitle='Cactus')
        self.album.removeTrack(surferRosa[2])
        self.driver.showsTrackMetadata(trackTitle='Where is My Mind?')
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
# -*- coding: utf-8 -*-
import pytest

from cute.finders import WidgetIdentity
from cute.probes import ValueMatcherProbe
from test.drivers import AlbumScreenDriver
from test.integration.ui import WidgetTest, show_widget
from test.util import builders as build, doubles
from tgit.preferences import Preferences

from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.album_edition_page import AlbumEditionPage

from tgit.ui.album_screen import AlbumScreen
from tgit.ui.track_edition_page import TrackEditionPage


@pytest.fixture()
def album():
    return build.album()


@pytest.fixture()
def track_edition_page_creator(album):
    def create_track_edition_page(track):
        page = TrackEditionPage()
        page.display(album, track)
        return page

    return create_track_edition_page


@pytest.yield_fixture()
def screen(qt, album, track_edition_page_creator):
    album_screen = AlbumScreen(AlbumCompositionPage(album, doubles.audio_player()),
                               AlbumEditionPage(Preferences(), album),
                               track_edition_page_creator)
    show_widget(album_screen)
    yield album_screen
    album_screen.close()


@pytest.yield_fixture()
def driver(screen, prober, automaton):
    album_screen_driver = AlbumScreenDriver(WidgetIdentity(screen), prober, automaton)
    yield album_screen_driver
    album_screen_driver.close()


def test_navigates_to_album_edition_page(screen, driver):
    screen.navigate_to_album_edition_page()
    driver.showsAlbumEditionPage()


def test_navigates_to_album_composition_page(screen, driver):
    screen.navigate_to_album_edition_page()
    screen.navigate_to_album_composition_page()
    driver.showsAlbumCompositionPage()


# todo change test_navigates_to_track_page to not register to the listener.
def test_navigates_to_track_page(screen, driver, album):
    album.addAlbumListener(screen)
    album.add_track(build.track(track_title="Chevere!"))
    album.add_track(build.track(track_title="Zumbar"))
    album.add_track(build.track(track_title="Salsa Coltrane"))

    screen.navigate_to_track_page(2)
    driver.shows_track_metadata(track_title="Zumbar")


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
        self.driver.hidesSaveButton()
        self.driver.nextPage()
        self.driver.showsAlbumEditionPage()
        self.driver.hidesNextPageButton()
        self.driver.hidesSaveButton()

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
        self.driver.hidesSaveButton()

    def testSignalsWhenSaveButtonClicked(self):
        self.album.addAlbumListener(self.view)

        self.album.addTrack(build.track())
        save_album_signal = ValueMatcherProbe("save album signal")
        self.view.record_album.connect(save_album_signal.received)

        self.driver.tag()
        self.driver.check(save_album_signal)

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
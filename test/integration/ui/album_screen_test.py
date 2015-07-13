# -*- coding: utf-8 -*-

import pytest

from cute.finders import WidgetIdentity
from cute.matchers import named
from cute.widgets import window
from test.drivers import AlbumScreenDriver
from test.drivers.fake_drivers import album_edition_page, track_list_page, track_edition_page, \
    no_album_edition_page, no_track_list_page, no_track_edition_page
from test.integration.ui import WidgetTest, show_widget
from test.integration.ui.fake_widgets import fake_track_list_page, fake_track_edition_page
from test.integration.ui.fake_widgets import fake_album_edition_page
from test.util import builders as build
from test.util.builders import make_track
from test.util.doubles import FakeAudioPlayer
from tgit.preferences import Preferences
from tgit.ui.track_list_page import TrackListPage
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.ui.album_screen import AlbumScreen
from tgit.ui.track_edition_page import TrackEditionPage


def ignore(*_):
    pass


@pytest.fixture()
def album_screen(qt):
    def create_screen(album):
        screen = AlbumScreen(fake_track_list_page(),
                             fake_album_edition_page(),
                             lambda track: fake_track_edition_page(track.track_number))

        # todo this should soon move to the screen itself
        album.addAlbumListener(screen)
        for index, track in enumerate(album.tracks):
            screen.trackAdded(track, index)

        show_widget(screen)
        return screen

    return create_screen


@pytest.yield_fixture()
def driver(prober, automaton):
    album_screen_driver = AlbumScreenDriver(window(AlbumScreen, named("album_screen")), prober, automaton)
    yield album_screen_driver
    album_screen_driver.close()


def test_jumps_to_album_edition_page(album_screen, driver):
    screen = album_screen(build.album())
    screen.show_album_edition_page()

    album_edition_page(driver).is_showing_on_screen()


def test_jumps_to_track_list_page(album_screen, driver):
    screen = album_screen(build.album())
    screen.show_album_edition_page()
    screen.show_track_list_page()

    track_list_page(driver).is_showing_on_screen()


def test_jumps_to_track_page(album_screen, driver):
    screen = album_screen(build.album(tracks=(build.track(), build.track(), build.track())))
    screen.show_track_page(2)

    track_edition_page(driver, number=2).is_showing_on_screen()


def test_closes_children_pages_on_close(album_screen, driver):
    screen = album_screen(build.album(tracks=(build.track(), build.track(), build.track())))

    track_list = track_list_page(driver).widget()
    album_page = album_edition_page(driver).widget()
    track_pages = [track_edition_page(driver, number + 1).widget() for number in range(3)]

    screen.close()

    no_track_list_page(driver).exists()
    track_list.is_closed()
    no_album_edition_page(driver).exists()
    album_page.is_closed()
    for number, track_page in enumerate(track_pages):
        no_track_edition_page(driver, number).exists()
        track_page.is_closed()


class AlbumScreenTest(WidgetTest):
    def setUp(self):
        super(AlbumScreenTest, self).setUp()
        self.album = build.album()
        self.view = AlbumScreen(TrackListPage(self.album, FakeAudioPlayer(), select_tracks=ignore),
                                AlbumEditionPage(Preferences(), self.album),
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

    def testInitiallyContainsOnlyTrackListAndEditionPages(self):
        self.driver.shows_track_list_page()
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

    def testMovesCorrespondingTrackPageWhenTrackPositionInAlbumChanges(self):
        self.album.addAlbumListener(self.view)
        self.album.track_moved.subscribe(self.view.track_moved)

        self.album.addTrack(make_track(track_title="Zumbar"))
        self.album.addTrack(make_track(track_title="Salsa Coltrane"))
        self.album.addTrack(make_track(track_title="Chevere!"))

        self.view.show_track_page(track_number=1)
        self.album.move_track(0, 2)

        self.driver.shows_track_metadata(track_title="Salsa Coltrane")
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Chevere!")
        self.driver.nextPage()
        self.driver.shows_track_metadata(track_title="Zumbar")
        self.driver.hidesNextPageButton()

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

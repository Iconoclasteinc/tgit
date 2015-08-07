# -*- coding: utf-8 -*-
from functools import wraps

from hamcrest import contains
import pytest

from cute.matchers import named, with_
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe
from cute.properties import name
from cute.widgets import window
from test.drivers import AlbumScreenDriver
from test.integration.ui import show_widget
from test.util import builders as build
from test.util.builders import make_track, make_album
from test.util.doubles import fake_audio_player
from tgit.preferences import Preferences
from tgit.ui import TrackEditionPage
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.ui.album_screen import AlbumScreen
from tgit.ui.track_list_page import TrackListPage

ignore = lambda *_: None


def create_track_list_page(album):
    return TrackListPage(album, fake_audio_player(), ignore)


def create_album_page(album):
    return AlbumEditionPage(Preferences(), ignore)


def create_track_page(track):
    page = TrackEditionPage()
    page.setObjectName("track_edition_page_" + str(track.track_number))
    return page


def number(track_number):
    return with_(name(), "track_edition_page_" + str(track_number))


def display_album_screen(album=None, list_tracks=create_track_list_page, edit_album=create_album_page,
                         edit_track=create_track_page):
    screen = AlbumScreen(list_tracks, edit_album, edit_track)
    show_widget(screen)
    if album is not None:
        screen.display(album)
    return screen


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    album_screen_driver = AlbumScreenDriver(window(AlbumScreen, named("album_screen")), prober, automaton)
    yield album_screen_driver
    album_screen_driver.close()


def test_is_initially_empty(driver):
    _ = display_album_screen()

    driver.has_no_track_list_page()
    driver.has_no_album_edition_page()
    driver.has_no_track_edition_page()
    driver.is_missing_previous_page_button()
    driver.is_missing_next_page_button()


def test_offers_goto_page_navigation(driver):
    screen = display_album_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_list_page()
    driver.shows_track_list_page()

    screen.to_album_edition_page()
    driver.shows_album_edition_page()

    screen.to_track_page(index=0)
    driver.shows_track_edition_page().is_(number(1))

    screen.to_track_page(index=1)
    driver.shows_track_edition_page().is_(number(2))

    screen.to_track_page(index=2)
    driver.shows_track_edition_page().is_(number(3))


def test_offers_back_and_forth_navigation_between_pages(driver):
    _ = display_album_screen(make_album(tracks=(make_track(), make_track())))

    driver.shows_track_list_page()

    driver.to_next_page()
    driver.shows_album_edition_page()

    driver.to_next_page()
    driver.shows_track_edition_page().is_(number(1))

    driver.to_next_page()
    driver.shows_track_edition_page().is_(number(2))
    driver.is_missing_next_page_button()

    driver.to_previous_page()
    driver.shows_track_edition_page().is_(number(1))

    driver.to_previous_page()
    driver.shows_album_edition_page()

    driver.to_previous_page()
    driver.shows_track_list_page()
    driver.is_missing_previous_page_button()

    driver.to_next_page()
    driver.shows_album_edition_page()


def test_lets_remove_track_pages(driver):
    screen = display_album_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_page(index=2)
    driver.shows_track_edition_page().is_(number(3))

    screen.remove_track_page(index=2)
    driver.shows_track_edition_page().is_(number(2))

    screen.to_track_page(index=0)
    driver.shows_track_edition_page().is_(number(1))

    screen.remove_track_page(index=0)
    driver.shows_track_edition_page().is_(number(2))


def test_lets_move_track_pages_around(driver):
    screen = display_album_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_page(index=0)
    driver.shows_track_edition_page().is_(number(1))

    screen.move_track_page(from_index=0, to_index=2)
    driver.shows_track_edition_page().is_(number(2))

    screen.to_track_page(index=1)
    driver.shows_track_edition_page().is_(number(3))

    screen.to_track_page(index=2)
    driver.shows_track_edition_page().is_(number(1))


def test_closes_children_pages_on_close(driver):
    closed_signals = MultiValueMatcherProbe("closed pages", contains(
        "track_edition_page_3",
        "track_edition_page_2",
        "track_edition_page_1",
        "album_edition_page",
        "track_list_page"))

    def record_close(create_page):
        @wraps(create_page)
        def wrapper(*args, **kwargs):
            page = create_page(*args, **kwargs)
            page.on_close(lambda: closed_signals.received(page.objectName()))
            return page

        return wrapper

    screen = display_album_screen(make_album(tracks=(make_track(), make_track(), make_track())),
                                  record_close(create_track_list_page),
                                  record_close(create_album_page),
                                  record_close(create_track_page))

    screen.close()

    driver.has_no_track_list_page()
    driver.has_no_album_edition_page()
    driver.has_no_track_edition_page()
    driver.check(closed_signals)
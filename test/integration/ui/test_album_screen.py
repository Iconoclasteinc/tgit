# -*- coding: utf-8 -*-
from functools import wraps

from hamcrest import contains
import pytest

from cute.matchers import named, with_
from cute.probes import MultiValueMatcherProbe
from cute.properties import name
from cute.widgets import window
from test.drivers import AlbumScreenDriver
from test.integration.ui import show_widget
from test.util.builders import make_track, make_album
from tgit.ui.track_edition_page import TrackEditionPage
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.ui.album_screen import AlbumScreen, make_album_screen
from tgit.ui.track_list_page import TrackListPage

ignore = lambda *_: None


def create_track_list_page(album):
    return TrackListPage(ignore)


def create_album_page(album):
    return AlbumEditionPage(ignore, ignore, ignore, ignore, ignore, ignore, ignore)


def create_track_page(track, review_assignation=ignore, show_isni_assignation_failed=ignore,
                      show_cheddar_connection_failed=ignore, show_cheddar_authentication_failed=ignore):
    page = TrackEditionPage(review_assignation, show_isni_assignation_failed, show_cheddar_connection_failed,
                            show_cheddar_authentication_failed)
    page.setObjectName("track_edition_page_" + str(track.track_number))
    return page


def number(track_number):
    return with_(name(), "track_edition_page_" + str(track_number))


def display_album_screen(album, list_tracks=create_track_list_page, edit_album=create_album_page,
                         edit_track=create_track_page):
    screen = make_album_screen(album, list_tracks, edit_album, edit_track)
    show_widget(screen)
    return screen


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    album_screen_driver = AlbumScreenDriver(window(AlbumScreen, named("album_screen")), prober, automaton)
    yield album_screen_driver
    album_screen_driver.close()


def test_has_no_track_edition_page_when_album_is_empty(driver):
    _ = display_album_screen(make_album())

    driver.shows_track_list_page()
    driver.has_no_track_edition_page()


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

    driver.is_missing_previous_page_button()

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


def test_removes_track_page_when_track_removed(driver):
    screen = display_album_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_page(index=2)
    driver.shows_track_edition_page().is_(number(3))

    screen.track_removed(index=2)
    driver.shows_track_edition_page().is_(number(2))

    screen.to_track_page(index=0)
    driver.shows_track_edition_page().is_(number(1))

    screen.track_removed(index=0)
    driver.shows_track_edition_page().is_(number(2))


def test_moves_track_page_when_track_moved(driver):
    screen = display_album_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_page(index=0)
    driver.shows_track_edition_page().is_(number(1))

    screen.track_moved(from_index=0, to_index=2)
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
            page.closed.connect(lambda: closed_signals.received(page.objectName()))
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

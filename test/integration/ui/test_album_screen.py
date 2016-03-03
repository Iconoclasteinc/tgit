# -*- coding: utf-8 -*-
from functools import wraps

import pytest
from hamcrest import contains

from cute.matchers import named
from cute.probes import MultiValueMatcherProbe
from cute.widgets import window
from test.drivers import AlbumScreenDriver
from test.integration.ui import show_widget
from test.util.builders import make_track, make_album
from tgit.ui.pages.album_edition_page import AlbumEditionPage
from tgit.ui.pages.album_screen import AlbumScreen, make_album_screen
from tgit.ui.pages.track_edition_page import make_track_edition_page
from tgit.ui.pages.track_list_page import TrackListPage

ignore = lambda *args, **kwargs: None


def create_track_list_page(album):
    return TrackListPage(ignore)


def create_project_page(album):
    return AlbumEditionPage(ignore, ignore, ignore, ignore, ignore, ignore, ignore)


def create_track_page(track):
    page = make_track_edition_page(album=make_album(), track=track,
                                   on_track_changed=ignore,
                                   review_assignation=ignore,
                                   show_isni_assignation_failed=ignore,
                                   show_cheddar_connection_failed=ignore,
                                   show_cheddar_authentication_failed=ignore)

    page.setObjectName("track_edition_page_" + str(track.track_number))

    return page


def display_project_screen(album, list_tracks=create_track_list_page, edit_album=create_project_page,
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
    _ = display_project_screen(make_album())

    driver.shows_track_list_page()
    driver.has_no_track_edition_page()


def test_offers_goto_page_navigation(driver):
    screen = display_project_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_list_page()
    driver.shows_track_list_page()

    screen.to_project_edition_page()
    driver.shows_project_edition_page()

    screen.to_track_page(index=0)
    driver.shows_track_edition_page(1)

    screen.to_track_page(index=1)
    driver.shows_track_edition_page(2)

    screen.to_track_page(index=2)
    driver.shows_track_edition_page(3)


def test_offers_back_and_forth_navigation_between_pages(driver):
    _ = display_project_screen(make_album(tracks=(make_track(), make_track())))

    driver.shows_previous_page_button(enabled=False)

    driver.to_next_page()
    driver.shows_project_edition_page()

    driver.to_next_page()
    driver.shows_track_edition_page(1)

    driver.to_next_page()
    driver.shows_track_edition_page(2)
    driver.shows_next_page_button(enabled=False)

    driver.to_previous_page()
    driver.shows_track_edition_page(1)

    driver.to_previous_page()
    driver.shows_project_edition_page()

    driver.to_previous_page()
    driver.shows_track_list_page()
    driver.shows_previous_page_button(enabled=False)

    driver.to_next_page()
    driver.shows_project_edition_page()


def test_removes_track_page_when_track_removed(driver):
    screen = display_project_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_page(index=2)
    driver.shows_track_edition_page(3)

    screen.track_removed(index=2)
    driver.shows_track_edition_page(2)

    screen.to_track_page(index=0)
    driver.shows_track_edition_page(1)

    screen.track_removed(index=0)
    driver.shows_track_edition_page(2)


def test_moves_track_page_when_track_moved(driver):
    screen = display_project_screen(make_album(tracks=(make_track(), make_track(), make_track())))

    screen.to_track_page(index=0)
    driver.shows_track_edition_page(1)

    screen.track_moved(from_index=0, to_index=2)
    driver.shows_track_edition_page(2)

    screen.to_track_page(index=1)
    driver.shows_track_edition_page(3)

    screen.to_track_page(index=2)
    driver.shows_track_edition_page(1)


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

    screen = display_project_screen(make_album(tracks=(make_track(), make_track(), make_track())),
                                    record_close(create_track_list_page),
                                    record_close(create_project_page),
                                    record_close(create_track_page))

    screen.close()

    driver.has_no_track_list_page()
    driver.has_no_project_edition_page()
    driver.has_no_track_edition_page()
    driver.check(closed_signals)


def test_displays_pages_in_navigation_combo(driver):
    tracks = [make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3")]
    _ = display_project_screen(make_album(tracks=tracks))

    driver.shows_pages_in_navigation_combo("Track list", "Project edition", "1 - track 1", "2 - track 2", "3 - track 3")


def test_navigates_using_the_combo_box(driver):
    tracks = [make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3")]
    _ = display_project_screen(make_album(tracks=tracks))

    driver.to_page("3 - track 3")
    driver.shows_track_edition_page(3)

    driver.to_page("2 - track 2")
    driver.shows_track_edition_page(2)

    driver.to_page("1 - track 1")
    driver.shows_track_edition_page(1)

    driver.to_page("Project edition")
    driver.shows_project_edition_page()

    driver.to_page("Track list")
    driver.shows_track_list_page()


def test_updates_the_displayed_page_when_navigating_using_the_arrows(driver):
    _ = display_project_screen(make_album(tracks=[make_track(track_title="track 1")]))

    driver.shows_page_in_navigation_combo("Track list")
    driver.to_next_page()
    driver.shows_page_in_navigation_combo("Project edition")
    driver.to_next_page()
    driver.shows_page_in_navigation_combo("1 - track 1")
    driver.to_previous_page()
    driver.shows_page_in_navigation_combo("Project edition")
    driver.to_previous_page()
    driver.shows_page_in_navigation_combo("Track list")


def test_updates_the_displayed_page_when_updating_track_title(driver):
    def update_track_metadata(**metadata):
        track.track_title = metadata["track_title"]

    def make_track_page(current_track):
        return make_track_edition_page(album, current_track,
                                       on_track_changed=update_track_metadata,
                                       review_assignation=ignore,
                                       show_isni_assignation_failed=ignore,
                                       show_cheddar_connection_failed=ignore,
                                       show_cheddar_authentication_failed=ignore)

    track = make_track(track_title="track 1")
    album = make_album(tracks=[track])
    _ = display_project_screen(album, edit_track=make_track_page)

    driver.to_next_page()
    driver.to_next_page()
    driver.shows_page_in_navigation_combo("1 - track 1")
    driver.change_track_title("Chevere!")
    driver.shows_page_in_navigation_combo("1 - Chevere!")

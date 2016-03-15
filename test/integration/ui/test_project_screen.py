from functools import wraps

import pytest
from hamcrest import contains

from cute.matchers import named
from cute.probes import MultiValueMatcherProbe
from cute.widgets import window
from test.drivers import ProjectScreenDriver
from test.integration.ui import show_widget, ignore
from test.util.builders import make_track, make_album
from tgit.ui.pages.project_edition_page import ProjectEditionPage
from tgit.ui.pages.project_screen import ProjectScreen, make_project_screen
from tgit.ui.pages.track_edition_page import make_track_edition_page
from tgit.ui.pages.track_list_tab import TrackListTab

pytestmark = pytest.mark.ui


def create_track_list_tab(_):
    return TrackListTab(ignore)


def create_project_page(album):
    return ProjectEditionPage(create_track_list_tab(album), ignore, ignore, ignore, ignore, ignore, ignore)


def create_track_page(track):
    page = make_track_edition_page(album=make_album(), track=track,
                                   on_track_changed=ignore,
                                   review_assignation=ignore,
                                   show_isni_assignation_failed=ignore,
                                   show_cheddar_connection_failed=ignore,
                                   show_cheddar_authentication_failed=ignore)

    page.setObjectName("track_edition_page_" + str(track.track_number))

    return page


def show_project_screen(page_driver, album, edit_album=create_project_page, edit_track=create_track_page):
    screen = make_project_screen(album, edit_album, edit_track)
    show_widget(page_driver, screen)
    return screen


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    screen_driver = ProjectScreenDriver(window(ProjectScreen, named("project_screen")), prober, automaton)
    yield screen_driver
    screen_driver.close()


def test_has_no_track_edition_page_when_album_is_empty(driver):
    _ = show_project_screen(driver, make_album())

    driver.shows_project_edition_page()
    driver.has_no_track_edition_page()


def test_offers_goto_page_navigation(driver):
    _ = show_project_screen(driver, make_album(tracks=(
        make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3"))))

    driver.to_page("Project edition")
    driver.shows_project_edition_page()

    driver.to_page("1 - track 1")
    driver.shows_track_edition_page(1)

    driver.to_page("2 - track 2")
    driver.shows_track_edition_page(2)

    driver.to_page("3 - track 3")
    driver.shows_track_edition_page(3)


def test_offers_back_and_forth_navigation_between_pages(driver):
    _ = show_project_screen(driver, make_album(tracks=(make_track(), make_track())))

    driver.shows_previous_page_button(enabled=False)
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
    driver.shows_previous_page_button(enabled=False)

    driver.to_next_page()
    driver.shows_track_edition_page(1)


def test_removes_track_page_when_track_removed(driver):
    album = make_album(tracks=(
        make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3")))
    _ = show_project_screen(driver, album)

    driver.to_page("1 - track 1")
    album.remove_track(position=1)
    driver.to_next_page()
    driver.shows_track_edition_page(number=3)


def test_moves_track_page_when_track_moved(driver):
    album = make_album(tracks=(
        make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3")))
    _ = show_project_screen(driver, album)

    driver.to_page("1 - track 1")
    driver.shows_track_edition_page(1)

    album.move_track(from_position=0, to_position=2)
    driver.shows_track_edition_page(2)

    driver.to_next_page()
    driver.shows_track_edition_page(3)

    driver.to_next_page()
    driver.shows_track_edition_page(1)


def test_closes_children_pages_on_close(driver):
    closed_signals = MultiValueMatcherProbe("closed pages", contains(
        "track_edition_page_3",
        "track_edition_page_2",
        "track_edition_page_1",
        "project_edition_page"))

    def record_close(create_page):
        @wraps(create_page)
        def wrapper(*args, **kwargs):
            page = create_page(*args, **kwargs)
            page.closed.connect(lambda: closed_signals.received(page.objectName()))
            return page

        return wrapper

    _ = show_project_screen(driver, make_album(tracks=(make_track(), make_track(), make_track())),
                            record_close(create_project_page),
                            record_close(create_track_page))

    driver.close()

    driver.has_no_project_edition_page()
    driver.has_no_track_edition_page()
    driver.check(closed_signals)


def test_displays_pages_in_navigation_combo(driver):
    tracks = [make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3")]
    _ = show_project_screen(driver, make_album(tracks=tracks))

    driver.shows_pages_in_navigation_combo("Project edition", "1 - track 1", "2 - track 2", "3 - track 3")


def test_navigates_using_the_combo_box(driver):
    tracks = [make_track(track_title="track 1"), make_track(track_title="track 2"), make_track(track_title="track 3")]
    _ = show_project_screen(driver, make_album(tracks=tracks))

    driver.to_page("3 - track 3")
    driver.shows_track_edition_page(3)

    driver.to_page("2 - track 2")
    driver.shows_track_edition_page(2)

    driver.to_page("1 - track 1")
    driver.shows_track_edition_page(1)

    driver.to_page("Project edition")
    driver.shows_project_edition_page()


def test_updates_the_displayed_page_when_navigating_using_the_arrows(driver):
    _ = show_project_screen(driver, make_album(tracks=[make_track(track_title="track 1")]))

    driver.shows_page_in_navigation_combo("Project edition")
    driver.to_next_page()
    driver.shows_page_in_navigation_combo("1 - track 1")
    driver.to_previous_page()
    driver.shows_page_in_navigation_combo("Project edition")


def test_updates_the_displayed_page_when_updating_track_title(driver):
    track = make_track(track_title="track 1")
    _ = show_project_screen(driver, make_album(tracks=[track]))

    driver.shows_pages_in_navigation_combo("Project edition", "1 - track 1")
    track.track_title = "Chevere!"
    driver.shows_pages_in_navigation_combo("Project edition", "1 - Chevere!")


def test_removes_track_menu_item_when_removing_a_track_from_the_project(driver):
    album = make_album(tracks=[(make_track(track_title="Chevere!")), (make_track(track_title="That is that"))])
    _ = show_project_screen(driver, album)

    driver.shows_pages_in_navigation_combo("Project edition", "1 - Chevere!", "2 - That is that")
    album.remove_track(0)
    driver.shows_pages_in_navigation_combo("Project edition", "1 - That is that")


def test_reorders_navigation_menu_when_moving_a_track(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="That is that")])
    _ = show_project_screen(driver, album)

    driver.shows_pages_in_navigation_combo("Project edition", "1 - Chevere!", "2 - That is that")
    album.move_track(from_position=0, to_position=1)
    driver.shows_pages_in_navigation_combo("Project edition", "1 - That is that", "2 - Chevere!")


def test_navigates_using_shortcut(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="That is that")])
    _ = show_project_screen(driver, album)

    driver.quick_navigate_to_page("2")
    driver.shows_track_edition_page(2)

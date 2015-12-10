# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains, assert_that, empty, contains_string
import pytest

from cute.matchers import with_text, named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import TrackListPageDriver
from test.integration.ui import show_widget
from test.util import doubles
from test.util.builders import make_album, make_track
from tgit.ui.pages.track_list_page import TrackListPage, make_track_list_page

ignore = lambda *_: None


def show_track_list(album, select_tracks=ignore):
    page = make_track_list_page(album, doubles.fake_audio_player(), select_tracks)
    show_widget(page)
    return page


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = TrackListPageDriver(window(TrackListPage, named("track_list_page")), prober, automaton)
    yield page_driver
    page_driver.close()


def test_displays_column_headings(driver):
    _ = show_track_list(make_album())
    driver.shows_column_headers('#', None, 'Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration')
    driver.has_track_count(0)


def test_displays_track_details_in_columns(driver):
    _ = show_track_list(make_album(release_name="Honeycomb",
                                   lead_performer=("Joel Miller",),
                                   tracks={make_track(track_title='Chevere!',
                                                      bitrate=192000,
                                                      duration=timedelta(minutes=4, seconds=12).total_seconds())}))

    driver.shows_track_details("1", "Chevere!", "Joel Miller", "Honeycomb", "192 kbps", "04:12")


def test_displays_all_tracks_in_rows(driver):
    _ = show_track_list(make_album(tracks=[make_track(track_title='Chevere!'),
                                           make_track(track_title='Honeycomb')]))

    driver.has_track_count(2)
    driver.shows_tracks_in_order(['1', 'Chevere!'],
                                 ['2', 'Honeycomb'])


def test_updates_track_list_when_album_metadata_change(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="Zumbar")])
    _ = show_track_list(album)

    album.release_name = "Honeycomb"

    driver.shows_tracks_in_order(['Chevere!', 'Honeycomb'], ['Zumbar', 'Honeycomb'])


def test_updates_track_row_when_track_metadata_change(driver):
    track = make_track()
    _ = show_track_list(make_album(tracks=[track]))

    track.track_title = "Chevere!"
    track.lead_performer = ("Joel Miller",)

    driver.shows_track_details("Chevere!", "Joel Miller")


def test_adds_row_to_table_when_track_added_to_album(driver):
    album = make_album()
    _ = show_track_list(album)

    album.add_track(make_track(track_title="Chevere!"))
    album.add_track(make_track(track_title="Zumbar!"))

    driver.has_track_count(2)
    driver.shows_tracks_in_order(["1", "Chevere!"], ["2", "Zumbar!"])


def test_removes_row_from_table_when_track_removed_from_album(driver):
    album = make_album(tracks=(make_track(track_title="Chevere!"),
                               make_track(track_title='Zumbar'),
                               make_track(track_title='Salsa Coltrane')))
    _ = show_track_list(album)

    driver.shows_tracks_in_order(['Chevere!'], ['Zumbar'], ['Salsa Coltrane'])
    album.remove_track(1)
    driver.shows_tracks_in_order(['Chevere!'], ['Salsa Coltrane'])
    album.remove_track(1)
    driver.shows_tracks_in_order(['Chevere!'])
    album.remove_track(0)
    driver.shows_tracks_in_order()


def test_unsubscribe_from_track_events_track_removed_from_album(driver):
    track = make_track()
    album = make_album(tracks=[track])
    _ = show_track_list(album)

    album.remove_track(0)

    assert_that(track.metadata_changed.subscribers, empty(), "track 'metadata changed' subscribers")


@pytest.mark.parametrize("using_shortcut", [False, True])
def test_makes_remove_track_request_when_remove_menu_item_selected(driver, using_shortcut):
    page = show_track_list(make_album(tracks=[make_track(), make_track(track_title="Chevere!")]))

    remove_request = ValueMatcherProbe("remove track request", 1)
    page.on_remove_track(remove_request.received)

    driver.remove_track("Chevere!", using_shortcut)
    driver.check(remove_request)


def test_makes_stop_track_request_when_remove_menu_item_selected_and_track_is_playing(driver):
    spain = make_track(track_title="Spain")
    stop_request = ValueMatcherProbe("stop track request")

    page = show_track_list(make_album(type="mp3", tracks=[spain]))
    page.on_stop_track(stop_request.received)

    page.playback_started(spain)
    driver.remove_track("Spain")
    driver.check(stop_request)


def test_makes_play_track_request_when_play_context_menu_item_selected(driver):
    page = show_track_list(make_album(type='mp3', tracks=[make_track(track_title="Spain")]))

    play_request = ValueMatcherProbe("play track request", has_title("Spain"))
    page.on_play_track(play_request.received)

    driver.play_track('Spain')
    driver.check(play_request)


def test_makes_stop_track_request_when_stop_context_menu_item_selected(driver):
    spain = make_track(track_title="Spain")
    stop_request = ValueMatcherProbe("stop track request")

    page = show_track_list(make_album(type='mp3', tracks=[spain]))
    page.on_stop_track(stop_request.received)

    page.playback_started(spain)
    driver.stop_track('Spain')
    driver.check(stop_request)


def test_shows_selected_track_title_in_context_menu(driver):
    show_track_list(make_album(tracks=[make_track(track_title="Partways"),
                                       make_track(track_title="Rebop")]))

    driver.select_track("Partways")
    driver.has_context_menu_item(with_text(contains_string("Partways")))
    driver.select_track("Rebop")
    driver.has_context_menu_item(with_text(contains_string("Rebop")))


def test_changes_play_context_menu_item_depending_on_playback_state(driver):
    track = make_track(track_title="Choices")
    page = show_track_list(make_album(tracks=[track]))

    driver.select_track("Choices")
    driver.has_context_menu_item(with_text('Play "Choices"'))
    page.playback_started(track)
    driver.has_context_menu_item(with_text('Stop "Choices"'))
    page.playback_stopped(track)
    driver.has_context_menu_item(with_text('Play "Choices"'))


def test_makes_add_tracks_request_when_add_button_clicked(driver):
    album = make_album()
    page = show_track_list(album, select_tracks=lambda on_select: on_select("track1", "track2", "track3"))

    add_tracks_signal = ValueMatcherProbe("add tracks", contains("track1", "track2", "track3"))
    page.on_add_tracks(lambda *track_files: add_tracks_signal.received(track_files))

    driver.add_tracks()
    driver.check(add_tracks_signal)


def test_makes_move_track_requests_when_track_row_moved(driver):
    page = show_track_list(make_album(tracks=[make_track(track_title='Chaconne'),
                                              make_track(track_title='Choices'),
                                              make_track(track_title='Place St-Henri')]))

    track_moved_signal = ValueMatcherProbe('track moved', contains(2, 1))
    page.on_move_track(lambda track, to_position: track_moved_signal.received((track, to_position)))

    driver.move_track('Place St-Henri', 1)
    driver.check(track_moved_signal)


def test_moves_row_when_track_changes_position(driver):
    tracks = (make_track(track_title="Chevere!"),
              make_track(track_title='Zumbar'),
              make_track(track_title='Salsa Coltrane'))
    album = make_album(tracks=tracks)
    _ = show_track_list(album)

    driver.shows_tracks_in_order(['Chevere!'], ['Zumbar'], ['Salsa Coltrane'])
    album.move_track(2, 1)
    driver.shows_tracks_in_order(['Chevere!'], ['Salsa Coltrane'], ["Zumbar"])


def test_unsubscribes_from_event_signals_on_close(driver):
    track = make_track()
    page = show_track_list(make_album(tracks=[track]))

    page.close()
    assert_that(track.metadata_changed.subscribers, empty(), "'track metadata changed' subscriptions")


def has_title(title):
    return has_property('track_title', title)

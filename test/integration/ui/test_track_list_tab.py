# -*- coding: utf-8 -*-

from datetime import timedelta

import pytest
from hamcrest import has_property, contains, assert_that, empty, contains_string

from cute.matchers import with_text, named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe
from cute.widgets import window
from test.drivers import TrackListTabDriver
from test.integration.ui import show_widget
from test.util import doubles
from test.util.builders import make_album, make_track
from tgit.ui.pages.track_list_tab import TrackListTab, make_track_list_tab

ignore = lambda *_: None


def show_track_list_tab(album, select_tracks=ignore):
    page = make_track_list_tab(album, doubles.fake_audio_player(), select_tracks)
    show_widget(page)
    return page


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    tab_driver = TrackListTabDriver(window(TrackListTab, named("track_list_tab")), prober, automaton)
    yield tab_driver
    tab_driver.close()


def test_displays_column_headings(driver):
    _ = show_track_list_tab(make_album())
    driver.shows_column_headers("#", None, "Track Title", "Lead Performer", "Release Name", "Bitrate", "Duration")
    driver.has_track_count(0)


def test_displays_track_details_in_columns(driver):
    _ = show_track_list_tab(make_album(release_name="Honeycomb",
                                       lead_performer="Joel Miller",
                                       tracks=[make_track(track_title="Chevere!",
                                                          bitrate=192000,
                                                          duration=timedelta(minutes=4, seconds=12).total_seconds())]))

    driver.shows_track_details("1", "Chevere!", "Joel Miller", "Honeycomb", "192 kbps", "04:12")


def test_displays_all_tracks_in_rows(driver):
    _ = show_track_list_tab(make_album(tracks=[make_track(track_title="Chevere!"),
                                               make_track(track_title="Honeycomb")]))

    driver.has_track_count(2)
    driver.shows_tracks_in_order(["1", "Chevere!"],
                                 ["2", "Honeycomb"])


def test_updates_track_list_when_album_metadata_change(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!"), make_track(track_title="Zumbar")])
    _ = show_track_list_tab(album)

    album.release_name = "Honeycomb"

    driver.shows_tracks_in_order(["Chevere!", "Honeycomb"], ["Zumbar", "Honeycomb"])


def test_updates_track_row_when_track_metadata_change(driver):
    track = make_track()
    _ = show_track_list_tab(make_album(tracks=[track]))

    track.track_title = "Chevere!"
    track.lead_performer = "Joel Miller"

    driver.shows_track_details("Chevere!", "Joel Miller")


def test_adds_row_to_table_when_track_added_to_album(driver):
    album = make_album()
    _ = show_track_list_tab(album)

    album.add_track(make_track(track_title="Chevere!"))
    album.add_track(make_track(track_title="Zumbar!"))

    driver.has_track_count(2)
    driver.shows_tracks_in_order(["1", "Chevere!"], ["2", "Zumbar!"])


def test_removes_row_from_table_when_track_removed_from_album(driver):
    album = make_album(tracks=(make_track(track_title="Chevere!"),
                               make_track(track_title="Zumbar"),
                               make_track(track_title="Salsa Coltrane")))
    _ = show_track_list_tab(album)

    driver.shows_tracks_in_order(["Chevere!"], ["Zumbar"], ["Salsa Coltrane"])
    album.remove_track(1)
    driver.shows_tracks_in_order(["Chevere!"], ["Salsa Coltrane"])
    album.remove_track(1)
    driver.shows_tracks_in_order(["Chevere!"])
    album.remove_track(0)
    driver.shows_tracks_in_order()


def test_unsubscribe_from_track_events_track_removed_from_album(driver):
    track = make_track()
    album = make_album(tracks=[track])
    _ = show_track_list_tab(album)

    album.remove_track(0)

    assert_that(track.metadata_changed.subscribers, empty(), "track 'metadata changed' subscribers")


@pytest.mark.parametrize("using", ["menu", "shortcut", "button"])
def test_makes_remove_track_request_with_selected_track_when_track_removed(driver, using):
    page = show_track_list_tab(make_album(tracks=[make_track(), make_track(track_title="Chevere!")]))

    remove_request = ValueMatcherProbe("remove track request", 1)
    page.on_remove_track(remove_request.received)

    driver.select_track("Chevere!")
    driver.remove_selected_track(using=using)
    driver.check(remove_request)


def test_disables_remove_button_when_no_track_selected(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!")])
    _ = show_track_list_tab(album)

    driver.remove_button.is_disabled()
    driver.select_track("Chevere!")
    driver.remove_button.is_enabled()

    album.remove_track(position=0)
    driver.remove_button.is_disabled()


def test_disables_remove_shortcut_when_table_does_not_have_focus(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!")])
    _ = show_track_list_tab(album)

    driver.remove_selected_track(using="shortcut")
    driver.shows_tracks_in_order(["Chevere!"])


def test_makes_stop_track_request_when_remove_menu_item_selected_and_track_is_playing(driver):
    spain = make_track(track_title="Spain")
    stop_request = ValueMatcherProbe("stop track request")

    page = show_track_list_tab(make_album(type="mp3", tracks=[spain]))
    page.on_stop_track(stop_request.received)

    page.playback_started(spain)
    driver.remove_track("Spain")
    driver.check(stop_request)


def test_makes_play_track_request_when_play_context_menu_item_selected(driver):
    page = show_track_list_tab(make_album(type="mp3", tracks=[make_track(track_title="Spain")]))

    play_request = ValueMatcherProbe("play track request", has_title("Spain"))
    page.on_play_track(play_request.received)

    driver.play_track("Spain")
    driver.check(play_request)


def test_makes_stop_track_request_when_stop_context_menu_item_selected(driver):
    spain = make_track(track_title="Spain")
    stop_request = ValueMatcherProbe("stop track request")

    page = show_track_list_tab(make_album(type="mp3", tracks=[spain]))
    page.on_stop_track(stop_request.received)

    page.playback_started(spain)
    driver.stop_track("Spain")
    driver.check(stop_request)


def test_shows_selected_track_title_in_context_menu(driver):
    _ = show_track_list_tab(make_album(tracks=[make_track(track_title="Partways"),
                                               make_track(track_title="Rebop")]))

    driver.select_track("Partways")
    driver.has_context_menu_item(with_text(contains_string("Partways")))
    driver.select_track("Rebop")
    driver.has_context_menu_item(with_text(contains_string("Rebop")))


def test_updates_context_menu_item_when_playback_state_changes(driver):
    track = make_track(track_title="Choices")
    page = show_track_list_tab(make_album(tracks=[track]))

    driver.select_track("Choices")
    driver.has_context_menu_item(with_text('Play "Choices"'))
    page.playback_started(track)
    driver.has_context_menu_item(with_text('Stop "Choices"'))
    page.playback_stopped(track)
    driver.has_context_menu_item(with_text('Play "Choices"'))


def test_makes_add_tracks_request_when_add_button_clicked(driver):
    album = make_album()
    page = show_track_list_tab(album, select_tracks=lambda on_select: on_select("track1", "track2", "track3"))

    add_tracks_signal = ValueMatcherProbe("add tracks", contains("track1", "track2", "track3"))
    page.on_add_tracks(lambda *track_files: add_tracks_signal.received(track_files))

    driver.add_tracks()
    driver.check(add_tracks_signal)


def test_makes_move_track_request_when_track_row_moved(driver):
    page = show_track_list_tab(make_album(tracks=[make_track(track_title="Chaconne"),
                                                  make_track(track_title="Choices"),
                                                  make_track(track_title="Place St-Henri")]))

    track_moved_signal = MultiValueMatcherProbe("track moved", contains(2, 1))
    page.on_move_track(track_moved_signal.received)

    driver.move_track("Place St-Henri", 1)
    driver.check(track_moved_signal)


def test_makes_move_track_request_when_track_moved_up(driver):
    page = show_track_list_tab(make_album(tracks=[make_track(track_title="Chaconne"),
                                                  make_track(track_title="Choices")]))

    track_moved_signal = MultiValueMatcherProbe("track moved", contains(1, 0))
    page.on_move_track(track_moved_signal.received)

    driver.select_track("Choices")
    driver.move_track_up()
    driver.check(track_moved_signal)


def test_disables_move_up_button_when_on_first_track_or_no_track_selected(driver):
    _ = show_track_list_tab(make_album(tracks=[make_track(track_title="Chaconne"), make_track(track_title="Choices")]))

    driver.move_up_button.is_disabled()

    driver.select_track("Choices")
    driver.move_up_button.is_enabled()

    driver.select_track("Chaconne")
    driver.move_up_button.is_disabled()


def test_makes_move_track_request_when_track_moved_down(driver):
    page = show_track_list_tab(make_album(tracks=[make_track(track_title="Chaconne"),
                                                  make_track(track_title="Choices")]))

    track_moved_signal = MultiValueMatcherProbe("track moved", contains(0, 1))
    page.on_move_track(track_moved_signal.received)

    driver.select_track("Chaconne")
    driver.move_track_down()
    driver.check(track_moved_signal)


def test_disables_move_down_button_when_on_last_track_or_no_track_selected(driver):
    _ = show_track_list_tab(make_album(tracks=[make_track(track_title="Chaconne"), make_track(track_title="Choices")]))

    driver.move_down_button.is_disabled()

    driver.select_track("Chaconne")
    driver.move_down_button.is_enabled()

    driver.select_track("Choices")
    driver.move_down_button.is_disabled()


def test_moves_and_select_row_in_table_accordingly_when_track_position_changes(driver):
    tracks = (make_track(track_title="Chevere!"),
              make_track(track_title="Zumbar"),
              make_track(track_title="Salsa Coltrane"))
    album = make_album(tracks=tracks)
    _ = show_track_list_tab(album)

    driver.shows_tracks_in_order(["Chevere!"], ["Zumbar"], ["Salsa Coltrane"])
    driver.select_track("Salsa Coltrane")
    album.move_track(2, 1)
    driver.shows_tracks_in_order(["Chevere!"], ["Salsa Coltrane"], ["Zumbar"])
    driver.has_selected_track("Salsa Coltrane")


def test_unsubscribes_from_event_signals_on_close(driver):
    track = make_track()
    page = show_track_list_tab(make_album(tracks=[track]))

    page.close()
    assert_that(track.metadata_changed.subscribers, empty(), "'track metadata changed' subscriptions")


def has_title(title):
    return has_property("track_title", title)

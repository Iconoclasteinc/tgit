# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains, assert_that, empty
import pytest

from cute.matchers import with_text, named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import TrackListPageDriver
from test.integration.ui import show_widget
from test.util import builders as build
from test.util.builders import make_album, make_track
from test.util.doubles import fake_audio_player
from tgit.ui.track_list_page import TrackListPage


ignore = lambda *_: None


def show_page(album=make_album(), player=fake_audio_player(), select_tracks=ignore):
    track_list_page = TrackListPage(album, player, select_tracks)
    show_widget(track_list_page)
    return track_list_page


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = TrackListPageDriver(window(TrackListPage, named("track_list_page")), prober, automaton)
    yield page_driver
    page_driver.close()


def test_displays_column_headings(driver):
    show_page()
    driver.shows_column_headers('#', None, 'Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration')
    driver.has_track_count(0)


def test_displays_track_details_in_columns(driver):
    show_page(make_album(release_name='Honeycomb',
                         lead_performer='Joel Miller',
                         tracks=[make_track(track_title='Chevere!',
                                            bitrate=192000,
                                            duration=timedelta(minutes=4, seconds=12).total_seconds())]))

    driver.shows_track_details('1', None, 'Chevere!', 'Joel Miller', 'Honeycomb', '192 kbps', '04:12')


def test_displays_all_tracks_in_rows(driver):
    show_page(make_album(tracks=[make_track(track_title='Give Life Back To Music'),
                                 make_track(track_title='Get Lucky')]))

    driver.has_track_count(2)
    driver.shows_tracks_in_order(['1', 'Give Life Back To Music'], ['2', 'Get Lucky'])


def test_updates_entire_table_when_album_metadata_change(driver):
    album = make_album(tracks=[make_track(track_title="Chevere!"), build.track(track_title='Zumbar')])
    show_page(album)

    album.release_name = 'Honeycomb'

    driver.shows_tracks_in_order(['Chevere!', 'Honeycomb'], ['Zumbar', 'Honeycomb'])


def test_updates_track_row_when_track_metadata_change(driver):
    track = make_track()
    show_page(make_album(tracks=[track]))

    track.track_title = "Chevere!"
    track.lead_performer = 'Joel Miller'

    driver.shows_track_details('Chevere!', 'Joel Miller')


def test_adds_row_to_table_when_track_added_to_album(driver):
    album = make_album()
    show_page(album)
    album.add_track(make_track(track_title="Chevere!"))

    driver.has_track_count(1)
    driver.shows_tracks_in_order(["1", "Chevere!"])


def test_removes_row_from_table_when_track_removed_from_album(driver):
    tracks = (make_track(track_title="Chevere!"),
              make_track(track_title='Zumbar'),
              make_track(track_title='Salsa Coltrane'))
    album = make_album(tracks=tracks)
    show_page(album)

    driver.shows_tracks_in_order(['Chevere!'], ['Zumbar'], ['Salsa Coltrane'])
    album.remove_track(tracks[1])
    driver.shows_tracks_in_order(['Chevere!'], ['Salsa Coltrane'])
    album.remove_track(tracks[2])
    driver.shows_tracks_in_order(['Chevere!'])
    album.remove_track(tracks[0])
    driver.shows_tracks_in_order()

    for index, track in enumerate(tracks):
        assert_that(track.metadata_changed.subscribers, empty(),
                    "track #{} 'metadata changed' subscribers".format(index))


def test_signals_user_request_to_remove_track(driver):
    page = show_page(make_album(tracks=[make_track(), make_track(track_title="Chevere!")]))

    remove_track_signal = ValueMatcherProbe("remove track", has_title("Chevere!"))
    page.on_remove_track(remove_track_signal.received)

    driver.remove_track('Chevere!')
    driver.check(remove_track_signal)


def test_can_remove_track_using_keyboard_shortcut(driver):
    page = show_page(make_album(tracks=[make_track(track_title="Chevere!")]))

    remove_track_signal = ValueMatcherProbe("remove track", has_title("Chevere!"))
    page.on_remove_track(remove_track_signal.received)

    driver.remove_track('Chevere!', using_shortcut=True)
    driver.check(remove_track_signal)


def test_signals_user_playback_request(driver):
    page = show_page(make_album(type='mp3', tracks=[make_track(track_title="Spain")]))

    playback_signal = ValueMatcherProbe("play track", has_title("Spain"))
    page.on_play_track(playback_signal.received)

    driver.play_track('Spain')
    driver.check(playback_signal)


def test_prevents_playing_flac_files(driver):
    show_page(make_album(type='flac', tracks=[make_track(track_title="Spain")]))

    driver.cannot_play_track('Spain')


def test_shows_title_of_track_to_play_in_context_menu(driver):
    show_page(make_album(tracks=[make_track(track_title="Partways")]))

    driver.select_track("Partways")
    driver.has_context_menu_item(with_text('Play "Partways"'))


def test_changes_context_menu_text_to_stop_when_selected_track_is_playing(driver):
    player = fake_audio_player()
    track = make_track(track_title="Choices")
    show_page(make_album(tracks=[track]), player)

    player.play(track)

    driver.select_track("Choices")
    driver.has_context_menu_item(with_text('Stop "Choices"'))


def test_signals_when_add_tracks_button_clicked(driver):
    album = make_album()
    page = show_page(album, select_tracks=lambda on_select: on_select("track1", "track2", "track3"))

    add_tracks_signal = ValueMatcherProbe("add tracks", contains("track1", "track2", "track3"))
    page.on_add_tracks(lambda *track_files: add_tracks_signal.received(track_files))

    driver.add_tracks()
    driver.check(add_tracks_signal)


def test_signals_when_track_was_moved(driver):
    page = show_page(make_album(tracks=[make_track(track_title='Chaconne'),
                                        make_track(track_title='Choices'),
                                        make_track(track_title='Place St-Henri')]))

    new_position = 1
    track_moved_signal = ValueMatcherProbe('track moved', contains(has_title('Place St-Henri'), new_position))
    page.on_move_track(lambda track, to_position: track_moved_signal.received((track, to_position)))

    driver.move_track('Place St-Henri', new_position)
    driver.check(track_moved_signal)


def test_unsubscribes_from_event_signals_on_close(driver):
    album = make_album()
    player = fake_audio_player()

    page = show_page(album, player)
    page.close()

    assert_that(album.track_inserted.subscribers, empty(), "'track inserted' subscriptions")
    assert_that(player.playing.subscribers, empty(), "'player playing' subscriptions")
    assert_that(player.stopped.subscribers, empty(), "'player stopped' subscriptions")


def has_title(title):
    return has_property('track_title', title)

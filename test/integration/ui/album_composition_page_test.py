# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains, assert_that, empty
import pytest

from cute.finders import WidgetIdentity
from cute.matchers import with_text
from cute.probes import ValueMatcherProbe
from test.integration.ui import WidgetTest
from test.drivers import AlbumCompositionPageDriver
from test.util import builders as build, doubles
from tgit.album import Album
from tgit.ui.album_composition_page import AlbumCompositionPage


@pytest.fixture
def player():
    return doubles.audio_player()


@pytest.fixture
def album():
    return build.album()


@pytest.fixture()
def page(main_window, album, player):
    composition_page = AlbumCompositionPage(album, player)
    main_window.setCentralWidget(composition_page)
    return composition_page


@pytest.yield_fixture()
def driver(page, prober, automaton):
    page_driver = AlbumCompositionPageDriver(WidgetIdentity(page, 'under test'), prober, automaton)
    yield page_driver
    page_driver.close()


def test_displays_column_headings(driver):
    driver.shows_column_headers('Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration')


def test_displays_track_details_in_columns(album, driver):
    album.release_name = 'Honeycomb'
    album.lead_performer = 'Joel Miller'
    album.add_track(build.track(track_title='Chevere!',
                               bitrate=192000,
                               duration=timedelta(minutes=4, seconds=12).total_seconds()))

    driver.shows_track_details('Chevere!', 'Joel Miller', 'Honeycomb', '192 kbps', '04:12')


def test_displays_all_tracks_in_rows(album, driver):
    album.add_track(build.track(track_title='Give Life Back To Music'))
    album.add_track(build.track(track_title='Get Lucky'))

    driver.has_track_count(2)
    driver.shows_tracks_in_order(['Give Life Back To Music'], ['Get Lucky'])


def test_updates_track_list_when_album_metadata_change(album, driver):
    album.add_track(build.track(track_title="Chevere!"))
    album.add_track(build.track(track_title='Zumbar'))

    album.release_name = 'Honeycomb'

    driver.shows_tracks_in_order(['Chevere!', 'Honeycomb'], ['Zumbar', 'Honeycomb'])


def test_updates_track_row_when_track_metadata_change(album, driver):
    track = build.track()
    album.add_track(track)

    track.track_title = "Chevere!"
    track.lead_performer = 'Joel Miller'

    driver.shows_track_details('Chevere!', 'Joel Miller')


def test_removes_row_from_table_when_track_removed_from_album(album, driver):
    tracks = [build.track(track_title="Chevere!"),
              build.track(track_title='Zumbar'),
              build.track(track_title='Salsa Coltrane')]

    for track in tracks:
        album.add_track(track)

    driver.shows_tracks_in_order(['Chevere!'], ['Zumbar'], ['Salsa Coltrane'])
    album.remove_track(tracks[1])
    driver.shows_tracks_in_order(['Chevere!'], ['Salsa Coltrane'])
    album.remove_track(tracks[2])
    driver.shows_tracks_in_order(['Chevere!'])
    album.remove_track(tracks[0])
    driver.shows_tracks_in_order()

    for index, track in enumerate(tracks):
        assert_that(track.metadata_changed.subscribers, empty(), "track #{} 'metadata changed' subscribers".format(index))


def test_signals_user_request_to_remove_track(album, page, driver):
    page.display(album)
    album.add_track(build.track())
    album.add_track(build.track(track_title="Chevere!"))

    remove_track_signal = ValueMatcherProbe("remove track", has_title("Chevere!"))
    page.remove_track.connect(remove_track_signal.received)

    driver.remove_track('Chevere!')
    driver.check(remove_track_signal)


def test_can_remove_track_using_keyboard_shortcut(album, page, driver):
    page.display(album)
    album.add_track(build.track(track_title="Chevere!"))

    remove_track_signal = ValueMatcherProbe("remove track", has_title("Chevere!"))
    page.remove_track.connect(remove_track_signal.received)

    driver.remove_track('Chevere!', using_shortcut=True)
    driver.check(remove_track_signal)


def test_signals_user_request_to_play_or_stop_track(album, page, driver):
    album.type = 'mp3'
    album.add_track(build.track(track_title="Spain"))

    play_track_signal = ValueMatcherProbe("play track", has_title("Spain"))
    page.play_track.connect(play_track_signal.received)

    driver.play_track('Spain')
    driver.check(play_track_signal)


def test_prevents_playing_flac_files(album, driver):
    album.type = 'flac'
    album.add_track(build.track(track_title="Spain"))

    driver.cannot_play_track('Spain')


def test_shows_title_of_track_to_play_in_context_menu(album, driver):
    album.add_track(build.track(track_title="Partways"))

    driver.select_track("Partways")
    driver.has_context_menu_item(with_text('Play "Partways"'))


def test_changes_context_menu_option_to_stop_when_selected_track_is_playing(album, player, driver):
    track = build.track(track_title="Choices")
    album.add_track(track)

    player.play(track)

    driver.select_track("Choices")
    driver.has_context_menu_item(with_text('Stop "Choices"'))


@pytest.mark.xfail(reason="fails probably because we're moving rows programmatically?")
def test_selected_row_follows_reorders(page, driver):
    album = build.album()
    page.display(album)

    album.addTrack(build.track(track_title='Chaconne'))
    album.addTrack(build.track(track_title='Choices'))
    album.addTrack(build.track(track_title='Place St-Henri'))

    driver.move_track_in_bottom_table('Choices', 2)
    driver.has_selected_track('Choices')


def test_signals_when_add_tracks_button_clicked(page, driver):
    add_tracks_signal = ValueMatcherProbe('add tracks')
    page.add_tracks.connect(add_tracks_signal.received)

    driver.add_tracks()
    driver.check(add_tracks_signal)


def test_unsubscribes_from_event_signals_on_close(album, player, page):
    page.close()

    assert_that(album.track_inserted.subscribers, empty(), "'track inserted' subscriptions")
    assert_that(player.playing.subscribers, empty(), "'player playing' subscriptions")
    assert_that(player.stopped.subscribers, empty(), "'player stopped' subscriptions")


def has_title(title):
    return has_property('track_title', title)


class AlbumCompositionPageTest(WidgetTest):
    def setUp(self):
        super(AlbumCompositionPageTest, self).setUp()
        self.page = AlbumCompositionPage(build.album(), doubles.audio_player())
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)
        self.album = build.album()
        self.page.display(self.album)

    def createDriverFor(self, widget):
        return AlbumCompositionPageDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testSignalsWhenTrackWasMoved(self):
        self.album.addTrack(build.track(track_title='Wisemen'))
        self.album.addTrack(build.track(track_title='1973'))
        self.album.addTrack(build.track(track_title='Tears and Rain'))

        newPosition = 1
        trackMovedSignal = ValueMatcherProbe('track moved', contains(has_title('Tears and Rain'), newPosition))
        self.page.move_track.connect(lambda track, to: trackMovedSignal.received([track, newPosition]))

        self.driver.move_track_in_bottom_table('Tears and Rain', newPosition)
        self.driver.check(trackMovedSignal)
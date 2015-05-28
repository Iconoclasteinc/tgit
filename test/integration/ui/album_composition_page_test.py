# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains, assert_that, empty
import pytest

from cute.finders import WidgetIdentity
from cute.matchers import with_text
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from test.integration.ui import WidgetTest, show_widget
from test.drivers import AlbumCompositionPageDriver
from test.util import builders as build, doubles
from tgit.album import Album
from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.main_window import MainWindow


@pytest.fixture
def player():
    return doubles.audio_player()


@pytest.yield_fixture()
def page(qt, player):
    main_window = MainWindow()
    composition_page = AlbumCompositionPage(player)
    main_window.setCentralWidget(composition_page)
    show_widget(main_window)
    yield composition_page
    main_window.close()


@pytest.yield_fixture()
def driver(page):
    page_driver = AlbumCompositionPageDriver(WidgetIdentity(page), EventProcessingProber(), Robot())
    yield page_driver
    page_driver.close()


def test_signals_user_request_to_remove_track(page, driver):
    album = build.album()
    page.display(album)
    # todo for the moment, we need to add tracks to the album to trigger an update of the table
    album.addTrack(build.track())
    album.addTrack(build.track(track_title="Chevere!"))

    remove_track_signal = ValueMatcherProbe("remove track", hasTitle("Chevere!"))
    page.remove_track.connect(remove_track_signal.received)

    driver.remove_track('Chevere!')
    driver.check(remove_track_signal)


def test_signals_user_request_to_play_or_stop_track(page, driver):
    album = build.album(of_type=Album.Type.MP3)
    page.display(album)
    album.addTrack(build.track(track_title="Spain"))

    play_track_signal = ValueMatcherProbe("play track", hasTitle("Spain"))
    page.play_track.connect(play_track_signal.received)

    driver.play_track('Spain')
    driver.check(play_track_signal)


def test_prevents_playing_flac_files(page, driver):
    album = build.album(of_type=Album.Type.FLAC)
    page.display(album)
    album.addTrack(build.track(track_title="Spain"))

    driver.cannot_play_track('Spain')


def test_displays_track_title_to_play_in_context_menu(page, driver):
    album = build.album()
    page.display(album)
    album.addTrack(build.track(track_title="Partways"))

    driver.select_track("Partways")
    driver.has_context_menu_item(with_text('Play "Partways"'))


def test_displays_stop_in_context_menu_when_selected_track_is_playing(player, page, driver):
    album = build.album()
    page.display(album)

    track = build.track(track_title="Choices")
    album.addTrack(track)

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

    driver.move_track('Choices', 2)
    driver.has_selected_track('Choices')


def test_unsubscribes_from_event_signals_on_close(player, page):
    page.close()

    assert_that(player.playing.subscribers, empty(), "'player playing' subscriptions")
    assert_that(player.stopped.subscribers, empty(), "'player stopped' subscriptions")


# todo find a home for feature matchers
def hasTitle(title):
    return has_property('track_title', title)


class AlbumCompositionPageTest(WidgetTest):
    def setUp(self):
        super(AlbumCompositionPageTest, self).setUp()
        self.page = AlbumCompositionPage(doubles.audio_player())
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)
        self.album = build.album()
        self.page.display(self.album)

    def createDriverFor(self, widget):
        return AlbumCompositionPageDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders('Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration')

    def testDisplaysTrackDetailsInColumns(self):
        self.album.release_name = 'All the Little Lights'
        self.album.lead_performer = 'Passenger'
        self.album.addTrack(build.track(track_title='Let Her Go',
                                        bitrate=192000,
                                        duration=timedelta(minutes=4, seconds=12).total_seconds()))

        self.driver.shows_track('Let Her Go', 'Passenger', 'All the Little Lights', '192 kbps', '04:12')

    def testDisplaysAllTracksInRows(self):
        self.album.addTrack(build.track(track_title='Give Life Back To Music'))
        self.album.addTrack(build.track(track_title='Get Lucky'))
        self.driver.hasTrackCount(2)
        self.driver.showsTracksInOrder(['Give Life Back To Music'], ['Get Lucky'])

    def testSignalsWhenAddTracksButtonClicked(self):
        addTracksSignal = ValueMatcherProbe('add tracks')
        self.page.addTracks.connect(addTracksSignal.received)

        self.driver.add_tracks()
        self.driver.check(addTracksSignal)

    def testSignalsWhenTrackWasMoved(self):
        self.album.addTrack(build.track(track_title='Wisemen'))
        self.album.addTrack(build.track(track_title='1973'))
        self.album.addTrack(build.track(track_title='Tears and Rain'))

        newPosition = 1
        trackMovedSignal = ValueMatcherProbe('track moved', contains(hasTitle('Tears and Rain'), newPosition))
        self.page.move_track.connect(lambda track, to: trackMovedSignal.received([track, newPosition]))

        self.driver.move_track('Tears and Rain', newPosition)
        self.driver.check(trackMovedSignal)
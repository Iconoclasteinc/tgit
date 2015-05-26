# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains
from pytest import yield_fixture

from cute.finders import WidgetIdentity
from cute.prober import EventProcessingProber
from cute.probes import ValueMatcherProbe
from cute.robot import Robot
from test.integration.ui import WidgetTest, show_widget
from test.drivers import AlbumCompositionPageDriver
from test.util import builders as build, doubles
from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.main_window import MainWindow


@yield_fixture()
def page(qt):
    main_window = MainWindow()
    composition_page = AlbumCompositionPage()
    main_window.setCentralWidget(composition_page)
    show_widget(main_window)
    yield composition_page
    main_window.close()


@yield_fixture()
def driver(page):
    page_driver = AlbumCompositionPageDriver(WidgetIdentity(page), EventProcessingProber(), Robot())
    yield page_driver
    page_driver.close()


def test_signals_when_track_selected_for_removal(page, driver):
    album = build.album()
    page.display(doubles.null_audio_player(), album)
    # todo for the moment, we need to add tracks to the album to trigger an update of the table
    album.addTrack(build.track())
    album.addTrack(build.track(track_title='Chevere!'))

    remove_track_signal = ValueMatcherProbe('remove track', hasTitle('Chevere!'))
    page.remove_track.connect(remove_track_signal.received)

    driver.remove_track('Chevere!')
    driver.check(remove_track_signal)


# todo find a home for feature matchers
def hasTitle(title):
    return has_property('track_title', title)


class AlbumCompositionPageTest(WidgetTest):
    def setUp(self):
        super(AlbumCompositionPageTest, self).setUp()
        self.page = AlbumCompositionPage()
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)
        self.album = build.album()
        self.page.display(doubles.null_audio_player(), self.album)

    def createDriverFor(self, widget):
        return AlbumCompositionPageDriver(WidgetIdentity(widget), self.prober, self.gesture_performer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders('Track Title', 'Lead Performer', 'Release Name', 'Bitrate', 'Duration', '')

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

    def testSignalsWhenPlayTrackButtonClicked(self):
        self.album.addTrack(build.track(track_title='Happy'))
        playTrackSignal = ValueMatcherProbe('play track', hasTitle('Happy'))
        self.page.playTrack.connect(playTrackSignal.received)

        self.driver.play('Happy')
        self.driver.check(playTrackSignal)

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
        self.page.trackMoved.connect(lambda track, to: trackMovedSignal.received([track, newPosition]))

        self.driver.move_track('Tears and Rain', newPosition)
        self.driver.check(trackMovedSignal)

    def test_disables_playback_for_unsupported_audio_tracks(self):
        self.album.addTrack(build.track(filename="track.mp3", track_title="mp3 file"))
        self.album.addTrack(build.track(filename="track.flac", track_title="flac file"))

        self.driver.enables_playback_of("mp3 file")
        self.driver.disables_playback_of("flac file")
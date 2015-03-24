# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains

from test.integration.ui import WidgetTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.album_composition_page_driver import AlbumCompositionPageDriver
from test.util import builders as build, doubles
from tgit.ui.album_composition_page import AlbumCompositionPage


# todo find a home for feature matchers
def hasTitle(title):
    return has_property('trackTitle', title)


class AlbumCompositionPageTest(WidgetTest):
    def setUp(self):
        super(AlbumCompositionPageTest, self).setUp()
        self.page = AlbumCompositionPage()
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)
        self.album = build.album()
        self.page.display(doubles.audioPlayer(), self.album)

    def createDriverFor(self, widget):
        return AlbumCompositionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders('Track Title', 'Lead Performer', 'Album Title', 'Bitrate', 'Duration', '', '')

    def testDisplaysTrackDetailsInColumns(self):
        self.album.releaseName = 'All the Little Lights'
        self.album.addTrack(build.track(trackTitle='Let Her Go',
                                        leadPerformer='Passenger',
                                        bitrate=192000,
                                        duration=timedelta(minutes=4, seconds=12).total_seconds()))

        self.driver.showsTrack('Let Her Go', 'Passenger', 'All the Little Lights', '192 kbps', '04:12')

    def testDisplaysAllTracksInRows(self):
        self.album.addTrack(build.track(trackTitle='Give Life Back To Music'))
        self.album.addTrack(build.track(trackTitle='Get Lucky'))
        self.driver.hasTrackCount(2)
        self.driver.showsTracksInOrder(['Give Life Back To Music'], ['Get Lucky'])

    def testSignalsWhenPlayTrackButtonClicked(self):
        self.album.addTrack(build.track(trackTitle='Happy'))
        playTrackSignal = ValueMatcherProbe('play track', hasTitle('Happy'))
        self.page.playTrack.connect(playTrackSignal.received)

        self.driver.play('Happy')
        self.driver.check(playTrackSignal)

    def testSignalsWhenAddTracksButtonClicked(self):
        addTracksSignal = ValueMatcherProbe('add tracks')
        self.page.addTracks.connect(addTracksSignal.received)

        self.driver.addTracks()
        self.driver.check(addTracksSignal)

    def testSignalsWhenRemoveTrackButtonClicked(self):
        self.album.addTrack(build.track())
        self.album.addTrack(build.track(trackTitle='Set Fire to the Rain'))
        removeTrackSignal = ValueMatcherProbe('remove track', hasTitle('Set Fire to the Rain'))
        self.page.removeTrack.connect(removeTrackSignal.received)

        self.driver.removeTrack('Set Fire to the Rain')
        self.driver.check(removeTrackSignal)

    def testSignalsWhenTrackWasMoved(self):
        self.album.addTrack(build.track(trackTitle='Wisemen'))
        self.album.addTrack(build.track(trackTitle='1973'))
        self.album.addTrack(build.track(trackTitle='Tears and Rain'))

        newPosition = 1
        trackMovedSignal = ValueMatcherProbe('track moved', contains(hasTitle('Tears and Rain'), newPosition))
        self.page.trackMoved.connect(lambda track, to: trackMovedSignal.received([track, newPosition]))

        self.driver.moveTrack('Tears and Rain', newPosition)
        self.driver.check(trackMovedSignal)
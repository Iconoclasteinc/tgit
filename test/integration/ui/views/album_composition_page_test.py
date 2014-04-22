# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_property, contains

from test.integration.ui.views import ViewTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.album_composition_page_driver import AlbumCompositionPageDriver
from test.util import builders as build, fakes
from tgit.album import Album
from tgit.ui.views.album_composition_model import AlbumCompositionModel
from tgit.ui.views.album_composition_page import AlbumCompositionPage


# todo find a home for feature matchers
def hasTitle(title):
    return has_property('trackTitle', title)


class AlbumCompositionPageTest(ViewTest):
    def setUp(self):
        super(AlbumCompositionPageTest, self).setUp()
        self.album = Album()
        self.page = AlbumCompositionPage()
        self.driver = self.createDriverFor(self.page)
        self.show(self.page)
        self.page.display(AlbumCompositionModel(self.album, fakes.audioPlayer()))

    def createDriverFor(self, widget):
        return AlbumCompositionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders('Track Title', 'Lead Performer', 'Album Title', 'Bitrate', 'Duration', '', '')

    def testDisplaysTrackDetailsInColumns(self):
        self.album.addTrack(build.track(trackTitle='My Song', bitrate=192000,
                                        duration=timedelta(minutes=3, seconds=43).total_seconds()))
        self.album.releaseName = 'My Album'
        self.album.leadPerformer = 'My Artist'

        self.driver.showsTrack('My Song', 'My Artist', 'My Album', '192 kbps', '03:43')

    def testDisplaysAllTracksInRows(self):
        self.album.addTrack(build.track(trackTitle='First'))
        self.album.addTrack(build.track(trackTitle='Second'))

        self.driver.hasTrackCount(2)
        self.driver.showsTracksInOrder(['First'], ['Second'])

    def testSignalsWhenPlayTrackButtonClicked(self):
        self.album.addTrack(build.track(trackTitle='Track'))
        playClicked = ValueMatcherProbe('play track', has_property('trackTitle', 'Track'))

        self.page.bind(play=playClicked.received)

        self.driver.play('Track')
        self.driver.check(playClicked)

    def testSignalsWhenAddTracksButtonClicked(self):
        addClicked = ValueMatcherProbe('add tracks')

        self.page.bind(add=addClicked.received)

        self.driver.addTracks()
        self.driver.check(addClicked)

    def testSignalsWhenRemoveTrackButtonClicked(self):
        self.album.addTrack(build.track())
        self.album.addTrack(build.track(trackTitle='Track'))
        removeClicked = ValueMatcherProbe('remove track', has_property('trackTitle', 'Track'))

        self.page.bind(remove=removeClicked.received)

        self.driver.removeTrack('Track')
        self.driver.check(removeClicked)

    def testSignalsWhenTrackWasMoved(self):
        self.album.addTrack(build.track(trackTitle='Song #1'))
        self.album.addTrack(build.track(trackTitle='Song #2'))
        self.album.addTrack(build.track(trackTitle='Song #3'))

        fromPosition, toPosition = 2, 1
        trackMoved = ValueMatcherProbe('move track', contains(fromPosition, toPosition))

        self.page.bind(trackMoved=lambda from_, to: trackMoved.received([from_, to]))

        self.driver.moveTrack('Song #3', toPosition)
        self.driver.check(trackMoved)
# -*- coding: utf-8 -*-

from datetime import timedelta

from flexmock import flexmock
from hamcrest import has_property, contains

from test.integration.ui.views.view_test import ViewTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.album_composition_page_driver import AlbumCompositionPageDriver
from test.util import builders as build, fakes
from tgit.album import Album
from tgit.ui.views.album_composition_model import AlbumCompositionModel
from tgit.ui.views.album_composition_page import AlbumCompositionPage


# QTableWidgetItem.__repr__ = lambda widget: widget.text()


def hasTitle(title):
    return has_property('trackTitle', title)


class AlbumCompositionPageTest(ViewTest):
    def setUp(self):
        super(AlbumCompositionPageTest, self).setUp()
        self.player = flexmock(fakes.audioPlayer())
        self.album = Album()
        self.view = AlbumCompositionPage()
        self.widget = self.view.render(AlbumCompositionModel(self.album, self.player))
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return AlbumCompositionPageDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeaders(u'Titre de la piste', 'Artiste principal',
                                       "Titre de l'album", u'Débit', u'Durée', '', '')

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
        playTrackProbe = ValueMatcherProbe('play track request', has_property('trackTitle', 'Track'))

        class PlayTrackListener(object):
            def playTrack(self, track):
                playTrackProbe.received(track)

        self.view.announceTo(PlayTrackListener())

        self.driver.play('Track')
        self.driver.check(playTrackProbe)

    def testSignalsWhenAddTracksButtonClicked(self):
        addTracksProbe = ValueMatcherProbe('add tracks request')

        class AddTracksToAlbumListener(object):
            def addTracksToAlbum(self):
                addTracksProbe.received()

        self.view.announceTo(AddTracksToAlbumListener())

        self.driver.addTracks()
        self.driver.check(addTracksProbe)

    def testSignalsWhenRemoveTrackButtonClicked(self):
        self.album.addTrack(build.track())
        self.album.addTrack(build.track(trackTitle='Track'))
        removeTrackProbe = ValueMatcherProbe('remove track request', has_property('trackTitle', 'Track'))

        class RemoveTrackListener(object):
            def removeTrack(self, track):
                removeTrackProbe.received(track)

        self.view.announceTo(RemoveTrackListener())

        self.driver.removeTrack('Track')
        self.driver.check(removeTrackProbe)

    def testSignalsWhenTrackIsMoved(self):
        self.album.addTrack(build.track(trackTitle='Song #1'))
        self.album.addTrack(build.track(trackTitle='Song #2'))
        self.album.addTrack(build.track(trackTitle='Song #3'))

        fromPosition, toPosition = 2, 1

        moveTrackProbe = ValueMatcherProbe('move track request', contains(fromPosition, toPosition))

        class MoveTrackListener(object):
            def moveTrack(self, from_, to):
                moveTrackProbe.received((from_, to))

        self.view.announceTo(MoveTrackListener())

        self.driver.moveTrack('Song #3', toPosition)
        self.driver.check(moveTrackProbe)
# -*- coding: utf-8 -*-

from datetime import timedelta
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
from PyQt4.QtGui import QWidget

from tgit.ui.album_content_panel import AlbumContentPanel

from tests.integration.ui.base_widget_test import BaseWidgetTest
from tests.cute.finders import WidgetIdentity
from tests.drivers.album_content_panel_driver import AlbumContentPanelDriver


# todo extract that to a builders module
def buildTrack(**tags):
    defaults = dict(filename='track.mp3',
                    trackTitle=None,
                    duration=timedelta(minutes=3, seconds=30).total_seconds())
    return flexmock(**dict(defaults.items() + tags.items()))


class FakePlayer(object):
    source = None
    playing = False

    def hasSource(self):
        return self.source

    def setSource(self, filename):
        self.source = filename

    def isPlaying(self):
        return self.playing

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def slider(self):
        return QWidget()


class AlbumContentPanelTest(BaseWidgetTest):
    def setUp(self):
        super(AlbumContentPanelTest, self).setUp()
        self.player = flexmock(FakePlayer())
        self.panel = AlbumContentPanel(player=self.player)
        self.view(self.panel)
        self.driver = self.createDriverFor(self.panel)

    def tearDown(self):
        super(AlbumContentPanelTest, self).tearDown()

    def createDriverFor(self, widget):
        return AlbumContentPanelDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testDisplaysColumnHeadings(self):
        self.driver.showsColumnHeadings('Track Title', 'Duration')

    def testDisplaysTrackTitle(self):
        track = buildTrack(trackTitle='Banana Song')
        self.panel.setTrack(track)
        self.driver.showsTrackTitle('Banana Song')

    def testDisplaysTrackDuration(self):
        track = buildTrack(duration=timedelta(minutes=3, seconds=43).total_seconds())
        self.panel.setTrack(track)
        self.driver.showsTrackDuration('03:43')

    def testCanPlayAndPauseTrack(self):
        self.player.should_call('setSource').with_args('track.mp3').when(
            lambda: not self.player.hasSource())
        self.player.should_call('play').once().when(lambda: not self.player.isPlaying())
        self.player.should_call('pause').once().when(lambda: self.player.isPlaying())

        self.panel.setTrack(buildTrack(filename='track.mp3'))
        self.driver.playTrack()
        self.driver.pauseTrack()
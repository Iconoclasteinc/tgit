# -*- coding: utf-8 -*-

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util import builders

from tgit.album import Album
from tgit.player import SilentPlayer
from tgit.ui.main_screen import MainScreen
from tgit.ui.track_selector import TrackSelector


class MainScreenTest(BaseWidgetTest):
    def setUp(self):
        super(MainScreenTest, self).setUp()
        self.album = Album()
        self.mainScreen = MainScreen(self.album, SilentPlayer(), TrackSelector())
        self.view(self.mainScreen)
        self.tagger = self.createDriverFor(self.mainScreen)

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testSignalsRecordAlbumRequestsWhenSaveButtonClicked(self):
        recordAlbumRequest = ValueMatcherProbe('record album request')

        class RecordAlbumListener(object):
            def recordAlbum(self):
                recordAlbumRequest.setReceivedValue(True)

        self.mainScreen.addRequestListener(RecordAlbumListener())
        self.album.addTrack(builders.track())
        self.tagger.nextPage()
        self.tagger.saveAlbum()
        self.tagger.check(recordAlbumRequest)
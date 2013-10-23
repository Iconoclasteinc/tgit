# -*- coding: utf-8 -*-

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util.fake_audio_library import FakeAudioLibrary

from tgit.album import Album
from tgit.producer import ProductionPortfolio, ArtisticDirector
from tgit.ui.main_window import MainWindow
from tgit.ui.track_selector import TrackSelector


class MainWindowTest(BaseWidgetTest):

    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.productions = ProductionPortfolio()
        self.widget = MainWindow(self.productions)
        self.widget.setTrackSelector(TrackSelector())
        self.view(self.widget)
        self.driver = self.createDriverFor(self.widget)
        self.audioLibrary = FakeAudioLibrary()

    def tearDown(self):
        self.audioLibrary.delete()
        super(MainWindowTest, self).tearDown()

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testStartsOnWelcomeScreen(self):
        self.driver.isShowingWelcomeScreen()

    def testShowsMainScreenAndEnablesAlbumCommandsWhenAlbumCreated(self):
        self.widget.productionAdded(ArtisticDirector(), Album())
        self.driver.isShowingTaggingScreen()
        self.driver.hasEnabledImportTrackMenuItem()
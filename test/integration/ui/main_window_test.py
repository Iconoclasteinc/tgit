# -*- coding: utf-8 -*-

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util.fakes import FakeAudioPlayer, FakeFileChooser

from tgit.album import Album
from tgit.record_label import AlbumPortfolio
from tgit.ui.main_window import MainWindow


class MainWindowTest(BaseWidgetTest):

    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.widget = MainWindow(AlbumPortfolio(), FakeAudioPlayer(), FakeFileChooser(),
                                 FakeFileChooser())
        self.view(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testStartsOnWelcomeScreen(self):
        self.driver.isShowingWelcomeScreen()

    def testShowsMainScreenAndEnablesAlbumCommandsWhenAlbumCreated(self):
        self.widget.albumCreated(Album())
        self.driver.isShowingTaggingScreen()
        self.driver.hasEnabledAddFilesMenuItem()
        self.driver.hasEnabledAddFolderMenuItem()
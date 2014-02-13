# -*- coding: utf-8 -*-

from test.integration.ui.view_test import ViewTest
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util import builders as build, fakes

from tgit.album import Album
from tgit.album_portfolio import AlbumPortfolio
from tgit.ui.main_window import MainWindow


class MainWindowTest(ViewTest):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.widget = MainWindow(AlbumPortfolio(), fakes.audioPlayer())
        self.show(self.widget)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testStartsOnWelcomeScreen(self):
        self.driver.showsWelcomeScreen()

    def testShowsMainScreenOnAlbumCreation(self):
        self.widget.albumCreated(Album())
        self.driver.showsAlbumScreen()

    def testShowsExportAsDialogOnExport(self):
        self.widget.export(build.album())
        self.driver.showsExportAsDialog()
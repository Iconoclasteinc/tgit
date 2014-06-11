# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow

from test.integration.ui.views import ViewTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.menu_bar_driver import MenuBarDriver
from test.util import builders as build
from tgit.ui.views.menu_bar import MenuBar


class MenuBarTest(ViewTest):
    def setUp(self):
        super(MenuBarTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.view = MenuBar()
        self.mainWindow.setMenuBar(self.view)
        self.show(self.mainWindow)
        self.driver = self.createDriverFor(self.view)

    def createDriverFor(self, widget):
        return MenuBarDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testHasAlbumMenuInitiallyDisabled(self):
        self.driver.hasDisabledAlbumActions()

    def testSignalsWhenAddFilesMenuItemClicked(self):
        album = build.album()
        addFilesEvent = ValueMatcherProbe('add files', album)
        self.view.bind(addFiles=addFilesEvent.received)
        self.view.albumCreated(album)
        self.driver.addFiles()
        self.driver.check(addFilesEvent)

    def testSignalsWhenAddFolderMenuItemClicked(self):
        album = build.album()
        addFolderEvent = ValueMatcherProbe('add folder', album)
        self.view.bind(addFolder=addFolderEvent.received)
        self.view.albumCreated(album)
        self.driver.addFolder()
        self.driver.check(addFolderEvent)

    def testSignalsWhenExportMenuItemClicked(self):
        album = build.album()
        exportAlbumEvent = ValueMatcherProbe('export', album)
        self.view.bind(exportAlbum=exportAlbumEvent.received)
        self.view.albumCreated(album)
        self.driver.export()
        self.driver.check(exportAlbumEvent)

    def testSignalsWhenSettingsMenuItemClicked(self):
        changeSettingsEvent = ValueMatcherProbe('change settings')
        self.view.bind(settings=changeSettingsEvent.received)
        self.driver.settings()
        self.driver.check(changeSettingsEvent)
# -*- coding: utf-8 -*-

from tgit.util import sip_api
sip_api.use_v2()

from PyQt4.QtGui import QMainWindow

from test.integration.ui import ViewTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.menu_bar_driver import MenuBarDriver
from test.util import builders as build
from tgit.ui.menu_bar import MenuBar


class MenuBarTest(ViewTest):
    def setUp(self):
        super(MenuBarTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.menuBar = MenuBar()
        self.mainWindow.setMenuBar(self.menuBar)
        self.show(self.mainWindow)
        self.driver = self.createDriverFor(self.menuBar)

    def createDriverFor(self, widget):
        return MenuBarDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testHasAlbumMenuInitiallyDisabled(self):
        self.driver.hasDisabledAlbumActions()

    def testSignalsWhenAddFilesMenuItemClicked(self):
        album = build.album()
        addFilesSignal = ValueMatcherProbe('add files', album)
        self.menuBar.addFiles.connect(addFilesSignal.received)
        self.menuBar.albumCreated(album)
        self.driver.addFiles()
        self.driver.check(addFilesSignal)

    def testSignalsWhenAddFolderMenuItemClicked(self):
        album = build.album()
        addFolderSignal = ValueMatcherProbe('add folder', album)
        self.menuBar.addFolder.connect(addFolderSignal.received)
        self.menuBar.albumCreated(album)
        self.driver.addFolder()
        self.driver.check(addFolderSignal)

    def testSignalsWhenExportMenuItemClicked(self):
        album = build.album()
        exportAlbumSignal = ValueMatcherProbe('export', album)
        self.menuBar.export.connect(exportAlbumSignal.received)
        self.menuBar.albumCreated(album)
        self.driver.export()
        self.driver.check(exportAlbumSignal)

    def testSignalsWhenSettingsMenuItemClicked(self):
        changeSettingsSignal = ValueMatcherProbe('change settings')
        self.menuBar.settings.connect(changeSettingsSignal.received)
        self.driver.settings()
        self.driver.check(changeSettingsSignal)
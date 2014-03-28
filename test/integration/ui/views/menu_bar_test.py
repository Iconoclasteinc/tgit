# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow

from test.integration.ui.views import ViewTest
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.menu_bar_driver import MenuBarDriver
from tgit.ui.views.menu_bar import MenuBar


class MenuBarTest(ViewTest):
    def setUp(self):
        super(MenuBarTest, self).setUp()
        self.menuBar = MenuBar()
        self.widget = self.menuBar.render()
        self.mainWindow = QMainWindow()
        self.mainWindow.setMenuBar(self.widget)
        self.show(self.mainWindow)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return MenuBarDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testHasAlbumMenuInitiallyDisabled(self):
        self.driver.hasDisabledAlbumMenu()

    def testSignalsWhenAddFilesMenuItemClicked(self):
        addFilesSignal = ValueMatcherProbe('add files')

        class AddFilesListener(object):
            def addFiles(self):
                addFilesSignal.received()

        self.menuBar.announceTo(AddFilesListener())
        self.menuBar.enableAlbumMenu()
        self.driver.addFiles()
        self.driver.check(addFilesSignal)

    def testSignalsWhenAddFolderMenuItemClicked(self):
        addFilesSignal = ValueMatcherProbe('add folder')

        class AddFolderListener(object):
            def addFolder(self):
                addFilesSignal.received()

        self.menuBar.announceTo(AddFolderListener())
        self.menuBar.enableAlbumMenu()
        self.driver.addFolder()
        self.driver.check(addFilesSignal)

    def testSignalsWhenExportMenuItemClicked(self):
        exportAlbumSignal = ValueMatcherProbe('export album')

        class ExportAlbumListener(object):
            def export(self):
                exportAlbumSignal.received()

        self.menuBar.announceTo(ExportAlbumListener())
        self.menuBar.enableAlbumMenu()
        self.driver.export()
        self.driver.check(exportAlbumSignal)
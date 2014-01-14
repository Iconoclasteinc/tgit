# -*- coding: utf-8 -*-

from hamcrest import equal_to

from test.integration.ui.view_test import ViewTest
from PyQt4.QtGui import QMainWindow
from test.cute.finders import WidgetIdentity
from test.cute.probes import ValueMatcherProbe
from test.drivers.menu_bar_driver import MenuBarDriver
from test.util import builders as build
from tgit.ui.menu_bar import MenuBar


class MenuBarTest(ViewTest):
    def setUp(self):
        super(MenuBarTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.show(self.mainWindow)
        self.widget = MenuBar(self.mainWindow)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return MenuBarDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testEnablesFileCommandsWhenAlbumCreated(self):
        self.widget.albumCreated(build.album())
        self.driver.hasEnabledAddFilesMenuItem()
        self.driver.hasEnabledAddFolderMenuItem()

    def testSignalsExportAlbumWhenExportMenuItemIsClicked(self):
        album = build.album()
        exportCommand = ValueMatcherProbe('export command', equal_to(album))

        class ExportCommandListener(object):
            def export(self, album):
                exportCommand.received(album)

        self.widget.announceTo(ExportCommandListener())
        self.widget.albumCreated(album)
        self.driver.export()
        self.driver.check(exportCommand)
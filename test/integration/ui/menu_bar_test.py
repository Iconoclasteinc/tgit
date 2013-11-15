# -*- coding: utf-8 -*-

from test.integration.ui.base_widget_test import BaseWidgetTest
from PyQt4.QtGui import QMainWindow
from test.cute.finders import WidgetIdentity
from test.drivers.menu_bar_driver import MenuBarDriver
from test.util import builders as build
from tgit.ui.menu_bar import MenuBar


class MenuBarTest(BaseWidgetTest):
    def setUp(self):
        super(MenuBarTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.view(self.mainWindow)
        self.widget = MenuBar(self.mainWindow)
        self.driver = self.createDriverFor(self.widget)

    def createDriverFor(self, widget):
        return MenuBarDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testEnablesFileCommandsWhenAlbumCreated(self):
        self.widget.albumCreated(build.album())
        self.driver.hasEnabledAddFilesMenuItem()
        self.driver.hasEnabledAddFolderMenuItem()
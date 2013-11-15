# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMenuBar

from test.cute.matchers import named
from test.cute.widgets import QMenuBarDriver

from tgit.ui import constants as ui


def menuBar(parent):
    return MenuBarDriver.findSingle(parent, QMenuBar)


class MenuBarDriver(QMenuBarDriver):
    def addFiles(self):
        menu = self._openFileMenu()
        menuItem = self._addFilesMenuItem(menu)
        menuItem.isEnabled()
        menuItem.click()

    def hasEnabledAddFilesMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._addFilesMenuItem(menu)
        menuItem.isEnabled()
        menu.close()

    def hasEnabledAddFolderMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._addFolderMenuItem(menu)
        menuItem.isEnabled()
        menu.close()

    def _openFileMenu(self):
        menuBar = MenuBarDriver.findSingle(self, QMenuBar)
        menu = menuBar.menu(named(ui.FILE_MENU_NAME))
        menu.open()
        return menu

    def _addFilesMenuItem(self, menu):
        return menu.menuItem(named(ui.ADD_FILES_ACTION_NAME))

    def _addFolderMenuItem(self, menu):
        return menu.menuItem(named(ui.ADD_FOLDER_ACTION_NAME))

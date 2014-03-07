# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMenuBar

from test.cute.matchers import named
from test.cute.widgets import QMenuBarDriver
from tgit.ui.views.menu_bar import MenuBar


def menuBar(parent):
    return MenuBarDriver.findSingle(parent, QMenuBar)


def addFilesMenuItem(menu):
    return menu.menuItem(named(MenuBar.ADD_FILES_ACTION_NAME))


def addFolderMenuItem(menu):
    return menu.menuItem(named(MenuBar.ADD_FOLDER_ACTION_NAME))


def exportMenuItem(menu):
    return menu.menuItem(named(MenuBar.EXPORT_ACTION_NAME))


class MenuBarDriver(QMenuBarDriver):
    def hasDisabledAlbumMenu(self):
        menu = self._openFileMenu()
        addFilesMenuItem(menu).isDisabled()
        addFolderMenuItem(menu).isDisabled()
        exportMenuItem(menu).isDisabled()
        menu.close()

    def addFiles(self):
        menu = self._openFileMenu()
        addFilesMenuItem(menu).click()

    def addFolder(self):
        menu = self._openFileMenu()
        addFolderMenuItem(menu).click()

    def export(self):
        menu = self._openFileMenu()
        exportMenuItem(menu).click()

    def _openFileMenu(self):
        menu = self._fileMenu()
        menu.open()
        return menu

    def _fileMenu(self):
        return self.menu(named(MenuBar.FILE_MENU_NAME))

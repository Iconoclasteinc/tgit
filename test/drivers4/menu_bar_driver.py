# -*- coding: utf-8 -*-

from PyQt4.QtGui import QMenuBar

from test.cute4.matchers import named
from test.cute4.widgets import QMenuBarDriver
from test.drivers4.settings_dialog_driver import settingsDialog


def menuBar(parent):
    return MenuBarDriver.findSingle(parent, QMenuBar)


def addFilesMenuItem(menu):
    return menu.menuItem(named('add-files'))


def addFolderMenuItem(menu):
    return menu.menuItem(named('add-folder'))


def exportMenuItem(menu):
    return menu.menuItem(named('export'))


class MenuBarDriver(QMenuBarDriver):
    def hasDisabledAlbumActions(self):
        menu = self.openMenu(named('file-menu'))
        addFilesMenuItem(menu).isDisabled()
        addFolderMenuItem(menu).isDisabled()
        exportMenuItem(menu).isDisabled()
        menu.close()

    def addFiles(self):
        menu = self.openMenu(named('file-menu'))
        addFilesMenuItem(menu).click()

    def addFolder(self):
        menu = self.openMenu(named('file-menu'))
        addFolderMenuItem(menu).click()

    def export(self):
        menu = self.openMenu(named('file-menu'))
        exportMenuItem(menu).click()

    def settings(self):
        menu = self.openMenu(named('file-menu'))
        menu.selectMenuItem(named('Settings'))
        return settingsDialog(self)

    def openMenu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

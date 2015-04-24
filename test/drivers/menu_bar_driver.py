# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMenuBar

from cute.matchers import named
from cute.widgets import QMenuBarDriver
from test.drivers.settings_dialog_driver import settingsDialog


def menuBar(parent):
    return MenuBarDriver.find_single(parent, QMenuBar)


def addFilesMenuItem(menu):
    return menu.menu_item(named('add-files'))


def addFolderMenuItem(menu):
    return menu.menu_item(named('add-folder'))


def exportMenuItem(menu):
    return menu.menu_item(named('export'))


class MenuBarDriver(QMenuBarDriver):
    def hasDisabledAlbumActions(self):
        menu = self.openMenu(named('file-menu'))
        addFilesMenuItem(menu).is_disabled()
        addFolderMenuItem(menu).is_disabled()
        exportMenuItem(menu).is_disabled()
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
        menu.select_menu_item(named('Settings'))
        return settingsDialog(self)

    def openMenu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

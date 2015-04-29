# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMenuBar

from cute.matchers import named
from cute.widgets import QMenuBarDriver
from test.drivers.settings_dialog_driver import settings_dialog


def menu_bar(parent):
    return MenuBarDriver.find_single(parent, QMenuBar)


def addFilesMenuItem(menu):
    return


def addFolderMenuItem(menu):
    return


def exportMenuItem(menu):
    return


class MenuBarDriver(QMenuBarDriver):
    def has_disabled_album_actions(self):
        menu = self.openMenu(named('file-menu'))
        menu.menu_item(named('add-files')).is_disabled()
        menu.menu_item(named('add-folder')).is_disabled()
        menu.menu_item(named('export')).is_disabled()
        menu.close()

    def add_files(self):
        menu = self.openMenu(named('file-menu'))
        menu.menu_item(named('add-files')).click()

    def add_folder(self):
        menu = self.openMenu(named('file-menu'))
        menu.menu_item(named('add-folder')).click()

    def export(self):
        menu = self.openMenu(named('file-menu'))
        menu.menu_item(named('export')).click()

    def settings(self):
        menu = self.openMenu(named('file-menu'))
        menu.select_menu_item(named('Settings'))
        return settings_dialog(self)

    def openMenu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

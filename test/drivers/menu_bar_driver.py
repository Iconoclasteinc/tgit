# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenuBar

from cute.matchers import named
from cute.widgets import QMenuBarDriver
from .settings_dialog_driver import settings_dialog


def menu_bar(parent):
    return MenuBarDriver.find_single(parent, QMenuBar, named("menu_bar"))


class MenuBarDriver(QMenuBarDriver):
    def has_disabled_album_actions(self):
        menu = self.open_menu(named("file_menu"))
        menu.menu_item(named("add_files_action")).is_disabled()
        menu.menu_item(named("add_folder_action")).is_disabled()
        menu.menu_item(named("export_action")).is_disabled()
        menu.menu_item(named("close_album_action")).is_disabled()
        menu.menu_item(named("save_album_action")).is_disabled()
        menu.close()

    def add_files(self):
        menu = self.open_menu(named("file_menu"))
        menu.menu_item(named("add_files_action")).click()

    def add_folder(self):
        menu = self.open_menu(named("file_menu"))
        menu.menu_item(named("add_folder_action")).click()

    def export(self):
        menu = self.open_menu(named("file_menu"))
        menu.menu_item(named("export_action")).click()

    def settings(self):
        menu = self.open_menu(named("file_menu"))
        menu.select_menu_item(named("settings_action"))
        return settings_dialog(self)

    def close_album(self):
        menu = self.open_menu(named("file_menu"))
        menu.menu_item(named("close_album_action")).click()

    def save(self):
        menu = self.open_menu(named("file_menu"))
        menu.menu_item(named("save_album_action")).click()

    def open_menu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenuBar

from cute.matchers import named
from cute.widgets import QMenuBarDriver
from .settings_dialog_driver import settings_dialog


def menu_bar(parent):
    return MenuBarDriver.find_single(parent, QMenuBar, named("menu_bar"))


class MenuBarDriver(QMenuBarDriver):
    @property
    def file(self):
        return self.FileMenuDriver(self.open_menu(named("file_menu")), self)

    @property
    def navigate(self):
        return self.NavigateMenuDriver(self.open_menu(named("navigate_menu")))

    def open_menu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

    class FileMenuDriver:
        def __init__(self, menu_driver, menu_bar_driver):
            self._menu_bar_driver = menu_bar_driver
            self._menu_driver = menu_driver

        def has_disabled_album_actions(self):
            self._menu_driver.menu_item(named("add_files_action")).is_disabled()
            self._menu_driver.menu_item(named("add_folder_action")).is_disabled()
            self._menu_driver.menu_item(named("export_action")).is_disabled()
            self._menu_driver.menu_item(named("close_album_action")).is_disabled()
            self._menu_driver.menu_item(named("save_album_action")).is_disabled()
            self._menu_driver.close()

        def add_files(self):
            self._menu_driver.menu_item(named("add_files_action")).click()

        def add_folder(self):
            self._menu_driver.menu_item(named("add_folder_action")).click()

        def export(self):
            self._menu_driver.menu_item(named("export_action")).click()

        def settings(self):
            self._menu_driver.select_menu_item(named("settings_action"))
            return settings_dialog(self._menu_bar_driver)

        def close_album(self):
            self._menu_driver.menu_item(named("close_album_action")).click()

        def save(self):
            self._menu_driver.menu_item(named("save_album_action")).click()

    class NavigateMenuDriver:
        def __init__(self, menu_driver):
            self._menu_driver = menu_driver

        def to_composition_page(self):
            self._menu_driver.select_menu_item(named("to_album_edition_action"))

        def is_disabled(self):
            self._menu_driver.is_disabled()

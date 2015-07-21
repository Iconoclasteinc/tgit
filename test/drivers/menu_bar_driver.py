# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenuBar
from hamcrest import all_of, is_not, has_item

from cute import matchers
from cute.widgets import QMenuBarDriver
from .settings_dialog_driver import settings_dialog


def menu_bar(parent):
    return MenuBarDriver.find_single(parent, QMenuBar, matchers.named("menu_bar"))


class MenuBarDriver(QMenuBarDriver):
    @property
    def file(self):
        return self.FileMenuDriver(self.open_menu(matchers.named("file_menu")), self)

    @property
    def navigate(self):
        return self.NavigateMenuDriver(self.open_menu(matchers.named("navigate_menu")))

    @property
    def help(self):
        return self.HelpMenuDriver(self.open_menu(matchers.named("help_menu")))

    def open_menu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

    class FileMenuDriver:
        def __init__(self, menu_driver, menu_bar_driver):
            self._menu_bar_driver = menu_bar_driver
            self._menu_driver = menu_driver

        def has_disabled_album_actions(self):
            self._menu_driver.menu_item(matchers.named("add_files_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("add_folder_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("export_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("close_album_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("save_album_action")).is_disabled()
            self._menu_driver.close()

        def add_files(self):
            self._menu_driver.menu_item(matchers.named("add_files_action")).click()

        def add_folder(self):
            self._menu_driver.menu_item(matchers.named("add_folder_action")).click()

        def export(self):
            self._menu_driver.menu_item(matchers.named("export_action")).click()

        def settings(self):
            self._menu_driver.select_menu_item(matchers.named("settings_action"))
            return settings_dialog(self._menu_bar_driver)

        def close_album(self):
            self._menu_driver.menu_item(matchers.named("close_album_action")).click()

        def save(self):
            self._menu_driver.menu_item(matchers.named("save_album_action")).click()

        def exit(self):
            self._menu_driver.menu_item(matchers.named("exit_action")).click()

    class NavigateMenuDriver:
        def __init__(self, menu_driver):
            self._menu_driver = menu_driver

        def to_album_page(self):
            self._menu_driver.select_menu_item(matchers.named("to_album_edition_action"))

        def to_track_list_page(self):
            self._menu_driver.select_menu_item(matchers.named("to_track_list_action"))

        def to_track_page(self, title, track_number):
            self._menu_driver.select_menu_item(matchers.with_text(track_menu_item(title, track_number)))

        def shows_track_action(self, title, track_number):
            self._menu_driver.has_menu_item(matchers.with_text(track_menu_item(title, track_number)))

        def does_not_show_action(self, title, track_number):
            self._menu_driver.has_menu_item(without_item(track_menu_item(title, track_number)))

        def is_disabled(self):
            self._menu_driver.is_disabled()

    class HelpMenuDriver:
        def __init__(self, menu_driver):
            self._menu_driver = menu_driver

        def about_qt(self):
            self._menu_driver.select_menu_item(matchers.named("_about_qt_action"))

        def about(self):
            self._menu_driver.select_menu_item(matchers.named("_about_action"))


def without_item(title):
    return is_not(has_item(title))


def track_menu_item(title, track_number):
    return "{0} - {1}".format(track_number, title)

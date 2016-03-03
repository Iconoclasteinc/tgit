# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenuBar
from hamcrest import is_not, has_item

from cute import matchers
from cute.widgets import QMenuBarDriver
from .user_preferences_dialog_driver import user_preferences_dialog


def menu_bar(parent):
    return MenuBarDriver.find_single(parent, QMenuBar, matchers.named("_menu_bar"))


class MenuBarDriver(QMenuBarDriver):
    @property
    def file(self):
        return self.FileMenuDriver(self.open_menu(matchers.named("_file_menu")), self)

    @property
    def navigate(self):
        return self.NavigateMenuDriver(self.open_menu(matchers.named("_navigate_menu")))

    @property
    def account(self):
        return self.AccountMenuDriver(self.open_menu(matchers.named("_account_menu")), self)

    @property
    def help(self):
        return self.HelpMenuDriver(self.open_menu(matchers.named("_help_menu")))

    @property
    def transmit(self):
        return self.TransmitMenuDriver(self.open_menu(matchers.named("_transmit_menu")))

    def open_menu(self, matching):
        menu = self.menu(matching)
        menu.open()
        return menu

    class FileMenuDriver:
        def __init__(self, menu_driver, menu_bar_driver):
            self._menu_bar_driver = menu_bar_driver
            self._menu_driver = menu_driver

        def has_disabled_project_actions(self):
            self._menu_driver.menu_item(matchers.named("_add_files_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("_add_folder_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("_export_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("_close_project_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("_save_project_action")).is_disabled()
            self._menu_driver.close()

        def add_files(self):
            self._menu_driver.menu_item(matchers.named("_add_files_action")).click()

        def add_folder(self):
            self._menu_driver.menu_item(matchers.named("_add_folder_action")).click()

        def export(self):
            self._menu_driver.menu_item(matchers.named("_export_action")).click()

        def settings(self):
            self._menu_driver.select_menu_item(matchers.named("_settings_action"))
            return user_preferences_dialog(self._menu_bar_driver)

        def close_project(self):
            self._menu_driver.menu_item(matchers.named("_close_project_action")).click()

        def save(self):
            self._menu_driver.menu_item(matchers.named("_save_project_action")).click()

        def exit(self):
            self._menu_driver.menu_item(matchers.named("_exit_action")).click()

    class NavigateMenuDriver:
        BASE_TRACKS_INDEX = 1

        def __init__(self, menu_driver):
            self._menu_driver = menu_driver

        def to_project_page(self):
            self._menu_driver.select_menu_item(matchers.named("_to_project_edition_action"))

        def to_track_list_page(self):
            self._menu_driver.select_menu_item(matchers.named("_to_track_list_action"))

        def to_track_page(self, title, track_number):
            self._menu_driver.select_menu_item(matchers.with_text(_track_menu_item(title, track_number)))

        def shows_track_action(self, title, track_number):
            track_index = self.BASE_TRACKS_INDEX + track_number
            self._menu_driver.has_menu_item(matchers.with_text(_track_menu_item(title, track_number)), track_index)

        def does_not_show_action(self, title, track_number):
            self._menu_driver.has_menu_item(_without_item(_track_menu_item(title, track_number)))

        def is_disabled(self):
            self._menu_driver.is_disabled()

    class HelpMenuDriver:
        def __init__(self, menu_driver):
            self._menu_driver = menu_driver

        def about_qt(self):
            self._menu_driver.select_menu_item(matchers.named("_about_qt_action"))

        def about(self):
            self._menu_driver.select_menu_item(matchers.named("_about_action"))

        def online_help(self):
            self._menu_driver.select_menu_item(matchers.named("_online_help_action"))

        def request_feature(self):
            self._menu_driver.select_menu_item(matchers.named("_request_feature_action"))

    class AccountMenuDriver:
        def __init__(self, menu_driver, menu_bar_driver):
            self._menu_bar_driver = menu_bar_driver
            self._menu_driver = menu_driver

        def register(self):
            self._menu_driver.select_menu_item(matchers.named("_register_action"))

        def sign_in(self):
            self._menu_driver.menu_item(matchers.named("_sign_in_action")).click()

        def sign_out(self):
            self._menu_driver.menu_item(matchers.named("_sign_out_action")).click()

        def shows_signed_in_user(self, email):
            self._menu_driver.menu_item(matchers.named("_sign_in_action")).is_hidden()
            self._menu_driver.menu_item(matchers.named("_logged_user_action")).is_showing_on_screen()
            self._menu_driver.menu_item(matchers.named("_logged_user_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("_sign_out_action")).is_enabled()
            self._menu_driver.has_menu_item(matchers.with_text(email))
            self._menu_driver.close()

        def shows_sign_in_menu(self):
            self._menu_bar_driver.pause(150)
            self._menu_driver.menu_item(matchers.named("_sign_in_action")).is_showing_on_screen()
            self._menu_driver.menu_item(matchers.named("_sign_out_action")).is_disabled()
            self._menu_driver.menu_item(matchers.named("_logged_user_action")).is_hidden()
            self._menu_driver.close()

    class TransmitMenuDriver:
        def __init__(self, menu_driver):
            self._menu_driver = menu_driver

        def soproq(self):
            self._menu_driver.select_menu_item(matchers.named("_soproq_action"))

        def is_disabled(self):
            self._menu_driver.is_disabled()


def _without_item(title):
    return is_not(has_item(title))


def _track_menu_item(title, track_number):
    return "{0} - {1}".format(track_number, title)

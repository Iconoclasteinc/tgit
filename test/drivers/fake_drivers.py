# -*- coding: utf-8 -*-
from cute.matchers import named
from cute.properties import PropertyQuery
from cute.widgets import WidgetDriver
from test.integration.ui.fake_widgets import *


def current_page():
    return PropertyQuery("current page", lambda w: w.current_page)


class FakeProjectScreenDriver(WidgetDriver):
    def is_showing_page(self, matching):
        self.has(current_page(), matching)

    def is_showing_track_list_tab(self):
        self.is_showing_page(TRACK_LIST_TAB_NAME)

    def is_showing_project_edition_page(self):
        self.is_showing_page(PROJECT_EDITION_PAGE_NAME)

    def is_showing_track_edition_page(self, number):
        self.is_showing_page(track_edition_page_name(number))


def widget(parent, matching):
    return WidgetDriver.find_single(parent, FakeWidget, matching)


def startup_screen(parent):
    return widget(parent, named(STARTUP_SCREEN_NAME))


def project_screen(parent):
    return FakeProjectScreenDriver.find_single(parent, FakeProjectScreen, named(PROJECT_SCREEN_NAME))


def no_widget(in_parent, matching):
    return WidgetDriver.find_none(in_parent, FakeWidget, matching)


def no_startup_screen(driver):
    return no_widget(driver, named(STARTUP_SCREEN_NAME))


def no_album_screen(driver):
    return no_widget(driver, named(PROJECT_SCREEN_NAME))

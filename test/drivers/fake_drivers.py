# -*- coding: utf-8 -*-
from cute.matchers import named
from cute.properties import PropertyQuery
from cute.widgets import WidgetDriver
from test.integration.ui.fake_widgets import *


def current_page():
    return PropertyQuery("current page", lambda w: w.current_page)


class FakeAlbumScreenDriver(WidgetDriver):
    def is_showing_page(self, matching):
        self.has(current_page(), matching)

    def is_showing_track_list_page(self):
        self.is_showing_page(TRACK_LIST_PAGE_NAME)

    def is_showing_album_edition_page(self):
        self.is_showing_page(ALBUM_EDITION_PAGE_NAME)

    def is_showing_track_edition_page(self, number):
        self.is_showing_page(track_edition_page_name(number))


def widget(parent, matching):
    return WidgetDriver.find_single(parent, FakeWidget, matching)


def track_list_page(parent):
    return widget(parent, named(TRACK_LIST_PAGE_NAME))


def album_edition_page(parent):
    return widget(parent, named(ALBUM_EDITION_PAGE_NAME))


def startup_screen(parent):
    return widget(parent, named(STARTUP_SCREEN_NAME))


def album_screen(parent):
    return FakeAlbumScreenDriver.find_single(parent, FakeAlbumScreen, named(ALBUM_SCREEN_NAME))


def track_edition_page(parent, number):
    return widget(parent, named(track_edition_page_name(number)))


def no_widget(in_parent, matching):
    return WidgetDriver.find_none(in_parent, FakeWidget, matching)


def no_startup_screen(driver):
    return no_widget(driver, named(STARTUP_SCREEN_NAME))


def no_album_screen(driver):
        return no_widget(driver, named(ALBUM_SCREEN_NAME))


def no_track_list_page(driver):
    return no_widget(driver, named(TRACK_LIST_PAGE_NAME))


def no_album_edition_page(driver):
    return no_widget(driver, named(ALBUM_EDITION_PAGE_NAME))


def no_track_edition_page(driver, number):
    return no_widget(driver, named(track_edition_page_name(number)))

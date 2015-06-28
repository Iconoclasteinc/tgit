# -*- coding: utf-8 -*-
from cute.matchers import StateMatcher, named
from cute.properties import PropertyQuery
from cute.widgets import WidgetDriver
from test.integration.ui.fake_widgets import *


def closed():
    return StateMatcher(lambda w: w.closed, "closed", "still open")


def current_page():
    return PropertyQuery("current page", lambda w: w.current_page)


class FakeWidgetDriver(WidgetDriver):
    def is_closed(self):
        self.is_(closed())


class FakeAlbumScreenDriver(FakeWidgetDriver):
    def is_showing_page(self, matching):
        self.has(current_page(), matching)

    def is_showing_album_composition_page(self):
        self.is_showing_page(ALBUM_COMPOSITION_PAGE_NAME)

    def is_showing_album_edition_page(self):
        self.is_showing_page(ALBUM_EDITION_PAGE_NAME)

    def is_showing_track_edition_page(self, number):
        self.is_showing_page(track_edition_page_name(number))


def fake_widget(parent, matching):
    return FakeWidgetDriver.find_single(parent, FakeWidget, matching)


def fake_album_composition_page(parent):
    return fake_widget(parent, named(ALBUM_COMPOSITION_PAGE_NAME))


def fake_album_edition_page(parent):
    return fake_widget(parent, named(ALBUM_EDITION_PAGE_NAME))


def fake_startup_screen(parent):
    return fake_widget(parent, named(STARTUP_SCREEN_NAME))


def fake_album_screen(parent):
    return FakeAlbumScreenDriver.find_single(parent, FakeAlbumScreen, named(ALBUM_SCREEN_NAME))


def fake_track_edition_page(parent, number):
    return fake_widget(parent, named(track_edition_page_name(number)))

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from hamcrest import assert_that

STARTUP_SCREEN_NAME = "startup_screen"
ALBUM_SCREEN_NAME = "album_screen"
TRACK_LIST_PAGE_NAME = "track_list_page"
ALBUM_EDITION_PAGE_NAME = "album_edition_page"
TRACK_EDITION_PAGE_NAME = "track_edition_page"


def track_edition_page_name(number):
    return "{}_{}".format(TRACK_EDITION_PAGE_NAME, number)


def fake_widget(name):
    return FakeWidget(name)


class FakeWidget(QWidget):
    closed = False

    def __init__(self, name):
        super().__init__()
        self.setObjectName(name)

    def close(self):
        self.closed = True

    def is_closed(self):
        assert_that(self.closed, "widget named '{}' still open".format(self.objectName()))


def fake_track_list_page():
    return fake_widget(TRACK_LIST_PAGE_NAME)


def fake_album_edition_page():
    return fake_widget(ALBUM_EDITION_PAGE_NAME)


def fake_track_edition_page(track_number):
    return fake_widget(track_edition_page_name(track_number))


def fake_startup_screen():
    return fake_widget(STARTUP_SCREEN_NAME)


def fake_album_screen(*_):
    return FakeAlbumScreen()


class FakeAlbumScreen(FakeWidget):
    current_page = None

    def __init__(self):
        super().__init__(ALBUM_SCREEN_NAME)

    def to_album_edition_page(self):
        self.current_page = ALBUM_EDITION_PAGE_NAME

    def to_track_list_page(self):
        self.current_page = TRACK_LIST_PAGE_NAME

    def to_track_page(self, index):
        self.current_page = track_edition_page_name(index + 1)

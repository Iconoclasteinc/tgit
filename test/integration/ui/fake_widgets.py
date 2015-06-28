# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget

STARTUP_SCREEN_NAME = "startup_screen"
ALBUM_SCREEN_NAME = "album_screen"
ALBUM_COMPOSITION_PAGE_NAME = "album_composition_page"
ALBUM_EDITION_PAGE_NAME = "album_edition_page"
TRACK_EDITION_PAGE_NAME = "track_edition_page"


def track_edition_page_name(number):
    return "{}_{}".format(TRACK_EDITION_PAGE_NAME, number)


def widget(name):
    return FakeWidget(name)


class FakeWidget(QWidget):
    closed = False

    def __init__(self, name):
        super().__init__()
        self.setObjectName(name)

    def close(self):
        self.closed = True


def album_composition_page():
    return widget(ALBUM_COMPOSITION_PAGE_NAME)


def album_edition_page():
    return widget(ALBUM_EDITION_PAGE_NAME)


def track_edition_page(track_number):
    return widget(track_edition_page_name(track_number))


def startup_screen():
    return widget(STARTUP_SCREEN_NAME)


def album_screen(*_):
    return FakeAlbumScreen()


class FakeAlbumScreen(FakeWidget):
    current_page = None

    def __init__(self):
        super().__init__(ALBUM_SCREEN_NAME)

    def show_album_edition_page(self):
        self.current_page = ALBUM_EDITION_PAGE_NAME

    def show_album_composition_page(self):
        self.current_page = ALBUM_COMPOSITION_PAGE_NAME

    def show_track_page(self, track_number):
        self.current_page = track_edition_page_name(track_number)

# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from hamcrest import assert_that

STARTUP_SCREEN_NAME = "startup_screen"
PROJECT_SCREEN_NAME = "project_screen"
TRACK_LIST_TAB_NAME = "track_list_tab"
PROJECT_EDITION_PAGE_NAME = "project_edition_page"
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


def fake_startup_screen():
    return fake_widget(STARTUP_SCREEN_NAME)


def fake_project_screen(*_):
    return FakeProjectScreen()


class FakeProjectScreen(FakeWidget):
    current_page = None

    def __init__(self):
        super().__init__(PROJECT_SCREEN_NAME)

    def to_project_edition_page(self):
        self.current_page = PROJECT_EDITION_PAGE_NAME

    def to_track_page(self, index):
        self.current_page = track_edition_page_name(index + 1)

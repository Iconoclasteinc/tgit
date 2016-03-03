# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenu, QTableWidget
from hamcrest import contains, has_items, equal_to

from cute import gestures
from cute.matchers import named
from cute.widgets import MenuDriver, TableViewDriver
from tgit.ui.pages.track_list_page import TrackListPage
from ._screen_driver import ScreenDriver


def track_list_page(parent):
    return TrackListPageDriver.find_single(parent, TrackListPage, named("track_list_page"))


def no_track_list_page(parent):
    return TrackListPageDriver.find_none(parent, TrackListPage, named("track_list_page"))


class TrackListPageDriver(ScreenDriver):
    def __init__(self, selector, prober, gesture_performer):
        super().__init__(selector, prober, gesture_performer)

    def shows_column_headers(self, *headers):
        self._track_table().has_headers(contains(*headers))

    def shows_track_details(self, *details):
        return self._track_table().has_row(has_items(*details))

    def has_selected_track(self, *cells):
        return self._track_table().has_selected_row(has_items(*cells))

    def shows_tracks_in_order(self, *tracks):
        rows = [has_items(*[column for column in track]) for track in tracks]
        return self._track_table().contains_rows(contains(*rows))

    def has_track_count(self, count):
        self._track_table().has_row_count(equal_to(count))

    def add_tracks(self):
        self.button(named("_add_tracks_button")).click()

    def has_context_menu_item(self, matching):
        context_menu = self._from_context_menu()
        context_menu.has_menu_item(matching)
        context_menu.close()

    @property
    def remove_button(self):
        return self.button(named("_remove_track_button"))

    @property
    def move_up_button(self):
        return self.button(named("_move_track_up_button"))

    @property
    def move_down_button(self):
        return self.button(named("_move_track_down_button"))

    def has_disabled_play_context_menu_item(self, title):
        self.select_track(title)
        self._from_context_menu().menu_item(named("_play_action")).is_disabled()

    def _from_context_menu(self):
        self.perform(gestures.mouse_right_click())
        return MenuDriver.find_single(self, QMenu, named("context_menu"))

    def select_track(self, title):
        row = self.shows_track_details(title)
        self._track_table().click_on_cell(row, 0)

    def play_track(self, title):
        self.select_track(title)
        self._from_context_menu().select_menu_item(named("_play_action"))

    def stop_track(self, title):
        self.select_track(title)
        self._from_context_menu().select_menu_item(named("_stop_action"))

    def remove_selected_track(self, using="shortcut"):
        if using == "shortcut":
            self.perform(gestures.delete_previous())
        elif using == "menu":
            self._from_context_menu().select_menu_item(named("_remove_action"))
        elif using == "button":
            self.remove_button.click()
        else:
            raise AssertionError("Don't know how to remove a track using {}", using)

    def remove_track(self, title):
        self.select_track(title)
        self.remove_selected_track()

    def move_track(self, title, to):
        from_ = self.shows_track_details(title)
        self._track_table().move_row(from_, to)

    def move_track_up(self):
        self.move_up_button.click()

    def move_track_down(self):
        self.move_down_button.click()

    def _track_table(self):
        table = TableViewDriver.find_single(self, QTableWidget, named('_track_table'))
        table.is_showing_on_screen()
        return table

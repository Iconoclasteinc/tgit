# -*- coding: utf-8 -*-
from hamcrest import contains, has_items, equal_to
from PyQt5.QtWidgets import QMenu, QTableWidget

from cute import gestures
from cute.widgets import MenuDriver, TableViewDriver, WidgetDriver
from cute.matchers import named, showing_on_screen
from tgit.ui.album_composition_page import AlbumCompositionPage
from ._screen_driver import ScreenDriver


def album_composition_page(parent):
    return AlbumCompositionPageDriver.find_single(parent, AlbumCompositionPage, named('album_composition_page'))


class AlbumCompositionPageDriver(ScreenDriver):
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
        self.button(named('_add_tracks_button')).click()

    def has_context_menu_item(self, matching):
        context_menu = self._from_context_menu()
        context_menu.has_menu_item(matching)
        context_menu.close()

    def _from_context_menu(self):
        self.perform(gestures.mouse_right_click())
        return MenuDriver.find_single(self, QMenu, named("context_menu"))

    def select_track(self, title):
        row = self.shows_track_details(title)
        self._track_table().click_on_cell(row, 0)

    def play_track(self, title):
        self.select_track(title)
        self._from_context_menu().select_menu_item(named("_play_action"))

    def cannot_play_track(self, title):
        self.select_track(title)
        self._from_context_menu().menu_item(named("_play_action")).is_disabled()

    def remove_track(self, title, using_shortcut=False):
        self.select_track(title)
        if using_shortcut:
            self.perform(gestures.delete())
        else:
            self._from_context_menu().select_menu_item(named("_remove_action"))

    def move_track(self, title, to):
        from_ = self.shows_track_details(title)
        self._track_table().move_row(from_, to)

    def _track_table(self):
        table = TableViewDriver.find_single(self, QTableWidget, named('_track_table'))
        # todo we need to remove the overloded is_ and manipulate on TableViewDriver, they break
        # non table matchers
        WidgetDriver.is_(table, showing_on_screen())
        return table

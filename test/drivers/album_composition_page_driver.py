# -*- coding: utf-8 -*-
from hamcrest import contains, has_items, equal_to
from PyQt5.QtWidgets import QMenu

from cute.widgets import MenuDriver
from cute.matchers import named
from tgit.ui.album_composition_page import AlbumCompositionPage
from ._screen_driver import ScreenDriver


def album_composition_page(parent):
    return AlbumCompositionPageDriver.find_single(parent, AlbumCompositionPage, named('album-composition-page'))


class AlbumCompositionPageDriver(ScreenDriver):
    def __init__(self, selector, prober, gesture_performer):
        super(AlbumCompositionPageDriver, self).__init__(selector, prober, gesture_performer)

    def showsColumnHeaders(self, *headers):
        self._track_table().has_headers(contains(*headers))

    def shows_track(self, *cells):
        return self._track_table().has_row(has_items(*cells))

    def has_selected_track(self, *cells):
        return self._track_table().has_selected_row(has_items(*cells))

    def showsTracksInOrder(self, *tracks):
        rows = [has_items(*[column for column in track]) for track in tracks]
        return self._track_table().contains_rows(contains(*rows))

    def hasTrackCount(self, count):
        self._track_table().has_row_count(equal_to(count))

    def add_tracks(self):
        self.button(named('add-tracks')).click()

    def has_context_menu_item(self, matching):
        context_menu = self._open_context_menu()
        context_menu.has_menu_item(matching)
        context_menu.close()

    def _open_context_menu(self):
        # since we can't trigger the popup through right click, force update the menu as if it was popped up
        self.manipulate('update context menu', lambda page: page._update_context_menu())
        context_menu = MenuDriver.find_single(self, QMenu, named("context_menu"))
        context_menu.open()
        return context_menu

    def select_track(self, title):
        row = self.shows_track(title)
        self._track_table().click_on_cell(row, 0)

    def _play_from_context_menu(self):
        context_menu = self._open_context_menu()
        context_menu.select_menu_item(named("play_action"))

    def play_track(self, title):
        self.select_track(title)
        self._play_from_context_menu()

    def cannot_play_track(self, title):
        self.select_track(title)
        context_menu = self._open_context_menu()
        context_menu.menu_item(named("play_action")).is_disabled()

    def _delete_from_context_menu(self):
        context_menu = self._open_context_menu()
        context_menu.select_menu_item(named("delete_action"))

    def remove_track(self, title):
        self.select_track(title)
        self._delete_from_context_menu()

    def move_track(self, title, to):
        from_ = self.shows_track(title)
        self._track_table().move_row(from_, to)

    def _track_table(self):
        return self.table(named('track-list'))
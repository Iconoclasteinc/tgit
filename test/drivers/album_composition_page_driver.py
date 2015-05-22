# -*- coding: utf-8 -*-

from hamcrest import contains, has_items, equal_to
from PyQt5.QtWidgets import QAbstractButton

from cute.widgets import ButtonDriver
from cute.matchers import named
from test.drivers import ScreenDriver
from tgit.ui.album_composition_model import Columns
from tgit.ui.album_composition_page import AlbumCompositionPage


def album_composition_page(parent):
    return AlbumCompositionPageDriver.find_single(parent, AlbumCompositionPage, named('album-composition-page'))


class AlbumCompositionPageDriver(ScreenDriver):
    def __init__(self, selector, prober, gesture_performer):
        super(AlbumCompositionPageDriver, self).__init__(selector, prober, gesture_performer)

    def showsColumnHeaders(self, *titles):
        headers = [title for title in titles]
        self._track_table().has_headers(contains(*headers))

    def shows_track(self, *columns):
        cells = [column for column in columns]
        return self._track_table().has_row(has_items(*cells))

    def showsTracksInOrder(self, *tracks):
        rows = [has_items(*[column for column in track]) for track in tracks]
        return self._track_table().contains_rows(contains(*rows))

    def hasTrackCount(self, count):
        self._track_table().has_row_count(equal_to(count))

    def play(self, title):
        row = self.shows_track(title)
        self._play_button_at(row).is_showing_on_screen()
        self.clickPlayButtonAt(row)

    def add_tracks(self):
        self.button(named('add-tracks')).click()

    def remove_track(self, title):
        row = self.shows_track(title)
        self._click_remove_button(row)

    def move_track(self, title, to):
        from_ = self.shows_track(title)
        self._track_table().move_row(from_, to)

    def _remove_button_at(self, row):
        return ButtonDriver.find_single(self.removeWidget(row), QAbstractButton, named('remove-track'))

    def removeWidget(self, index):
        return self._track_table().widget_in_cell(index, Columns.index(Columns.remove))

    def _click_remove_button(self, row):
        self._remove_button_at(row).is_showing_on_screen()
        self._track_table().click_on_cell(row, Columns.index(Columns.remove))

    def _play_button_at(self, index):
        return ButtonDriver.find_single(self.playWidget(index), QAbstractButton, named('play-track'))

    def playWidget(self, index):
        return self._track_table().widget_in_cell(index, Columns.index(Columns.play))

    def clickPlayButtonAt(self, row):
        self._track_table().click_on_cell(row, Columns.index(Columns.play))

    def _track_table(self):
        return self.table(named('track-list'))

    def enables_playback_of(self, track_title):
        row = self.shows_track(track_title)
        self._play_button_at(row).is_enabled()

    def disables_playback_of(self, track_title):
        row = self.shows_track(track_title)
        self._play_button_at(row).is_disabled()

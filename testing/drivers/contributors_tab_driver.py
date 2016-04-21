# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidget
from hamcrest import contains, equal_to, has_items

from ._screen_driver import ScreenDriver
from cute.matchers import named
from cute.widgets import TableViewDriver, ComboBoxDriver


class ContributorsTabDriver(ScreenDriver):
    NAME_CELL_INDEX = 0
    ROLE_CELL_INDEX = 1
    IPI_CELL_INDEX = 2
    ISNI_CELL_INDEX = 3

    def shows_column_headers(self, *headers):
        self._table.has_headers(contains(*headers))

    def has_contributors_count(self, count):
        self._table.has_row_count(equal_to(count))

    def add_contributor(self):
        self._add_button.click()

    def has_added_empty_row(self):
        self._table.cell_is_readonly(self._empty_row_index, self.ISNI_CELL_INDEX)
        self._combo_in_cell(self._empty_row_index, self.ROLE_CELL_INDEX).has_options("", "Author", "Composer",
                                                                                     "Publisher")

    def remove_contributor_at(self, row):
        self._table.click_on_cell(row, self.NAME_CELL_INDEX)
        self._remove_button.click()

    def shows_remove_button(self, disabled=False):
        self._remove_button.is_disabled(disabled=disabled)

    def add_lyricist(self, name):
        self._add_button.click()
        self._table.edit_cell(self._empty_row_index, self.NAME_CELL_INDEX, name)
        self._combo_in_cell(self._empty_row_index, self.ROLE_CELL_INDEX).select_option("Author")

    def change_name_at_row(self, name, row):
        self._table.edit_cell(row, self.NAME_CELL_INDEX, name)

    def shows_isni_at_row(self, isni, row):
        self._table.has_value_in_cell(equal_to(isni), row, self.ISNI_CELL_INDEX)

    def shows_ipi_at_row(self, ipi, row):
        self._table.has_value_in_cell(equal_to(ipi), row, self.IPI_CELL_INDEX)

    def _combo_in_cell(self, row, col):
        widget_driver = self._table.widget_in_cell(row, col)
        return ComboBoxDriver(widget_driver.selector, self.prober, self.gesture_performer)

    @property
    def _empty_row_index(self):
        return self._table.has_row(has_items(None, None, None, None))

    @property
    def _table(self):
        table = TableViewDriver.find_single(self, QTableWidget, named("_contributors_table"))
        table.is_showing_on_screen()
        return table

    @property
    def _add_button(self):
        return self.button(named("_add_button"))

    @property
    def _remove_button(self):
        return self.button(named("_remove_button"))

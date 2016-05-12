# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidget
from hamcrest import contains, has_items, equal_to, has_item

from ._screen_driver import ScreenDriver
from cute.matchers import named, showing_on_screen
from cute.widgets import TableViewDriver, ComboBoxDriver
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab


def chain_of_title_tab(parent):
    return ChainOfTitleTabDriver.find_single(parent, ChainOfTitleTab, showing_on_screen())


class ChainOfTitleTabDriver(ScreenDriver):
    CONTRIBUTOR_AFFILIATION_CELL_INDEX = 1
    CONTRIBUTOR_PUBLISHERS_CELL_INDEX = 2
    CONTRIBUTOR_SHARE_CELL_INDEX = 3
    PUBLISHER_AFFILIATION_CELL_INDEX = 1
    PUBLISHER_SHARE_CELL_INDEX = 2

    def shows_contributors_column_headers(self, *headers):
        self._shows_column_headers(self._contributors_table, *headers)

    def shows_publishers_column_headers(self, *headers):
        self._shows_column_headers(self._publishers_table, *headers)

    def shows_contributor_row_details(self, *details):
        return self._shows_row_details(self._contributors_table, *details)

    def shows_publisher_row_details(self, *details):
        return self._shows_row_details(self._publishers_table, *details)

    def has_contributors_count(self, count):
        self._contributors_table.has_row_count(equal_to(count))

    def has_publishers_count(self, count):
        self._publishers_table.has_row_count(equal_to(count))

    def shows_affiliation_options_for_contributor(self, name, *affiliations):
        row = self._contributors_table.has_row(has_item(name))
        self._combo_in_cell(self._contributors_table, row, self.CONTRIBUTOR_AFFILIATION_CELL_INDEX).has_options(
            *affiliations)

    def shows_affiliation_options_for_publisher(self, name, *affiliations):
        row = self._publishers_table.has_row(has_item(name))
        self._combo_in_cell(self._publishers_table, row, self.CONTRIBUTOR_AFFILIATION_CELL_INDEX).has_options(
            *affiliations)

    def shows_affiliation_of_contributor(self, name, affiliation):
        row = self._contributors_table.has_row(has_item(name))
        self._combo_in_cell(self._contributors_table, row, self.CONTRIBUTOR_AFFILIATION_CELL_INDEX).has_current_text(
            affiliation)

    def shows_affiliation_of_publisher(self, name, affiliation):
        row = self._publishers_table.has_row(has_item(name))
        self._combo_in_cell(self._publishers_table, row, self.PUBLISHER_AFFILIATION_CELL_INDEX).has_current_text(
            affiliation)

    def change_affiliation_of_contributor(self, name, affiliation):
        row = self._contributors_table.has_row(has_item(name))
        self._combo_in_cell(self._contributors_table, row, self.CONTRIBUTOR_AFFILIATION_CELL_INDEX).select_option(
            affiliation)

    def change_affiliation_of_publisher(self, name, affiliation):
        row = self._publishers_table.has_row(has_item(name))
        self._combo_in_cell(self._publishers_table, row, self.PUBLISHER_AFFILIATION_CELL_INDEX).select_option(
            affiliation)

    def shows_publisher_options_on_row(self, row, *publishers):
        self._combo_in_cell(self._contributors_table, row, self.CONTRIBUTOR_PUBLISHERS_CELL_INDEX).has_options(
            *publishers)

    def shows_publisher_of_contributor(self, name, publisher):
        row = self._contributors_table.has_row(has_item(name))
        self._combo_in_cell(self._contributors_table, row, self.CONTRIBUTOR_PUBLISHERS_CELL_INDEX).has_current_text(
            publisher)

    def change_publisher_of_contributor(self, name, publisher):
        row = self._contributors_table.has_row(has_item(name))
        self._combo_in_cell(self._contributors_table, row, self.CONTRIBUTOR_PUBLISHERS_CELL_INDEX).select_option(
            publisher)

    def change_share_of_contributor(self, name, share):
        row = self._contributors_table.has_row(has_item(name))
        self._contributors_table.edit_cell(row, self.CONTRIBUTOR_SHARE_CELL_INDEX, share)

    def change_share_of_publisher(self, name, share):
        row = self._publishers_table.has_row(has_item(name))
        self._publishers_table.edit_cell(row, self.PUBLISHER_SHARE_CELL_INDEX, share)

    @staticmethod
    def _shows_row_details(table, *details):
        row = table.has_row(has_items(*details))
        table.cell_is_readonly(row, 0)

        return row

    @staticmethod
    def _shows_column_headers(table, *headers):
        table.has_headers(contains(*headers))

    def _combo_in_cell(self, table, row, col):
        widget_driver = table.widget_in_cell(row, col)
        return ComboBoxDriver(widget_driver.selector, self.prober, self.gesture_performer)

    @property
    def _contributors_table(self):
        table = TableViewDriver.find_single(self, QTableWidget, named("_contributors_table"))
        table.is_showing_on_screen()
        return table

    @property
    def _publishers_table(self):
        table = TableViewDriver.find_single(self, QTableWidget, named("_publishers_table"))
        table.is_showing_on_screen()
        return table

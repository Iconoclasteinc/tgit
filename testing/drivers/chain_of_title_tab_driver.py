# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidget
from hamcrest import contains, has_items, equal_to

from ._screen_driver import ScreenDriver
from cute.matchers import named, showing_on_screen
from cute.widgets import TableViewDriver
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab


def chain_of_title_tab(parent):
    return ChainOfTitleTabDriver.find_single(parent, ChainOfTitleTab, showing_on_screen())


class ChainOfTitleTabDriver(ScreenDriver):
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

    @staticmethod
    def _shows_row_details(table, *details):
        row = table.has_row(has_items(*details))
        table.cell_is_readonly(row, 0)

        return row

    @staticmethod
    def _shows_column_headers(table, *headers):
        table.has_headers(contains(*headers))

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

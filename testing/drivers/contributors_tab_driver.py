# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidget
from hamcrest import contains, equal_to, has_items

from ._screen_driver import ScreenDriver
from cute.matchers import named, showing_on_screen
from cute.widgets import TableViewDriver, ComboBoxDriver
from tgit.ui.pages.contributors_tab import ContributorsTab


def contributor_tab(parent):
    return ContributorsTabDriver.find_single(parent, ContributorsTab, showing_on_screen())


class ContributorsTabDriver(ScreenDriver):
    NAME_CELL_INDEX = 0
    ROLE_CELL_INDEX = 1
    IPI_CELL_INDEX = 2
    ISNI_CELL_INDEX = 3

    def shows_column_headers(self, *headers):
        self._table.has_headers(contains(*headers))

    def shows_row_details(self, *details):
        return self._table.has_row(has_items(*details))

    def shows_role_on_row(self, row, role):
        self._combo_in_cell(row, self.ROLE_CELL_INDEX).has_current_text(role)

    def has_contributors_count(self, count):
        self._table.has_row_count(equal_to(count))

    def add_contributor(self):
        self._add_button.click()

    def has_added_empty_row(self):
        row = self._has_empty_row()
        self._table.cell_is_readonly(row, self.ISNI_CELL_INDEX)
        self._combo_in_cell(row, self.ROLE_CELL_INDEX).has_options("", "Author", "Composer", "Publisher")

    def remove_contributor_at(self, row):
        self._table.click_on_cell(row, self.NAME_CELL_INDEX)
        self._remove_button.click()

    def shows_remove_button(self, disabled=False):
        self._remove_button.is_disabled(disabled=disabled)

    def add_lyricist(self, name):
        row = self._add_collaborator(name)
        self._combo_in_cell(row, self.ROLE_CELL_INDEX).select_option("Author")

    def add_composer(self, name):
        row = self._add_collaborator(name)
        self._combo_in_cell(row, self.ROLE_CELL_INDEX).select_option("Composer")

    def add_publisher(self, name):
        row = self._add_collaborator(name)
        self._combo_in_cell(row, self.ROLE_CELL_INDEX).select_option("Publisher")

    def _add_collaborator(self, name):
        self._add_button.click()
        row = self._has_empty_row()
        self._table.edit_cell(row, self.NAME_CELL_INDEX, name)
        return row

    def change_name_at_row(self, name, row):
        self._table.edit_cell(row, self.NAME_CELL_INDEX, name)

    def change_ipi_at_row(self, ipi, row):
        self._table.edit_cell(row, self.IPI_CELL_INDEX, ipi)

    def shows_isni_at_row(self, isni, row):
        self._table.has_value_in_cell(equal_to(isni), row, self.ISNI_CELL_INDEX)

    def shows_ipi_at_row(self, ipi, row):
        self._table.has_value_in_cell(equal_to(ipi), row, self.IPI_CELL_INDEX)

    def _combo_in_cell(self, row, col):
        widget_driver = self._table.widget_in_cell(row, col)
        return ComboBoxDriver(widget_driver.selector, self.prober, self.gesture_performer)

    def _has_empty_row(self):
        return self._table.has_row(contains(None, None, None, None))

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

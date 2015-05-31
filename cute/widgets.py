# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QDir, QPoint, Qt, QTime, QDate
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QListView,
                             QToolButton, QFileDialog, QMenu, QComboBox, QMessageBox, QTextEdit, QLabel,
                             QAbstractButton, QSpinBox, QTableView)
from hamcrest import all_of, equal_to
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from . import gestures, properties, matchers as match
from .probes import (WidgetManipulatorProbe, WidgetAssertionProbe, WidgetPropertyAssertionProbe,
                     WidgetScreenBoundsProbe)
from .finders import (SingleWidgetFinder, TopLevelWidgetsFinder, RecursiveWidgetFinder, NthWidgetFinder, WidgetSelector,
                      WidgetIdentity)


windows = sys.platform == 'win32'


def all_top_level_widgets():
    return TopLevelWidgetsFinder(QApplication.instance())


def only_widget(of_type, matching):
    return SingleWidgetFinder(RecursiveWidgetFinder(of_type, matching, all_top_level_widgets()))


def main_application_window(*matchers):
    return only_widget(QMainWindow, all_of(*matchers))


def window(of_type, *matchers):
    return only_widget(of_type, all_of(*matchers))


class WidgetDriver:
    def __init__(self, selector, prober, gesture_performer):
        self.selector = selector
        self.prober = prober
        self.gesture_performer = gesture_performer

    @classmethod
    def find_single(cls, parent, widget_type, *matchers):
        return cls(SingleWidgetFinder(
            RecursiveWidgetFinder(widget_type, all_of(*matchers), parent.selector)), parent.prober,
            parent.gesture_performer)

    @classmethod
    def find_nth(cls, parent, widget_type, index, *matchers):
        return cls(NthWidgetFinder(
            RecursiveWidgetFinder(widget_type, all_of(*matchers), parent.selector), index),
            parent.prober, parent.gesture_performer)

    def exists(self):
        self.is_(match.existing())

    def is_showing_on_screen(self):
        self.is_(match.showing_on_screen())

    def is_hidden(self):
        self.is_(match.hidden())

    def is_enabled(self, enabled=True):
        self.is_(enabled and match.enabled() or match.disabled())

    def is_disabled(self, disabled=True):
        self.is_enabled(not disabled)

    def is_(self, criteria):
        self.check(WidgetAssertionProbe(self.selector, criteria))

    def has_cursor_shape(self, shape):
        self.has(properties.cursor_shape(), wrap_matcher(shape))

    def has(self, query, criteria):
        self.check(WidgetPropertyAssertionProbe(self.selector, query, criteria))

    def manipulate(self, description, manipulation):
        self.check(WidgetManipulatorProbe(self.selector, manipulation, description))

    def widget_center(self):
        return self.widget_bounds().center()

    def widget_bounds(self):
        probe = WidgetScreenBoundsProbe(self.selector)
        self.check(probe)
        return probe.bounds

    def click(self):
        return self.left_click_on_widget()

    def left_click_on_widget(self):
        self.is_showing_on_screen()
        self.perform(gestures.mouse_click_at(self.widget_center()))

    def enter(self):
        self.perform(gestures.enter())

    def perform(self, *gestures):
        self.gesture_performer.perform(*gestures)

    def check(self, probe):
        self.prober.check(probe)

    def close(self):
        self.manipulate("close", lambda widget: widget.close())

    def clear_focus(self):
        self.manipulate("clear focus", lambda widget: widget.clearFocus())

    def pause(self, ms):
        self.perform(gestures.pause(ms))


class ButtonDriver(WidgetDriver):
    def click(self):
        self.is_enabled()
        super().click()

    def has_text(self, matcher):
        self.has(properties.text(), wrap_matcher(matcher))

    def is_unchecked(self, unchecked=True):
        self.is_checked(not unchecked)

    def is_checked(self, checked=True):
        self.is_showing_on_screen()
        self.is_(checked and match.checked() or match.unchecked())


class LabelDriver(WidgetDriver):
    def has_text(self, matcher):
        self.has(properties.text(), wrap_matcher(matcher))

    def has_pixmap(self, matcher):
        self.has(properties.label_pixmap(), matcher)


class AbstractEditDriver(WidgetDriver):
    EDITION_DELAY = 20

    def change_text(self, text):
        self.is_enabled()
        self.replace_all_text(text)
        self.enter()

    def replace_all_text(self, text):
        self.focus_with_mouse()
        self.clear_all_text()
        self.type(text)

    def focus_with_mouse(self):
        self.left_click_on_widget()

    def clear_all_text(self):
        self.select_all_text()
        self.perform(gestures.pause(self.EDITION_DELAY))
        self.delete_selected_text()

    def select_all_text(self):
        self.perform(gestures.select_all())

    def delete_selected_text(self):
        self.perform(gestures.delete_previous())

    def type(self, text):
        self.perform(gestures.type_text(text))


class LineEditDriver(AbstractEditDriver):
    def has_text(self, text):
        self.has(properties.input_text(), equal_to(text))


class TextEditDriver(AbstractEditDriver):
    MULTILINE_DELAY = 10

    def has_plain_text(self, text):
        self.has(properties.plain_text(), equal_to(text))

    def add_line(self, text):
        self.focus_with_mouse()
        self.type(text)
        self.perform(gestures.enter())
        self.pause(self.MULTILINE_DELAY)


class QAbstractSpinBoxDriver(AbstractEditDriver):
    pass


class ComboBoxDriver(AbstractEditDriver):
    CHOICES_DISPLAY_DELAY = 250

    def select_option(self, matching):
        options_list = self._open_options_list()
        self.pause(self.CHOICES_DISPLAY_DELAY)
        options_list.select_item(match.with_list_item_text(matching))

    def _open_options_list(self):
        self.manipulate("pop up", lambda w: w.showPopup())
        return ListViewDriver.find_single(self, QListView)

    def has_current_text(self, matching):
        self.has(properties.current_text(), wrap_matcher(matching))


def _right_edge_of(rect):
    return QPoint(rect.right(), rect.center().y())


class DateTimeEditDriver(WidgetDriver):
    CALENDAR_DISPLAY_DELAY = 250

    def display_format(self):
        class QueryDisplayFormat:
            def __call__(self, date_time_edit):
                self.display_format = date_time_edit.displayFormat()

        query = QueryDisplayFormat()
        self.manipulate("query display format", query)
        return query.display_format

    def has_date(self, date):
        self.has(properties.date(), equal_to(QDate.fromString(date, self.display_format())))

    def has_time(self, time):
        self.has(properties.time(), equal_to(QTime.fromString(time, self.display_format())))

    def change_date(self, year, month, day):
        self._popup_calendar()
        self.pause(self.CALENDAR_DISPLAY_DELAY)
        self._calendar().select_date(year, month, day)

    def _popup_calendar(self):
        self.perform(gestures.mouse_click_at(_right_edge_of(self.widget_bounds())))

    def _calendar(self):
        def find_calendar_widget(date_edit):
            nonlocal calendar
            calendar = date_edit.calendarWidget()

        calendar = None
        self.manipulate("find calendar widget", find_calendar_widget)

        return QCalendarDriver(WidgetIdentity(calendar), self.prober, self.gesture_performer)


class QCalendarDriver(WidgetDriver):
    MENU_DISPLAY_DELAY = 250

    def select_date(self, year, month, day):
        self.select_year(year)
        self.select_month(month)
        self.select_day(day)

    def select_year(self, year):
        self._year_button().click()
        self._year_spinner().type(str(year))
        self.perform(gestures.enter())

    def select_month(self, month):
        # Clicking the toolbutton blocks the execution, so pop up menu manually
        bottom_left = self._month_button().widget_bounds().bottomLeft()
        self._month_menu().open_at(bottom_left.x(), bottom_left.y())

        self.pause(self.MENU_DISPLAY_DELAY)
        self._month_menu().select_menu_item(match.with_data(month))

    def select_day(self, day):
        row, col = self._find_day(day)
        self._table().click_on_cell(row, col)

    def _year_button(self):
        return ButtonDriver.find_single(self, QAbstractButton, match.named("qt_calendar_yearbutton"))

    def _year_spinner(self):
        return QAbstractSpinBoxDriver.find_single(self, QSpinBox, match.named("qt_calendar_yearedit"))

    def _month_button(self):
        return ButtonDriver.find_single(self, QAbstractButton, match.named("qt_calendar_monthbutton"))

    def _month_menu(self):
        def find_month_menu(calendar):
            nonlocal month_menu
            month_menu = calendar.findChild(QToolButton, "qt_calendar_monthbutton").menu()

        month_menu = None
        self.manipulate("find month selector menu", find_month_menu)
        return MenuDriver(WidgetIdentity(month_menu), self.prober, self.gesture_performer)

    def _table(self):
        def find_calendar_table(calendar):
            nonlocal table_view
            table_view = calendar.findChild(QTableView, "qt_calendar_calendarview")

        table_view = None
        self.manipulate("find calendar table", find_calendar_table)
        return TableViewDriver(WidgetIdentity(table_view), self.prober, self.gesture_performer)

    def _find_day(self, day):
        class FindDayInCalendar:
            def __call__(self, table):
                def day_at(row, col):
                    return str(table.model().data(table.model().index(row, col)))

                def find_position_of_day_in_calendar(which_day, from_row=0, from_col=0):
                    row = from_row
                    col = from_col

                    while row < 7:
                        while col < 7:
                            if str(which_day) == day_at(row, col):
                                return row, col
                            col += 1
                        row, col = row + 1, 0

                    return -1, -1

                self.row, self.col = find_position_of_day_in_calendar(day, *find_position_of_day_in_calendar(1))

        find_position = FindDayInCalendar()
        self._table().manipulate("find position of day '{0}' in calendar".format(day), find_position)
        return find_position.row, find_position.col


class FileDialogDriver(WidgetDriver):
    DISPLAY_DELAY = 500 if windows else 250
    INITIAL_SETUP_DELAY = 1000 if windows else 0

    def show_hidden_files(self):
        def show_dialog_hidden_files(dialog):
            dialog.setFilter(dialog.filter() | QDir.Hidden)

        self.manipulate("show hidden files", show_dialog_hidden_files)

    def view_as_list(self):
        def set_list_view_mode(dialog):
            dialog.setViewMode(QFileDialog.List)

        self.manipulate("set the view mode to list", set_list_view_mode)

    def navigate_to_dir(self, path):
        self.pause(self.INITIAL_SETUP_DELAY)
        for folder_name in self._navigation_path_to(path):
            if folder_name == '':
                pass
            elif folder_name == '..':
                self.up_one_folder()
            else:
                self.into_folder(folder_name)

    def _navigation_path_to(self, path):
        return self._current_dir().relativeFilePath(path).split('/')

    def _current_dir(self):
        class FindOutCurrentFolder:
            def __call__(self, dialog):
                self.name = dialog.directory()

        find_folder = FindOutCurrentFolder()
        self.manipulate("find out current folder", find_folder)
        return find_folder.name

    def into_folder(self, name):
        self.select_file(name)
        self.enter()

    def filter_files_of_type(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.select_option(matching)

    def select_file(self, name):
        self.select_files(name)

    def select_files(self, *names):
        self.pause(self.DISPLAY_DELAY)
        self._list_view().select_items(*[match.with_list_item_text(name) for name in names])

    def up_one_folder(self):
        up_button = ButtonDriver.find_single(self, QToolButton, match.named("toParentButton"))
        up_button.click()

    def enter_manually(self, filename):
        self._filename_edit().replace_all_text(filename)

    def accept(self):
        self._accept_button().click()

    def has_accept_button(self, criteria):
        return self._accept_button().is_(criteria)

    def has_accept_button_text(self, text):
        return self._accept_button().has_text(text)

    def reject(self):
        return self._reject_button().click()

    def has_reject_button(self, criteria):
        return self._reject_button().is_(criteria)

    def has_reject_button_text(self, text):
        return self._reject_button().has_text(text)

    def _list_view(self):
        return ListViewDriver.find_single(self, QListView, match.named("listView"))

    def _filename_edit(self):
        return LineEditDriver.find_single(self, QLineEdit, match.named("fileNameEdit"))

    def _accept_button(self):
        return self._dialog_button(QFileDialog.Accept)

    def _reject_button(self):
        return self._dialog_button(QFileDialog.Reject)

    def _dialog_button(self, label):
        class QueryButtonText:
            def __call__(self, dialog):
                self.text = dialog.labelText(label)

        query = QueryButtonText()
        self.manipulate('query button text', query)
        return ButtonDriver.find_single(self, QPushButton, match.with_text(query.text))

    def has_selected_file_type(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.has_current_text(matching)

    def _has_file_type_options_count(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.has(properties.count(), wrap_matcher(matching))

    def has_file_type_options(self, *options):
        for index, option in enumerate(options):
            self._has_file_type_option(option, index=index)
        self._has_file_type_options_count(len(options))

    def _has_file_type_option(self, option, *, index):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.has(properties.has_option_text(index), wrap_matcher(option))


class ListViewDriver(WidgetDriver):
    def select_item(self, matching):
        self.select_items(matching)

    def select_items(self, *matchers):
        self._select_items([self._index_of_first_item(matching) for matching in matchers])

    def _select_items(self, indexes):
        self._select_item(indexes.pop(0))
        for index in indexes:
            self._multi_select_item(index)

    def _multi_select_item(self, index):
        self._scroll_item_to_visible(index)
        self.perform(gestures.mouse_multi_click_at(self._center_of_item(index)))

    def _select_item(self, index):
        self._scroll_item_to_visible(index)
        self.perform(gestures.mouse_click_at(self._center_of_item(index)))

    def _scroll_item_to_visible(self, index):
        self.manipulate("scroll item to visible", lambda listView: listView.scrollTo(index))

    def _center_of_item(self, index):
        class CalculateCenterOfItem:
            def __call__(self, list_view):
                item_visible_area = list_view.visualRect(index)
                self.pos = list_view.mapToGlobal(item_visible_area.center())

        calculate_center = CalculateCenterOfItem()
        self.manipulate("calculate center of item", calculate_center)
        return calculate_center.pos

    def _index_of_first_item(self, matching):
        class ContainingMatchingItem(BaseMatcher):
            def _matches(self, list_view):
                model = list_view.model()
                root = list_view.rootIndex()
                item_count = model.rowCount(root)
                for i in range(item_count):
                    index = model.index(i, 0, root)
                    if matching.matches(index):
                        self.at_index = index
                        return True

                return False

            def describe_to(self, description):
                description.append_text("containing an item ")
                matching.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained no item ")
                matching.describe_to(mismatch_description)

        containing_item = ContainingMatchingItem()
        self.is_(containing_item)
        return containing_item.at_index


class QMenuBarDriver(WidgetDriver):
    def menu(self, matching):
        # First we have to make sure the menu actually exists on the menu bar
        self.has_menu(matching)

        # QMenuBar on Mac OS X is a wrapper for using the system-wide menu bar
        # so we cannot just click on it, we have to pop it up manually
        menu_driver = TopLevelQMenuDriver.find_single(self, QMenu, matching)
        return menu_driver

    def has_menu(self, matching):
        class ContainingMatchingMenu(BaseMatcher):
            def _matches(self, menu_bar):
                for menu in [action.menu() for action in menu_bar.actions()]:
                    if matching.matches(menu):
                        return True
                return False

            def describe_to(self, description):
                description.append_text("containing a menu ")
                matching.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained no menu ")
                matching.describe_to(mismatch_description)

        self.is_(ContainingMatchingMenu())


class MenuDriver(WidgetDriver):
    def open(self):
        # For some unknown reason, menu does not pop up on right click on Mac
        # self.perform(gestures.mouse_click(gestures.RIGHT_BUTTON))
        self.open_at(*self.gesture_performer.mouse_position)

    def open_at(self, x, y):
        # For some reason, we can't open the menu by just right clicking, so open it manually
        self.manipulate("open at ({0}, {1})".format(x, y), lambda menu: menu.popup(QPoint(x, y)))

    def menu_item(self, matching):
        # We have to make sure the item menu actually exists in the menu
        # Checking that the item is a child of the menu is not sufficient
        action = self.has_menu_item(matching)
        return MenuItemDriver(WidgetIdentity(action), self.prober, self.gesture_performer)

    def select_menu_item(self, matching):
        menu_item = self.menu_item(matching)
        menu_item.click()

    def has_menu_item(self, matching):
        class ContainingMatchingMenuItem(BaseMatcher):
            def _matches(self, menu):
                for action in menu.actions():
                    if matching.matches(action):
                        self.action = action
                        return True
                return False

            def describe_to(self, description):
                description.append_text("containing an item ")
                matching.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained no item ")
                matching.describe_to(mismatch_description)

        containing_menu_item = ContainingMatchingMenuItem()
        self.is_(containing_menu_item)
        return containing_menu_item.action


class TopLevelQMenuDriver(MenuDriver):
    def open(self):
        class FindPositionInMenuBar:
            def __call__(self, menu):
                menu_bar = menu.parent()
                menu_title_visible_area = menu_bar.actionGeometry(menu.menuAction())
                # We try to pop up the menu at a position that makes sense on all platforms
                # i.e. just below the menu title
                self.coordinates = menu_bar.mapToGlobal(menu_title_visible_area.bottomLeft())

        find_position = FindPositionInMenuBar()
        self.manipulate("find position in menu bar", find_position)
        self.open_at(find_position.coordinates.x(), find_position.coordinates.y())


class MenuItemDriver(WidgetDriver):
    def _center_of_item(self):
        class CalculateCenterOfItem:
            def __call__(self, item):
                menu = item.associatedWidgets()[0]
                item_visible_area = menu.actionGeometry(item)
                self.coordinates = menu.mapToGlobal(item_visible_area.center())

        calculate_center = CalculateCenterOfItem()
        self.manipulate('calculate center of item', calculate_center)
        return calculate_center.coordinates

    def click(self):
        self.is_enabled()
        self.perform(gestures.mouse_click_at(self._center_of_item()))


class QMessageBoxDriver(WidgetDriver):
    def shows_message(self, message):
        LabelDriver.find_single(self, QLabel, match.named("qt_msgbox_label")).has_text(message)

    def shows_details(self, details):
        TextEditDriver.find_single(self, QTextEdit).has_plain_text(details)

    def ok(self):
        self._dialog_button(QMessageBox.Ok).click()

    def yes(self):
        self._dialog_button(QMessageBox.Yes).click()

    def _dialog_button(self, role):
        button = None

        def query_button_role(message_box):
            nonlocal button
            button = message_box.button(role)

        self.manipulate("lookup button with role {0}".format(role), query_button_role)
        return ButtonDriver(WidgetIdentity(button), self.prober, self.gesture_performer)


class TableViewDriver(WidgetDriver):
    def has_headers(self, matching):
        class WithMatchingHeaders(BaseMatcher):
            @staticmethod
            def _headers(table):
                return [header_text(table, column) for column in range(column_count(table))]

            def _matches(self, table):
                return matching.matches(self._headers(table))

            def describe_to(self, description):
                description.append_text("with headers ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("headers ")
                matching.describe_mismatch(self._headers(table), mismatch_description)

        self.is_(WithMatchingHeaders())

    def has_row(self, matching):
        class WithMatchingRow(BaseMatcher):
            @staticmethod
            def _cells_of(table, row):
                return [cell_text(table, row, column) for column in range(column_count(table))]

            def _matches(self, table):
                for row in range(row_count(table)):
                    if matching.matches(self._cells_of(table, row)):
                        self.index = visual_row(table, row)
                        return True
                return False

            def describe_to(self, description):
                description.append_text("containing row ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("contained no row ")
                matching.describe_to(mismatch_description)

        with_matching_row = WithMatchingRow()
        self.is_(with_matching_row)
        return with_matching_row.index

    def contains_rows(self, matching):
        class WithMatchingRows(BaseMatcher):
            @staticmethod
            def _cells_in(table, row):
                return [cell_text(table, row, column) for column in range(column_count(table))]

            @staticmethod
            def _rows_in(table):
                rows = []
                for row in range(row_count(table)):
                    rows.append(WithMatchingRows._cells_in(table, row))
                return rows

            def _matches(self, table):
                return matching.matches(self._rows_in(table))

            def describe_to(self, description):
                description.append_text("with rows ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("rows ")
                matching.describe_mismatch(self._rows_in(table), mismatch_description)

        self.is_(WithMatchingRows())

    def scroll_cell_to_visible(self, row, column):
        class ScrollCellToVisible:
            def __call__(self, table):
                logical_row, logical_column = logical_cell(table, row, column)
                table.scrollTo(table.indexAt(QPoint(table.columnViewportPosition(logical_column),
                                                    table.rowViewportPosition(logical_row))))

        scroll_cell_to_visible = ScrollCellToVisible()
        self.manipulate("scroll cell ({0}, {1}) into view".format(row, column), scroll_cell_to_visible)

    def _click_at_cell_center(self, row, column):
        class CalculateCellPosition:
            @staticmethod
            def center_of_cell(table):
                logical_row, logical_column = logical_cell(table, row, column)
                row_offset = table.horizontalHeader().height() + table.rowViewportPosition(logical_row)
                column_offset = table.verticalHeader().width() + table.columnViewportPosition(logical_column)
                return QPoint(column_offset + table.columnWidth(column) / 2,
                              row_offset + table.rowHeight(row) / 2)

            def __call__(self, table):
                self.center = table.mapToGlobal(self.center_of_cell(table))

        calculate_position = CalculateCellPosition()
        self.manipulate("calculate cell ({0}, {1}) center position".format(row, column), calculate_position)
        self.perform(gestures.mouse_click_at(calculate_position.center))

    def click_on_cell(self, row, column):
        self.scroll_cell_to_visible(row, column)
        self._click_at_cell_center(row, column)

    def widget_in_cell(self, row, column):
        class WidgetInCell(WidgetSelector):
            def __init__(self, table_selector):
                super(WidgetInCell, self).__init__()
                self._table_selector = table_selector

            def describe_to(self, description):
                description.append_text("in cell ({0}, {1}) widget".format(row, column))
                description.append_text("\n    in ")
                description.append_description_of(self._table_selector)

            def describe_failure_to(self, description):
                self._table_selector.describe_failure_to(description)
                if self._table_selector.is_satisfied():
                    if self.is_satisfied():
                        description.append_text("\n    cell ({0}, {1})".format(row, column))
                    else:
                        description.append_text("\n    had no widget in cell ({0}, {1})".format(row, column))

            def widgets(self):
                if self.is_satisfied():
                    return self._widget_in_cell,
                else:
                    return ()

            def is_satisfied(self):
                return self._widget_in_cell is not None

            def test(self):
                self._table_selector.test()

                if not self._table_selector.is_satisfied():
                    self._widget_in_cell = None
                    return

                table = self._table_selector.widget()
                self._widget_in_cell = widget_at(table, row, column)

        return WidgetDriver(WidgetInCell(self.selector), self.prober, self.gesture_performer)

    def has_row_count(self, matching):
        class WithMatchingRowCount(BaseMatcher):
            def _matches(self, table):
                return matching.matches(row_count(table))

            def describe_to(self, description):
                description.append_text("with row count ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("row count ")
                matching.describe_mismatch(row_count(table), mismatch_description)

        self.is_(WithMatchingRowCount())

    def move_row(self, from_position, to_position):
        def move_row_to_new_position(table):
            table.verticalHeader().moveSection(logical_row(table, from_position),
                                               logical_row(table, to_position))

        # We'd like to use gestures but drag and drop is not supported by our Robot
        # so we have to use a manipulation
        self.manipulate("move row {0} to position {1}".format(from_position, to_position), move_row_to_new_position)


class TableWidgetDriver(TableViewDriver):
    def has_header_items(self, matching):
        class WithMatchingHeaders(BaseMatcher):
            @staticmethod
            def _header_items(table):
                return [table.horizontalHeaderItem(logical_column(table, column))
                        for column in range(table.columnCount())]

            def _matches(self, table):
                return matching.matches(self._header_items(table))

            def describe_to(self, description):
                description.append_text("with header items ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("header items ")
                matching.describe_mismatch(self._header_items(table), mismatch_description)

        self.is_(WithMatchingHeaders())

    def hasRowItems(self, matching):
        class WithMatchingRow(BaseMatcher):
            @staticmethod
            def _cell_items(table, row):
                return [table.item(row, column) for column in range(table.columnCount())]

            def _matches(self, table):
                for row in range(table.rowCount()):
                    if matching.matches(self._cell_items(table, row)):
                        self.index = table.visualRow(row)
                        return True
                return False

            def describe_to(self, description):
                description.append_text("containing row items ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("contained no items ")
                matching.describe_to(mismatch_description)

        with_matching_row = WithMatchingRow()
        self.is_(with_matching_row)
        return with_matching_row.index

    def contains_row_items(self, matching):
        class WithMatchingRowItems(BaseMatcher):
            @staticmethod
            def _cellItems(table, row):
                return [table.item(row, column) for column in range(table.columnCount())]

            @staticmethod
            def _rowsItems(table):
                rows = []
                for row in range(table.rowCount()):
                    rows.append(WithMatchingRowItems._cellItems(table, row))
                return rows

            def _matches(self, table):
                return matching.matches(self._rowsItems(table))

            def describe_to(self, description):
                description.append_text("with row items ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("row items ")
                matching.describe_mismatch(self._rowsItems(table), mismatch_description)

        self.is_(WithMatchingRowItems())


def logical_column(table, visual_column):
    return table.horizontalHeader().logicalIndex(visual_column)


def logical_row(table, visual_row):
    return table.verticalHeader().logicalIndex(visual_row)


def logical_cell(table, visual_row, visual_column):
    return logical_row(table, visual_row), logical_column(table, visual_column)


def cell_text(table, row, column):
    return table.model().data(table.model().index(row, column), Qt.DisplayRole)


def header_text(table, column):
    return table.model().headerData(column, Qt.Horizontal, Qt.DisplayRole)


def column_count(table):
    return table.model().columnCount()


def row_count(table):
    return table.model().rowCount()


def widget_at(table, row, column):
    return table.indexWidget(table.model().index(row, column))


def visual_row(table, logical_row):
    return table.verticalHeader().visualIndex(logical_row)

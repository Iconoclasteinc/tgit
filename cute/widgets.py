# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QDir, QPoint, Qt, QTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QListView,
                             QToolButton, QFileDialog, QMenu, QAction, QComboBox)
from hamcrest import all_of, equal_to

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from . import gestures, properties, keyboard_shortcuts as shortcuts, matchers as match
from .probes import (WidgetManipulatorProbe, WidgetAssertionProbe, WidgetPropertyAssertionProbe,
                     WidgetScreenBoundsProbe)
from .finders import (SingleWidgetFinder, TopLevelWidgetsFinder, RecursiveWidgetFinder, NthWidgetFinder, WidgetSelector)


windows = sys.platform == 'win32'


def all_top_level_widgets():
    return TopLevelWidgetsFinder(QApplication.instance())


def only_widget(of_type, matching):
    return SingleWidgetFinder(RecursiveWidgetFinder(of_type, matching, all_top_level_widgets()))


def main_application_window(*matchers):
    return only_widget(QMainWindow, all_of(*matchers))


def window(of_type, *matchers):
    return only_widget(of_type, all_of(*matchers))


class WidgetDriver(object):
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
        probe = WidgetScreenBoundsProbe(self.selector)
        self.check(probe)
        return probe.bounds.center()

    def click(self):
        return self.left_click_on_widget()

    def left_click_on_widget(self):
        self.is_showing_on_screen()
        self.perform(gestures.click_at(self.widget_center()))

    def enter(self):
        self.perform(shortcuts.ENTER)

    def perform(self, *gestures):
        self.gesture_performer.perform(*gestures)

    def check(self, probe):
        self.prober.check(probe)

    def close(self):
        self.manipulate('close', lambda widget: widget.close())

    def clear_focus(self):
        self.manipulate('clear focus', lambda widget: widget.clearFocus())

    def pause(self, ms):
        self.perform(gestures.pause(ms))


class MainWindowDriver(WidgetDriver):
    pass


class ButtonDriver(WidgetDriver):
    def click(self):
        self.is_enabled()
        WidgetDriver.click(self)

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
        self.perform(shortcuts.SELECT_ALL)

    def delete_selected_text(self):
        self.perform(shortcuts.DELETE_PREVIOUS)

    def type(self, text):
        self.perform(gestures.type_text(text))


class LineEditDriver(AbstractEditDriver):
    def has_text(self, text):
        self.has(properties.input_text(), equal_to(text))


class TextEditDriver(AbstractEditDriver):
    def has_plain_text(self, text):
        self.has(properties.plain_text(), equal_to(text))

    def add_line(self, text):
        self.focus_with_mouse()
        self.type(text)
        self.perform(shortcuts.ENTER)


class ComboBoxDriver(AbstractEditDriver):
    CHOICES_DISPLAY_DELAY = 250

    def select_option(self, matching):
        popup = self._popup()
        self.pause(self.CHOICES_DISPLAY_DELAY)
        popup.select_item(match.with_list_item_text(matching))

    def _popup(self):
        self.manipulate("pop up", lambda w: w.showPopup())
        return ListViewDriver.find_single(self, QListView)

    def has_current_text(self, matching):
        self.has(properties.current_text(), wrap_matcher(matching))


class DateTimeEditDriver(WidgetDriver):
    def has_time(self, time):
        class QueryDisplayFormat(object):
            def __call__(self, dateTimeEdit):
                self.result = dateTimeEdit.displayFormat()

        query_display_format = QueryDisplayFormat()
        self.manipulate('query display format', query_display_format)

        self.has(properties.time(), equal_to(QTime.fromString(time, query_display_format.result)))


class FileDialogDriver(WidgetDriver):
    DISPLAY_DELAY = 500 if windows else 250
    INITIAL_SETUP_DELAY = 1000 if windows else 0

    def show_hidden_files(self):
        def show_dialog_hidden_files(dialog):
            dialog.setFilter(dialog.filter() | QDir.Hidden)

        self.manipulate('show hidden files', show_dialog_hidden_files)

    def view_as_list(self):
        def set_list_view_mode(dialog):
            dialog.setViewMode(QFileDialog.List)

        self.manipulate('set the view mode to list', set_list_view_mode)

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
        class FindOutCurrentFolder(object):
            def __call__(self, dialog):
                self.name = dialog.directory()

        current_folder = FindOutCurrentFolder()
        self.manipulate('find out current folder', current_folder)
        return current_folder.name

    def into_folder(self, name):
        self.select_file(name)
        self._double_click_on_folder()

    def _double_click_on_folder(self):
        self.perform(gestures.mouse_double_click())

    def filter_files_of_type(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.select_option(matching)

    def select_file(self, name):
        self.select_files(name)

    def select_files(self, *names):
        self.pause(self.DISPLAY_DELAY)
        self._list_view().select_items(*[match.with_list_item_text(name) for name in names])

    def up_one_folder(self):
        self._tool_button_named('toParentButton').click()

    def _tool_button_named(self, name):
        return ButtonDriver.find_single(self, QToolButton, match.named(name))

    def enter_manually(self, filename):
        self._filename_edit().replace_all_text(filename)

    def accept(self):
        self._accept_button().click()

    def accept_button_is(self, criteria):
        return self._accept_button().is_(criteria)

    def accept_button_has_text(self, text):
        return self._accept_button().has_text(text)

    def reject(self):
        return self.reject_button().click()

    def reject_button_is(self, criteria):
        return self.reject_button().is_(criteria)

    def reject_button_has_text(self, text):
        return self.reject_button().has_text(text)

    def _list_view(self):
        return ListViewDriver.find_single(self, QListView, match.named("listView"))

    def _filename_edit(self):
        return LineEditDriver.find_single(self, QLineEdit, match.named("fileNameEdit"))

    def _accept_button(self):
        return self._dialog_button(QFileDialog.Accept)

    def reject_button(self):
        return self._dialog_button(QFileDialog.Reject)

    def _dialog_button(self, label):
        class QueryButtonText(object):
            def __init__(self, label):
                super(QueryButtonText, self).__init__()
                self._label = label

            def __call__(self, dialog):
                self.text = dialog.labelText(self._label)

        button_text = QueryButtonText(label)
        self.manipulate('query button text', button_text)
        return ButtonDriver.find_single(self, QPushButton, match.with_text(button_text.text))

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
        self.perform(gestures.with_modifiers(Qt.ControlModifier, gestures.click_at(self._center_of_item(index))))

    def _select_item(self, index):
        self._scroll_item_to_visible(index)
        self.perform(gestures.click_at(self._center_of_item(index)))

    def _scroll_item_to_visible(self, index):
        self.manipulate('scroll item to visible', lambda listView: listView.scrollTo(index))

    def _center_of_item(self, index):
        class CalculateCenterOfItem(object):
            def __call__(self, list_view):
                item_visible_area = list_view.visualRect(index)
                self.pos = list_view.mapToGlobal(item_visible_area.center())

        center_of_item = CalculateCenterOfItem()
        self.manipulate('calculate center of item', center_of_item)
        return center_of_item.pos

    def _index_of_first_item(self, matching):
        class ContainingItem(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingItem, self).__init__()
                self._item_matcher = matcher
                self.at_index = None

            def _matches(self, list_view):
                model = list_view.model()
                root = list_view.rootIndex()
                item_count = model.rowCount(root)
                for i in range(item_count):
                    index = model.index(i, 0, root)
                    if self._item_matcher.matches(index):
                        self.at_index = index
                        return True

                return False

            def describe_to(self, description):
                description.append_text('containing an item ')
                self._item_matcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text('contained no item ')
                self._item_matcher.describe_to(mismatch_description)

        containing_item = ContainingItem(matching)
        self.is_(containing_item)
        return containing_item.at_index


class QMenuBarDriver(WidgetDriver):
    def menu(self, matching):
        # We have to make sure the menu actually exists on the menu bar
        # Checking that the menu is a child of the menu bar is not sufficient
        self.has_menu(matching)
        return MenuDriver.find_single(self, QMenu, matching)

    def has_menu(self, matching):
        class ContainingMenu(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingMenu, self).__init__()
                self._matcher = matcher

            def _matches(self, menu_bar):
                for menu in [action.menu() for action in menu_bar.actions()]:
                    if self._matcher.matches(menu):
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing a menu ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text('contained no menu ')
                self._matcher.describe_to(mismatch_description)

        self.is_(ContainingMenu(matching))


class MenuDriver(WidgetDriver):
    def open(self):
        # QMenuBar on Mac OS X is a wrapper for using the system-wide menu bar
        # so we cannot just click on it, we have to pop it up manually
        def popup(menu):
            menu_bar = menu.parent()
            menu_title_visible_area = menu_bar.actionGeometry(menu.menuAction())
            # We try to pop up the menu at a position that makes sense on all platforms
            # i.e. just below the menu title
            menu.popup(menu_bar.mapToGlobal(menu_title_visible_area.bottomLeft()))

        self.manipulate('open', popup)

    def menu_item(self, matching):
        # We have to make sure the item menu actually exists in the menu
        # Checking that the item is a child of the menu is not sufficient
        self.has_menu_item(matching)
        return MenuItemDriver.find_single(self, QAction, matching)

    def select_menu_item(self, matching):
        menu_item = self.menu_item(matching)
        menu_item.click()

    def has_menu_item(self, matching):
        class ContainingMenuItem(BaseMatcher):
            def __init__(self, matcher):
                super(ContainingMenuItem, self).__init__()
                self._matcher = matcher
                self.action = None

            def _matches(self, menu):
                for action in menu.actions():
                    if self._matcher.matches(action):
                        self.action = action
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing an item ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text('contained no item ')
                self._matcher.describe_to(mismatch_description)

        containing_menu_item = ContainingMenuItem(matching)
        self.is_(containing_menu_item)
        return containing_menu_item.action


class MenuItemDriver(WidgetDriver):
    def _center_of_item(self):
        class CalculateCenterOfItem(object):
            def __call__(self, item):
                menu = item.parent()
                item_visible_area = menu.actionGeometry(item)
                self.coordinates = menu.mapToGlobal(item_visible_area.center())

        center = CalculateCenterOfItem()
        self.manipulate('calculate center of item', center)
        return center.coordinates

    def click(self):
        self.is_enabled()
        self.perform(gestures.mouse_move(self._center_of_item()), gestures.mouse_click())


class TableViewDriver(WidgetDriver):
    def has_headers(self, matching):
        class WithHeaders(BaseMatcher):
            def __init__(self, matcher):
                super(WithHeaders, self).__init__()
                self._matcher = matcher

            @staticmethod
            def _headers(table):
                return [header_text(table, column) for column in range(column_count(table))]

            def _matches(self, table):
                return self._matcher.matches(self._headers(table))

            def describe_to(self, description):
                description.append_text('with headers ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('headers ')
                self._matcher.describe_mismatch(self._headers(table), mismatch_description)

        self.is_(WithHeaders(matching))

    def has_row(self, matching):
        class RowInTable(BaseMatcher):
            def __init__(self, matcher):
                super(RowInTable, self).__init__()
                self._matcher = matcher

            @staticmethod
            def _cells_of(table, row):
                return [cell_text(table, row, column) for column in range(column_count(table))]

            def _matches(self, table):
                for row in range(row_count(table)):
                    if self._matcher.matches(self._cells_of(table, row)):
                        self.in_row = visual_row(table, row)
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing row ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('contained no row ')
                self._matcher.describe_to(mismatch_description)

        row_in_table = RowInTable(matching)
        self.is_(row_in_table)
        return row_in_table.in_row

    def contains_rows(self, matching):
        class WithRows(BaseMatcher):
            def __init__(self, matcher):
                super(WithRows, self).__init__()
                self._matcher = matcher

            @staticmethod
            def _cells_in(table, row):
                return [cell_text(table, row, column) for column in range(column_count(table))]

            @staticmethod
            def _rows_in(table):
                rows = []
                for row in range(row_count(table)):
                    rows.append(WithRows._cells_in(table, row))
                return rows

            def _matches(self, table):
                return self._matcher.matches(self._rows_in(table))

            def describe_to(self, description):
                description.append_text('with rows ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('rows ')
                self._matcher.describe_mismatch(self._rows_in(table), mismatch_description)

        self.is_(WithRows(matching))

    def scroll_cell_to_visible(self, row, column):
        class ScrollCellToVisible(object):
            def __init__(self, row, column):
                self._row = row
                self._column = column

            def __call__(self, table):
                row, column = cell_location(table, self._row, self._column)
                table.scrollTo(table.indexAt(QPoint(table.columnViewportPosition(column),
                                                    table.rowViewportPosition(row))))

        scroll_cell_to_visible = ScrollCellToVisible(row, column)
        self.manipulate('scroll cell (%s, %s) into view' % (row, column), scroll_cell_to_visible)

    def _click_at_cell_center(self, row, column):
        class CalculateCellPosition(object):
            def __init__(self, row, column):
                self._row = row
                self._column = column

            def center_of_cell(self, table):
                row, column = cell_location(table, self._row, self._column)
                row_offset = table.horizontalHeader().height() + table.rowViewportPosition(row)
                column_offset = table.verticalHeader().width() + table.columnViewportPosition(column)
                return QPoint(column_offset + table.columnWidth(column) / 2,
                              row_offset + table.rowHeight(row) / 2)

            def __call__(self, table):
                self.center = table.mapToGlobal(self.center_of_cell(table))

        cell_position = CalculateCellPosition(row, column)
        self.manipulate('calculate cell (%s, %s) center position' % (row, column), cell_position)
        self.perform(gestures.click_at(cell_position.center))

    def click_on_cell(self, row, column):
        self.scroll_cell_to_visible(row, column)
        self._click_at_cell_center(row, column)

    def widget_in_cell(self, row, column):
        class WidgetAt(WidgetSelector):
            def __init__(self, table_selector, row, column):
                super(WidgetAt, self).__init__()
                self._table_selector = table_selector
                self._row = row
                self._column = column

            def describe_to(self, description):
                description.append_text('in cell (%s, %s) widget' % (self._row, self._column))
                description.append_text('\n    in ')
                description.append_description_of(self._table_selector)

            def describe_failure_to(self, description):
                self._table_selector.describe_failure_to(description)
                if self._table_selector.is_satisfied():
                    if self.is_satisfied():
                        description.append_text('\n    cell (%s, %s)' % (self._row, self._column))
                    else:
                        description.append_text('\n    had no widget in cell (%s, %s)'
                                                % (self._row, self._column))

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
                self._widget_in_cell = widget_at(table, self._row, self._column)

        return WidgetDriver(WidgetAt(self.selector, row, column), self.prober, self.gesture_performer)

    def has_row_count(self, matching):
        class WithRowCount(BaseMatcher):
            def __init__(self, matcher):
                super(WithRowCount, self).__init__()
                self._matcher = matcher

            def _matches(self, table):
                return self._matcher.matches(row_count(table))

            def describe_to(self, description):
                description.append_text('with row count ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('row count ')
                self._matcher.describe_mismatch(row_count(table), mismatch_description)

        self.is_(WithRowCount(matching))

    def move_row(self, old_position, new_position):
        class MoveRow(object):
            def __init__(self, old_position, new_position):
                self._oldPosition = old_position
                self._newPosition = new_position

            def __call__(self, table):
                table.verticalHeader().moveSection(row_location(table, old_position),
                                                   row_location(table, new_position))

        # We'd like to use gestures but drag and drop is not supported by our Robot
        # so we have to use a manipulation
        self.manipulate('move row %s to position %s' % (old_position, new_position),
                        MoveRow(old_position, new_position))


class TableWidgetDriver(TableViewDriver):
    def has_header_items(self, matching):
        class WithHeaders(BaseMatcher):
            def __init__(self, matcher):
                super(WithHeaders, self).__init__()
                self._matcher = matcher

            @staticmethod
            def _header_items(table):
                return [table.horizontalHeaderItem(column_location(table, column))
                        for column in range(table.columnCount())]

            def _matches(self, table):
                return self._matcher.matches(self._header_items(table))

            def describe_to(self, description):
                description.append_text('with header items ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('header items ')
                self._matcher.describe_mismatch(self._header_items(table), mismatch_description)

        self.is_(WithHeaders(matching))

    def hasRowItems(self, matching):
        class RowInTable(BaseMatcher):
            def __init__(self, matcher):
                super(RowInTable, self).__init__()
                self._matcher = matcher

            @staticmethod
            def _cell_items(table, row):
                return [table.item(row, column) for column in range(table.columnCount())]

            def _matches(self, table):
                for row in range(table.rowCount()):
                    if self._matcher.matches(self._cell_items(table, row)):
                        self.in_row = table.visualRow(row)
                        return True
                return False

            def describe_to(self, description):
                description.append_text('containing row items ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('contained no items ')
                self._matcher.describe_to(mismatch_description)

        row_in_table = RowInTable(matching)
        self.is_(row_in_table)
        return row_in_table.in_row

    def contains_row_items(self, matching):
        class WithRows(BaseMatcher):
            def __init__(self, matcher):
                super(WithRows, self).__init__()
                self._matcher = matcher

            @staticmethod
            def _cellItems(table, row):
                return [table.item(row, column) for column in range(table.columnCount())]

            @staticmethod
            def _rowsItems(table):
                rows = []
                for row in range(table.rowCount()):
                    rows.append(WithRows._cellItems(table, row))
                return rows

            def _matches(self, table):
                return self._matcher.matches(self._rowsItems(table))

            def describe_to(self, description):
                description.append_text('with row items ')
                self._matcher.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('row items ')
                self._matcher.describe_mismatch(self._rowsItems(table), mismatch_description)

        self.is_(WithRows(matching))


def column_location(table, column):
    return table.horizontalHeader().logicalIndex(column)


def row_location(table, row):
    return table.verticalHeader().logicalIndex(row)


def cell_location(table, row, column):
    return row_location(table, row), column_location(table, column)


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


def visual_row(table, row):
    return table.verticalHeader().visualIndex(row)

# -*- coding: utf-8 -*-
from PyQt5.QtCore import QDir, QPoint, QTime, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QListView, QToolButton, QFileDialog, \
    QMenu, QComboBox, QTextEdit, QLabel, QAbstractButton, QSpinBox, QTableView, QDialogButtonBox
from hamcrest import all_of, anything
from hamcrest.core.base_matcher import BaseMatcher

from cute import event_loop
from . import gestures, properties, matchers as match, rect
from .finders import SingleWidgetFinder, TopLevelWidgetsFinder, RecursiveWidgetFinder, NthWidgetFinder, \
    WidgetSelector, WidgetIdentity, MissingWidgetFinder
from .probes import WidgetManipulatorProbe, WidgetAssertionProbe, WidgetPropertyAssertionProbe, WidgetScreenBoundsProbe
from .table import TableMatcher, TableManipulation, Table


def all_top_level_widgets():
    # noinspection PyArgumentList
    return TopLevelWidgetsFinder(QApplication.instance())


def all_widgets(of_type, matching=anything()):
    return RecursiveWidgetFinder(of_type, matching, all_top_level_widgets())


def only_widget(of_type, matching=anything()):
    return SingleWidgetFinder(all_widgets(of_type, matching))


def no_widget(of_type, matching=anything()):
    return MissingWidgetFinder(all_widgets(of_type, matching))


def window(of_type, *matchers):
    return only_widget(of_type, all_of(*matchers))


def main_application_window(*matchers):
    return only_widget(QMainWindow, all_of(*matchers))


class QueryManipulation:
    def __init__(self, query):
        self._query = query
        self._values = []

    def __call__(self, widget):
        self._values.append(self._query(widget))

    @property
    def value(self):
        return self.values[0] if self.values else None

    @property
    def values(self):
        return self._values


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
    def find_none(cls, parent, widget_type, *matchers):
        return cls(MissingWidgetFinder(
            RecursiveWidgetFinder(widget_type, all_of(*matchers), parent.selector)), parent.prober,
            parent.gesture_performer)

    @classmethod
    def find_nth(cls, parent, widget_type, index, *matchers):
        return cls(NthWidgetFinder(
            RecursiveWidgetFinder(widget_type, all_of(*matchers), parent.selector), index),
            parent.prober, parent.gesture_performer)

    def exists(self):
        self.check(self.selector)

    def is_showing_on_screen(self):
        self.is_(match.showing_on_screen())

    def is_hidden(self):
        self.is_(match.hidden())

    def is_enabled(self, enabled=True):
        self.is_(match.enabled() if enabled else match.disabled())

    def is_disabled(self, disabled=True):
        self.is_enabled(not disabled)

    def is_(self, criteria):
        self.check(WidgetAssertionProbe(self.selector, criteria))

    def has(self, query, criteria):
        self.check(WidgetPropertyAssertionProbe(self.selector, query, criteria))

    def has_tooltip(self, text):
        self.has(properties.tooltip(), text)

    def has_cursor_shape(self, shape):
        self.has(properties.cursor_shape(), shape)

    def has_window_title(self, title):
        self.has(properties.window_title(), title)

    def manipulate(self, description, manipulation):
        self.check(WidgetManipulatorProbe(self.selector, manipulation, description))
        self.refresh()

    def refresh(self):
        event_loop.process_pending_events()

    def query(self, description, widget_query):
        manipulation = QueryManipulation(widget_query)
        self.manipulate("query {0}".format(description), manipulation)
        return manipulation.value

    def widget(self):
        return self.query("widget", lambda widget: widget)

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

    def perform(self, *gestures_to_perform):
        self.gesture_performer.perform(*gestures_to_perform)

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
        self.has(properties.text(), matcher)

    def is_unchecked(self, unchecked=True):
        self.is_checked(not unchecked)

    def is_checked(self, checked=True):
        self.is_(match.checked() if checked else match.unchecked())

    def has_icon_size(self, matcher):
        self.has(properties.icon_size(), matcher)


class QToolButtonDriver(ButtonDriver):
    def open_menu(self):
        bottom_left = self.widget_bounds().bottomLeft()
        menu = self.query("selector menu", lambda button: button.menu())
        driver = MenuDriver(WidgetIdentity(menu), self.prober, self.gesture_performer)
        driver.popup_manually_at(bottom_left.x(), bottom_left.y())
        return driver


class LabelDriver(WidgetDriver):
    def has_text(self, matcher):
        self.has(properties.text(), matcher)

    def has_pixmap(self, matcher):
        self.has(properties.label_pixmap(), matcher)


class AbstractEditDriver(WidgetDriver):
    def change_text(self, text):
        self.replace_all_text(text)
        self.enter()

    def replace_all_text(self, text):
        self.is_enabled()
        self.focus_with_mouse()
        self.clear_all_text()
        self.type(text)

    def focus_with_mouse(self):
        self.left_click_on_widget()

    def clear_all_text(self):
        self.select_all_text()
        self.delete_selected_text()

    def select_all_text(self):
        self.perform(gestures.select_all())

    def delete_selected_text(self):
        self.perform(gestures.delete_previous())

    def type(self, text):
        self.perform(gestures.type_text(text))


class LineEditDriver(AbstractEditDriver):
    def has_text(self, text):
        self.has(properties.input_text(), text)


class TextEditDriver(AbstractEditDriver):
    def has_plain_text(self, text):
        self.has(properties.plain_text(), text)

    def add_line(self, text):
        self.focus_with_mouse()
        self.type(text)
        self.perform(gestures.enter())


class QAbstractSpinBoxDriver(AbstractEditDriver):
    pass


class ComboBoxDriver(AbstractEditDriver):
    def select_option(self, matching):
        options_list = self._open_options_list()
        options_list.select_item(match.with_list_item_text(matching))

    def has_options(self, *matching):
        options_list = self._open_options_list()
        for matcher in matching:
            options_list.has_item(match.with_list_item_text(matcher))

    def has_no_option(self, matching):
        options_list = self._open_options_list()
        options_list.has_no_item(match.with_list_item_text(matching))

    def _open_options_list(self):
        self.perform(gestures.mouse_click_at(rect.center_right(rect.inside_bounds(self.widget_bounds(), right=5))))
        return QListViewDriver.find_single(self, QListView)

    def has_current_text(self, matching):
        self.has(properties.current_text(), matching)


class QDateTimeEditDriver(WidgetDriver):
    def display_format(self):
        return self.query("display format", lambda date_time: date_time.displayFormat())

    def has_date(self, date):
        self.has(properties.date(), QDate.fromString(date, self.display_format()))

    def has_time(self, time):
        self.has(properties.time(), QTime.fromString(time, self.display_format()))

    def enter_date(self, year, month, day):
        self.perform(gestures.mouse_double_click_at(rect.center_left(rect.inside_bounds(self.widget_bounds(), left=5))))
        self.perform(gestures.type_text(str(year) + "{0:02d}".format(month) + "{0:02d}".format(day)))
        self.perform(gestures.enter())

    def select_date(self, year, month, day):
        self._popup_calendar()
        self.refresh()
        self._calendar().select_date(year, month, day)

    def _popup_calendar(self):
        self.perform(gestures.mouse_click_at(rect.center_right(self.widget_bounds())))

    def _calendar(self):
        calendar = self.query("calendar widget", lambda date_edit: date_edit.calendarWidget())
        return QCalendarDriver(WidgetIdentity(calendar), self.prober, self.gesture_performer)


class QCalendarDriver(WidgetDriver):
    def select_date(self, year, month, day):
        self.enter_year(year)
        self.select_month(month)
        self.select_day(day)

    def enter_year(self, year):
        self._year_button().click()
        self._year_spinner().type(str(year))
        self.perform(gestures.enter())
        self.refresh()

    def select_month(self, month):
        # Clicking the toolbutton blocks the execution, so pop up menu manually
        bottom_left = self._month_button().widget_bounds().bottomLeft()
        self._month_menu().popup_manually_at(bottom_left.x(), bottom_left.y())
        self._month_menu().select_menu_item(match.with_data(month))
        self.refresh()

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
        month_menu = self.query("month selector menu",
                                lambda calendar: calendar.findChild(QToolButton, "qt_calendar_monthbutton").menu())
        return MenuDriver(WidgetIdentity(month_menu), self.prober, self.gesture_performer)

    def _table(self):
        table = self.query("calendar table",
                           lambda calendar: calendar.findChild(QTableView, "qt_calendar_calendarview"))
        return TableViewDriver(WidgetIdentity(table), self.prober, self.gesture_performer)

    def _find_day(self, day):
        class FindDayInCalendar:
            def __call__(self, table):
                def find_position_of_day_in_calendar(which_day, from_row=0, from_col=0):
                    row = from_row
                    col = from_col

                    while row < 7:
                        while col < 7:
                            if str(which_day) == str(table.cell_text(row, col)):
                                return row, col
                            col += 1
                        row, col = row + 1, 0

                    return -1, -1

                self.row, self.col = find_position_of_day_in_calendar(day, *find_position_of_day_in_calendar(1))

        find_position = FindDayInCalendar()
        self._table().manipulate_table("find position of day '{0}' in calendar".format(day), find_position)
        return find_position.row, find_position.col


class QDialogButtonBoxDriver(WidgetDriver):
    def click_ok(self):
        self.ok_button().click()

    def click_yes(self):
        self.button(QDialogButtonBox.Yes).click()

    def click_no(self):
        self.button(QDialogButtonBox.No).click()

    def click_cancel(self):
        self.button(QDialogButtonBox.Cancel).click()

    def ok_button(self):
        return self.button(QDialogButtonBox.Ok)

    def button(self, role):
        self.is_showing_on_screen()
        button = self.query("button with role {0}".format(role), lambda button_box: button_box.button(role))
        # todo find a way to fail with a descriptive message if button is None
        return ButtonDriver(WidgetIdentity(button), self.prober, self.gesture_performer)


class QDialogDriver(WidgetDriver):
    def is_active(self):
        self.is_showing_on_screen()
        self.is_(match.active_window())

    def ok_button(self):
        return self.button_box().ok_button()

    def click_ok(self):
        self.button_box().click_ok()

    def click_cancel(self):
        self.button_box().click_cancel()

    def click_yes(self):
        self.button_box().click_yes()

    def click_no(self):
        self.button_box().click_no()

    def button_box(self):
        self.is_showing_on_screen()
        return QDialogButtonBoxDriver.find_single(self, QDialogButtonBox)


class QFileDialogDriver(QDialogDriver):
    def show_hidden_files(self):
        def show_dialog_hidden_files(dialog):
            dialog.setFilter(dialog.filter() | QDir.Hidden)

        self.manipulate("show hidden files", show_dialog_hidden_files)

    def view_as_list(self):
        def set_list_view_mode(dialog):
            dialog.setViewMode(QFileDialog.List)

        self.manipulate("set the view mode to list", set_list_view_mode)

    @property
    def current_dir(self):
        class FindOutCurrentFolder:
            def __call__(self, dialog):
                self.name = dialog.directory()

        find_folder = FindOutCurrentFolder()
        self.manipulate("find out current folder", find_folder)
        return find_folder.name

    def has_current_directory(self, matching):
        self.has(properties.current_directory(), matching)

    def into_folder(self, name):
        self.files_list.open_item(match.with_list_item_text(name))

    def filter_files_of_type(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.select_option(matching)

    def select_file(self, name):
        self.select_files(name)

    def select_files(self, *names):
        self.files_list.select_items(*[match.with_list_item_text(name) for name in names])

    def up_one_folder(self):
        up_button = ButtonDriver.find_single(self, QToolButton, match.named("toParentButton"))
        up_button.click()

    def enter_manually(self, filename):
        self._filename_edit().replace_all_text(filename)

    def has_filename(self, filename):
        self._filename_edit().has_text(filename)

    def accept(self):
        self._accept_button().click()

    def has_accept_button(self, criteria):
        return self._accept_button().is_(criteria)

    def has_accept_button_text(self, text):
        return self._accept_button().has_text(text)

    def reject(self):
        self._reject_button().click()

    def has_reject_button(self, criteria):
        self._reject_button().is_(criteria)

    def has_reject_button_text(self, text):
        self._reject_button().has_text(text)

    @property
    def files_list(self):
        return QListViewDriver.find_single(self, QListView, match.named("listView"))

    def _filename_edit(self):
        return LineEditDriver.find_single(self, QLineEdit, match.named("fileNameEdit"))

    def _accept_button(self):
        return self._dialog_button(QFileDialog.Accept)

    def _reject_button(self):
        return self._dialog_button(QFileDialog.Reject)

    def _dialog_button(self, label):
        button_text = self.query("button text", lambda dialog: dialog.labelText(label))
        return ButtonDriver.find_single(self, QPushButton, match.with_text(button_text))

    def has_selected_file_type(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.has_current_text(matching)

    def _has_file_type_options_count(self, matching):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.has(properties.count(), matching)

    def has_file_type_options(self, *options):
        for index, option in enumerate(options):
            self._has_file_type_option(option, index=index)
        self._has_file_type_options_count(len(options))

    def _has_file_type_option(self, option, *, index):
        driver = ComboBoxDriver.find_single(self, QComboBox, match.named("fileTypeCombo"))
        driver.has(properties.has_option_text(index), option)


class QListViewDriver(WidgetDriver):
    def select_item(self, matching):
        self.select_items(matching)

    def select_items(self, *matchers):
        self._select_items_at([self._index_of_first_item(matching) for matching in matchers])

    def open_item(self, matching):
        self._open_item_at(self._index_of_first_item(matching))

    def has_item(self, matching):
        self._index_of_first_item(matching)

    def has_no_item(self, matching):
        self._is_not_containing(matching)

    def _select_item_at(self, index):
        self._scroll_item_to_visible(index)
        self.perform(gestures.mouse_click_at(self._center_of_item(index)))

    def _open_item_at(self, index):
        self._scroll_item_to_visible(index)
        self.perform(gestures.mouse_double_click_at(self._center_of_item(index)))

    def _select_items_at(self, indexes):
        self._select_item_at(indexes.pop(0))
        for index in indexes:
            self._multi_select_item_at(index)

    def _multi_select_item_at(self, index):
        self._scroll_item_to_visible(index)
        self.perform(gestures.mouse_multi_click_at(self._center_of_item(index)))

    def _scroll_item_to_visible(self, index):
        self.manipulate("scroll item to visible", lambda list_view: list_view.scrollTo(index))

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

    def _is_not_containing(self, matching):
        class NotContainingMatchingItem(BaseMatcher):
            def _matches(self, list_view):
                model = list_view.model()
                root = list_view.rootIndex()
                item_count = model.rowCount(root)
                for i in range(item_count):
                    index = model.index(i, 0, root)
                    if matching.matches(index):
                        return False

                return True

            def describe_to(self, description):
                description.append_text("containing no item ")
                matching.describe_to(description)

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("contained an item ")
                matching.describe_to(mismatch_description)

        containing_item = NotContainingMatchingItem()
        self.is_(containing_item)


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
    def popup_manually_at(self, x, y):
        # For some reason, we can't open the menu by just right clicking, so open it manually
        self.manipulate("open at ({0}, {1})".format(x, y), lambda menu: menu.popup(QPoint(x, y)))

    def menu_item(self, matching):
        # We have to make sure the item menu actually exists in the menu
        # Checking that the item is a child of the menu is not sufficient
        action = self.has_menu_item(matching)
        return MenuItemDriver(WidgetIdentity(action), self.prober, self.gesture_performer)

    def select_menu_item(self, matching):
        self.is_showing_on_screen()
        menu_item = self.menu_item(matching)
        menu_item.click()

    def has_menu_item(self, matching, track_index=None):
        class ContainingMatchingMenuItem(BaseMatcher):
            def _matches(self, menu):
                for index, action in enumerate(menu.actions()):
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

        class MenuItemPositionedAt(BaseMatcher):
            _index = None

            def _matches(self, menu):
                for index, action in enumerate(menu.actions()):
                    if matching.matches(action):
                        self._index = index
                        if index == track_index:
                            return True
                return False

            def describe_to(self, description):
                description.append_text("positioned at index " + str(track_index))

            def describe_mismatch(self, item, mismatch_description):
                mismatch_description.append_text("positioned at index " + str(self._index))

        containing_menu_item = ContainingMatchingMenuItem()
        self.is_(containing_menu_item)
        if track_index is not None:
            self.is_(MenuItemPositionedAt())
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
        self.popup_manually_at(find_position.coordinates.x(), find_position.coordinates.y())


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
        self.is_showing_on_screen()
        self.perform(gestures.mouse_click_at(self._center_of_item()))


class QMessageBoxDriver(QDialogDriver):
    def shows_message(self, message):
        LabelDriver.find_single(self, QLabel, match.named("qt_msgbox_label")).has_text(message)

    def shows_details(self, details):
        TextEditDriver.find_single(self, QTextEdit).has_plain_text(details)


class TableViewDriver(WidgetDriver):
    def manipulate_table(self, description, manipulation):
        self.manipulate(description, TableManipulation(manipulation))

    def is_table(self, criteria):
        self.is_(TableMatcher(criteria))

    def has_headers(self, matching):
        class WithMatchingHeaders(BaseMatcher):
            def _matches(self, table):
                return matching.matches(table.headers())

            def describe_to(self, description):
                description.append_text("with headers ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("headers ")
                matching.describe_mismatch(table.headers(), mismatch_description)

        self.is_table(WithMatchingHeaders())

    def has_row(self, matching):
        class WithMatchingRow(BaseMatcher):
            def _matches(self, table):
                for row in range(table.row_count()):
                    if matching.matches(table.cells(row)):
                        self.index = row
                        return True
                return False

            def describe_to(self, description):
                description.append_text("containing row ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("contained no row ")
                matching.describe_to(mismatch_description)

        with_matching_row = WithMatchingRow()
        self.is_table(with_matching_row)
        return with_matching_row.index

    def contains_rows(self, matching):
        class WithMatchingRows(BaseMatcher):
            def _matches(self, table):
                return matching.matches(table.all_cells())

            def describe_to(self, description):
                description.append_text("with rows ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("rows ")
                matching.describe_mismatch(table.all_cells(), mismatch_description)

        self.is_table(WithMatchingRows())

    def scroll_cell_to_visible(self, row, column):
        def scroll_cell_to_visible(table):
            table.scroll_to(row, column)

        self.manipulate_table("scroll cell ({0}, {1}) into view".format(row, column), scroll_cell_to_visible)

    def _click_at_cell_center(self, row, column):
        class CalculateCellPosition:
            def __call__(self, table):
                self.center = table.cell_center(row, column)

        calculate_position = CalculateCellPosition()
        self.manipulate_table("calculate cell ({0}, {1}) center position".format(row, column), calculate_position)
        self.perform(gestures.mouse_click_at(calculate_position.center))

    def click_on_cell(self, row, column):
        self.scroll_cell_to_visible(row, column)
        self._click_at_cell_center(row, column)

    def widget_in_cell(self, row, column):
        class WidgetInCell(WidgetSelector):
            _widget_in_cell = None

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

                widget = self._table_selector.widget()
                self._widget_in_cell = Table(widget).widget_at(row, column)

        return WidgetDriver(WidgetInCell(self.selector), self.prober, self.gesture_performer)

    def has_row_count(self, matching):
        class WithMatchingRowCount(BaseMatcher):
            def _matches(self, table):
                return matching.matches(table.row_count())

            def describe_to(self, description):
                description.append_text("with row count ")
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text("row count ")
                matching.describe_mismatch(table.row_count(), mismatch_description)

        self.is_table(WithMatchingRowCount())

    def has_selected_row(self, matching):
        class WithMatchingSelectedRow(BaseMatcher):
            @staticmethod
            def _selected_row(table):
                return table.cells(table.selected_row())

            def _matches(self, table):
                return matching.matches(self._selected_row(table))

            def describe_to(self, description):
                description.append_text('with selected row ')
                matching.describe_to(description)

            def describe_mismatch(self, table, mismatch_description):
                mismatch_description.append_text('selected row was ')
                mismatch_description.append_description_of(self._selected_row(table))

        self.is_table(WithMatchingSelectedRow())

    def move_row(self, from_position, to_position):
        class CalculateHeaderBounds:
            def __init__(self, row):
                self.row = row

            def __call__(self, table):
                self.bounds = table.vertical_header_bounds(self.row)

        from_header = CalculateHeaderBounds(from_position)
        self.manipulate_table("calculate bounds of header row {0}".format(from_position), from_header)
        to_header = CalculateHeaderBounds(to_position)
        self.manipulate_table("calculate bounds of header row {0}".format(to_position), to_header)

        drop_target = rect.bottom_center(rect.inside_bounds(to_header.bounds, bottom=1)) if (
            from_position < to_position) \
            else rect.top_center(rect.inside_bounds(to_header.bounds, top=1))
        self.perform(gestures.mouse_drag(from_header.bounds.center(), drop_target))


class QTabWidgetDriver(WidgetDriver):
    def select(self, text):
        tab_bar = self.query("tab bar", lambda t: t.tabBar())
        QTabBarDriver(WidgetIdentity(tab_bar), self.prober, self.gesture_performer).select(text)


class QTabBarDriver(WidgetDriver):
    def select(self, text):
        class CalculateCenterOfItem:
            center = None

            def __call__(self, item):
                for i in range(0, item.count()):
                    if item.tabText(i) == text:
                        self.center = item.mapToGlobal(item.tabRect(i).center())
                        break

        calculate_center = CalculateCenterOfItem()
        self.manipulate("calculate center of item", calculate_center)
        self.perform(gestures.mouse_click_at(calculate_center.center))

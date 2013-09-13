# -*- coding: utf-8 -*-

from PyQt4.Qt import (Qt, QApplication, QMainWindow, QLineEdit, QPushButton, QListView,
                      QToolButton, QDir)
from hamcrest.core import all_of, equal_to

from .probes import (WidgetManipulatorProbe, WidgetAssertionProbe, WidgetPropertyAssertionProbe,
                    WidgetScreenBoundsProbe)
from .finders import SingleWidgetFinder, TopLevelFrameFinder, RecursiveWidgetFinder
from . import properties, gestures
from . import matchers as match


def main_window(*matchers):
    return SingleWidgetFinder(RecursiveWidgetFinder(QMainWindow, all_of(*matchers),
                                                    TopLevelFrameFinder(QApplication.instance())))


class WidgetDriver(object):
    def __init__(self, selector, prober):
        self._selector = selector
        self._prober = prober

    @property
    def selector(self):
        return self._selector

    @property
    def prober(self):
        return self._prober

    @classmethod
    def find(cls, parent, widget_type, *matchers):
        return cls(SingleWidgetFinder(
            RecursiveWidgetFinder(widget_type, all_of(*matchers), parent.selector)), parent.prober)

    def is_showing_on_screen(self):
        self.verify(match.showing_on_screen())

    def verify(self, criteria):
        self._check(WidgetAssertionProbe(self.selector, criteria))

    def has(self, query, criteria):
        self._check(WidgetPropertyAssertionProbe(self.selector, query, criteria))

    def manipulate(self, description, manipulation):
        self._check(WidgetManipulatorProbe(self.selector, manipulation, description))

    def widget_center(self):
        probe = WidgetScreenBoundsProbe(self.selector)
        self._check(probe)
        return probe.bounds.center()

    def left_click_on_widget(self):
        self.is_showing_on_screen()
        return gestures.click_on(self.widget_center())

    def _check(self, probe):
        self.prober.check(probe)


class MainWindowDriver(WidgetDriver):
    def close(self):
        self.manipulate("close", lambda window: window.close())


class AbstractButtonDriver(WidgetDriver):
    def click(self):
        return self.left_click_on_widget()


class LabelDriver(WidgetDriver):
    def has_text(self, text):
        self.has(properties.label_text(), equal_to(text))


# Caution: text edition works unreliably within file dialogs
class LineEditDriver(WidgetDriver):
    def has_text(self, text):
        self.has(properties.input_text(), equal_to(text))

    def replace_all_text(self, text):
        return gestures.sequence(self.focus_with_mouse(), self.clear_all_text(), self.type(text))

    def focus_with_mouse(self):
        return self.left_click_on_widget()

    def clear_all_text(self):
        return gestures.sequence(self.select_all_text(),
                                 gestures.pause(50), self.delete_selected_text())

    def select_all_text(self):
        # todo probably better to try key sequence Select-All (CTRL+A for Qt)
        return gestures.mouse_double_click()

    def delete_selected_text(self):
        return gestures.type_key(Qt.Key_Backspace)

    def type(self, text):
        return gestures.type_text(text)


class FileDialogDriver(WidgetDriver):
    NAVIGATION_DELAY = 100

    def show_hidden_files(self):
        # todo use a manipulation
        self.selector.test()
        dialog = self.selector.widget()
        dialog.setFilter(dialog.filter() | QDir.Hidden)

    def navigate_to_dir(self, path):
        def change_to(name):
            if name == '..':
                return lambda robot: self.up_one_folder()(robot)
            else:
                return lambda robot: self.into_folder(name)(robot)

        return gestures.sequence(*[change_to(d) for d in self._navigation_path_to(path)])

    def _navigation_path_to(self, path):
        return self._current_dir().relativeFilePath(path).split("/")

    def _current_dir(self):
        class ReadCurrentDirectory(object):
            def __call__(self, dialog):
                self.name = dialog.directory()

        current_dir = ReadCurrentDirectory()
        self.manipulate("read current directory", current_dir)
        return current_dir.name

    def into_folder(self, name):
        return gestures.sequence(self.select_file(name),
                                 gestures.pause(self.NAVIGATION_DELAY),
                                 gestures.mouse_double_click(),
                                 gestures.pause(self.NAVIGATION_DELAY))

    def select_file(self, name):
        return self._list_view().select_item(match.with_list_item_text(name))

    def up_one_folder(self):
        return self._tool_button_named('toParentButton').click()

    def _tool_button_named(self, name):
        return AbstractButtonDriver.find(self, QToolButton, match.named(name))

    def enter_manually(self, filename):
        return self._filename_edit().replace_all_text(filename)

    def accept(self):
        return self._accept_button().click()

    def _list_view(self):
        return ListViewDriver.find(self, QListView, match.named('listView'))

    def _filename_edit(self):
        return LineEditDriver.find(self, QLineEdit, match.named("fileNameEdit"))

    def _accept_button(self):
        # todo Query the file dialog accept button label (see QFileDialog.labelText(QFileDialog
        # .Accept)) using a widget manipulation
        return AbstractButtonDriver.find(self, QPushButton, match.with_button_text("&Open"))


class ListViewDriver(WidgetDriver):
    def select_item(self, matcher):
        return self._select_item(self._index_of_first_item_matching(matcher))

    def _select_item(self, index):
        self._scroll_item_to_visible(index)
        return gestures.click_on(self._center_of_item(index))

    def _scroll_item_to_visible(self, index):
        self.manipulate("scroll item to visible", lambda list_view: list_view.scrollTo(index))

    def _center_of_item(self, index):
        class CalculateCenterOfItem(object):
            def __call__(self, list_view):
                item_visible_area = list_view.visualRect(index)
                self.pos = list_view.mapToGlobal(item_visible_area.center())

        center_of_item = CalculateCenterOfItem()
        self.manipulate("calculate center of item", center_of_item)
        return center_of_item.pos

    def _index_of_first_item_matching(self, matcher):
        from hamcrest.core.base_matcher import BaseMatcher

        class ItemMatcher(BaseMatcher):
            def __init__(self, matcher):
                super(ItemMatcher, self).__init__()
                self._item_matcher = matcher

            def _matches(self, list_view):
                model = list_view.model()
                root = list_view.rootIndex()
                item_count = model.rowCount(root)
                for i in range(item_count):
                    index = model.index(i, 0, root)
                    if self._item_matcher.matches(index):
                        self.index = index
                        return True

                return False

            def describe_to(self, description):
                description.append_text("containing an item ")
                self._item_matcher.describe_to(description)

        item_found = ItemMatcher(matcher)
        self.verify(item_found)
        return item_found.index




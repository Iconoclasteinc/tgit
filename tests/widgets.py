# -*- coding: utf-8 -*-

from PyQt4.Qt import QApplication, QMainWindow, QLineEdit, QPushButton, QListView
from hamcrest.core import all_of, equal_to

from probes import (WidgetManipulatorProbe, WidgetAssertionProbe, WidgetPropertyAssertionProbe,
                    WidgetScreenBoundsProbe, FileDialogCurrentDirectoryProbe)
from finders import SingleWidgetFinder, TopLevelWindowFinder, RecursiveWidgetFinder
import matchers as match
import properties
import gestures


def main_window(*matchers):
    return SingleWidgetFinder(RecursiveWidgetFinder(QMainWindow, all_of(*matchers),
                                                    TopLevelWindowFinder(QApplication.instance())))


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
        return gestures.click_on(self.widget_center())

    def _check(self, probe):
        self.prober.check(probe)


class MainWindowDriver(WidgetDriver):
    def close(self):
        self.manipulate("close", lambda widget: widget.close())


class PushButtonDriver(WidgetDriver):
    def click(self):
        return self.left_click_on_widget()


class LabelDriver(WidgetDriver):
    def has_text(self, text):
        self.has(properties.label_text(), equal_to(text))


class LineEditDriver(WidgetDriver):
    def has_text(self, text):
        self.has(properties.input_text(), equal_to(text))

    def replace_text(self, text):
        # Finish the sequence by a left click to make autocomplete go away
        return gestures.sequence(self.left_click_on_widget(), self.clear_text(),
                                 self.type(text), self.left_click_on_widget())

    def clear_text(self):
        # todo
        return lambda robot: robot

    def type(self, text):
        return gestures.type_text(text)


class FileDialogDriver(WidgetDriver):
    NAVIGATION_DELAY = 100

    def navigate_to_dir(self, path):
        current_dir = self._current_dir()
        navigation_path = current_dir.relativeFilePath(path).split("/")

        def change_to(name):
            # we don't support going up the directory tree just yet
            # if name == '..' up_one_dir()
            return lambda robot: self.into_dir(name)(robot)

        return gestures.sequence(*[change_to(d) for d in navigation_path])

    def _current_dir(self):
        probe = FileDialogCurrentDirectoryProbe(self.selector)
        self._check(probe)
        return probe.current_dir

    def into_dir(self, name):
        return gestures.sequence(self.select_file(name),
                                 gestures.pause(self.NAVIGATION_DELAY),
                                 gestures.mouse_double_click(),
                                 gestures.pause(self.NAVIGATION_DELAY))

    def select_file(self, name):
        # todo now that it works, let's make it clean
        # Introduce a probe, a ListViewDriver and a matcher to select child(ren) from the list
        # Maybe something like: find item based on criteria (i.e. name of file),
        # scroll item into view, then click on center of item
        current_dir = self._current_dir()
        dialog = self._selector.widget()
        file_list = dialog.findChild(QListView, 'listView')
        model = file_list.model()
        parent = model.index(current_dir.absolutePath())
        child_count = model.rowCount(parent)
        for i in range(child_count):
            child = model.index(i, 0, parent)
            if model.fileName(child) == name:
                file_list.scrollTo(child)
                item_visible_area = file_list.visualRect(child)
                return gestures.click_on(file_list.mapToGlobal(item_visible_area.center()))

    def enter_manually(self, filename):
        return self._filename_edit().replace_text(filename)

    def accept(self):
        return self._accept_button().click()

    def _filename_edit(self):
        return LineEditDriver.find(self, QLineEdit, match.named("fileNameEdit"))

    def _accept_button(self):
        return PushButtonDriver.find(self, QPushButton, match.with_text("&Open"))

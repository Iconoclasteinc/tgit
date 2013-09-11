# -*- coding: utf-8 -*-

from PyQt4.Qt import QApplication, QMainWindow
from hamcrest.core import all_of, equal_to

from probes import (WidgetManipulatorProbe, WidgetAssertionProbe, WidgetPropertyAssertionProbe,
                    WidgetScreenBoundsProbe)
from finders import SingleWidgetFinder, TopLevelWindowFinder, RecursiveWidgetFinder
from matchers import showing_on_screen
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
        self.is_(showing_on_screen())

    def is_(self, criteria):
        self._check(WidgetAssertionProbe(self.selector, criteria))

    def has(self, query, criteria):
        self._check(WidgetPropertyAssertionProbe(self.selector, query, criteria))

    def manipulate(self, description, manipulation):
        self._check(WidgetManipulatorProbe(self.selector, manipulation, description))

    def widget_center(self):
        probe = WidgetScreenBoundsProbe(self.selector)
        self._check(probe)
        return probe.bounds().center()

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
        self.has(properties.label_text(), equal_to(unicode(text, "UTF-8")))


class LineEditDriver(WidgetDriver):
    def replace_text(self, text):
        return gestures.sequence(self.left_click_on_widget(), self.clear_text(),
                                 self.type(text))

    def clear_text(self):
        return lambda robot: robot

    def type(self, text):
        return gestures.type_text(text)
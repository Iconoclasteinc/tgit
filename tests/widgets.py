# -*- coding: utf-8 -*-

from PyQt4.Qt import QApplication, QMainWindow
from hamcrest.core import all_of

from probing import in_context
from probes import WidgetManipulationProbe, WidgetAssertionProbe, WidgetScreenBoundsProbe
from finders import SingleWidgetFinder, TopLevelWindowFinder, RecursiveWidgetFinder
from matchers import showing_on_screen
from gestures import click_on


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
        self._find(WidgetAssertionProbe(self.selector, criteria))

    def manipulate(self, description, manipulation):
        self._check(in_context(description, WidgetManipulationProbe(self.selector, manipulation)))

    def widget_center(self):
        probe = WidgetScreenBoundsProbe(self._selector)
        self._find(probe)
        return probe.bounds().center()

    def _find(self, probe):
        self._check(in_context("find", probe))

    def _check(self, probe):
        self.prober.check(probe)


class MainWindowDriver(WidgetDriver):
    def __init__(self, selector, prober):
        super(MainWindowDriver, self).__init__(selector, prober)

    def close(self):
        self.manipulate("close", lambda widget: widget.close())


class PushButtonDriver(WidgetDriver):
    def __init__(self, selector, prober):
        super(PushButtonDriver, self).__init__(selector, prober)

    def press(self):
        return click_on(self.widget_center())
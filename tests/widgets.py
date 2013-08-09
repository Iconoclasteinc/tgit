# -*- coding: utf-8 -*-

from PyQt4.Qt import QApplication, QMainWindow
from hamcrest.core import all_of

from probing import Probe, in_context
from finders import SingleWidgetFinder, TopLevelWindowFinder, RecursiveWidgetFinder
from matchers import showing_on_screen


def main_window(*matchers):
    return SingleWidgetFinder(RecursiveWidgetFinder(QMainWindow, all_of(*matchers),
                                                    TopLevelWindowFinder(QApplication.instance())))


class WidgetAssertionProbe(Probe):
    def __init__(self, selector, assertion):
        self._selector = selector
        self._assertion = assertion
        self._assertion_met = False

    def test(self):
        self._selector.test()
        self._assertion_met = \
            self._selector.is_satisfied() \
                and self._assertion.matches(self._selector.widget())

    def is_satisfied(self):
        return self._assertion_met

    def describe_to(self, description):
        description.append_description_of(self._selector). \
            append_text(" and check that it is "). \
            append_description_of(self._assertion)

    def describe_failure_to(self, description):
        self._selector.describe_failure_to(description)
        if self._selector.is_satisfied():
            description.append_text(" it ")
            if self._assertion_met:
                description.append_text("is ")
            else:
                description.append_text("is not ")
            description.append_description_of(self._assertion)


class WidgetManipulationProbe(Probe):
    def __init__(self, finder, manipulation):
        self._finder = finder
        self._manipulation = manipulation

    def describe_to(self, description):
        self._finder.describe_to(description)

    def describe_failure_to(self, description):
        self._finder.describe_failure_to(description)

    def is_satisfied(self):
        return self._finder.is_satisfied()

    def test(self):
        self._finder.test()
        if self._finder.is_satisfied():
            for widget in self._finder.widgets():
                self._manipulation(widget)


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

    def widget(self):
        self._find(self._selector)
        return self._selector.widget()

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
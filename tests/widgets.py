# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QMainWindow

from hamcrest.core import all_of

from finders import SingleWidgetFinder, TopLevelWindowFinder, RecursiveWidgetFinder
from matchers import ShowingOnScreenMatcher


def main_window(*matchers):
    return SingleWidgetFinder(RecursiveWidgetFinder(QMainWindow, all_of(*matchers),
                                                    TopLevelWindowFinder(QApplication.instance())))


class WidgetAssertionProbe():

    def __init__(self, selector, assertion):
        self.selector = selector
        self.assertion = assertion
        self.assertion_met = False

    def test(self):
        self.selector.test()
        self.assertion_met = \
            self.selector.is_satisfied() \
            and self.assertion.matches(self.selector.widget())

    def is_satisfied(self):
        return self.assertion_met

    def describe_to(self, description):
        description.append_description_of(self.selector). \
            append_text(" and check that it is "). \
            append_description_of(self.assertion)

    def describe_failure_to(self, description):
        self.selector.describe_failure_to(description)
        if self.selector.is_satisfied():
            description.append_text(" it ")
            if self.assertion_met:
                description.append_text("is ")
            else:
                description.append_text("is not ")
            description.append_description_of(self.assertion)


class WidgetDriver(object):

    def __init__(self, selector, prober):
        self.selector = selector
        self.prober = prober

    def is_showing_on_screen(self):
        self.is_(ShowingOnScreenMatcher())

    def is_(self, criteria):
        self.check(WidgetAssertionProbe(self.selector, criteria))

    def check(self, probe):
        self.prober.check(probe)


class MainWindowDriver(WidgetDriver):

    def __init__(self, selector, prober):
        super(MainWindowDriver, self).__init__(selector, prober)

    def main_window(self):
        self.check(self.selector)
        return self.selector.widget()

    def close(self):
        self._manipulate(lambda widget: widget.close())

    def _manipulate(self, manipulation):
        self.check(self.selector)
        manipulation(self.selector.widget())


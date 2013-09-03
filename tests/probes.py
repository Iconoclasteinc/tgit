# -*- coding: utf-8 -*-

from PyQt4.Qt import QPoint, QRect
from probing import Probe


class WidgetAssertionProbe(Probe):
    def __init__(self, selector, assertion):
        super(WidgetAssertionProbe, self).__init__()
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
        super(WidgetManipulationProbe, self).__init__()
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


class WidgetScreenBoundsProbe(Probe):
    def __init__(self, selector):
        super(WidgetScreenBoundsProbe, self).__init__()
        self._selector = selector

    def bounds(self):
        return self._bounds

    def describe_to(self, description):
        description.append_text("dimensions of ")
        description.append_description_of(self._selector)

    def describe_failure_to(self, description):
        self._selector.describe_failure_to(description)
        if self._selector.is_satisfied():
            description.append_text(" which had no dimensions")

    def is_satisfied(self):
        return (self._bounds is not None and self._bounds.width > 0 and
                self._bounds.height() > 0) or False

    def test(self):
        self._selector.test()

        if len(self._selector.widgets()) == 0:
            self._bounds = None
            return

        widget = self._selector.widget()
        if widget.isVisible():
            self._bounds = QRect(widget.mapToGlobal(QPoint(0, 0)), widget.size())
        else:
            self._bounds = None

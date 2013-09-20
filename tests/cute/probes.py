# -*- coding: utf-8 -*-

from PyQt4.Qt import QPoint, QRect
from .prober import Probe


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


class WidgetPropertyAssertionProbe(Probe):
    def __init__(self, selector, property_value_query, property_value_matcher):
        super(WidgetPropertyAssertionProbe, self).__init__()
        self._selector = selector
        self._property_value_query = property_value_query
        self._property_value_matcher = property_value_matcher
        self._property_value = None

    def test(self):
        self._selector.test()
        if self._selector.is_satisfied():
            self._property_value = self._property_value_query(self._selector.widget())

    def is_satisfied(self):
        return self._selector.is_satisfied and \
               self._property_value_matcher.matches(self._property_value)

    def describe_to(self, description):
        description.append_description_of(self._selector)\
            .append_text(" and check that its ")\
            .append_description_of(self._property_value_query)\
            .append_text(" is ")\
            .append_description_of(self._property_value_matcher)

    def describe_failure_to(self, description):
        self._selector.describe_failure_to(description)
        if self._selector.is_satisfied():
            description.append_text(" ")\
                .append_description_of(self._property_value_query)\
                .append_text(" was ")\
                .append_value(self._property_value)


class WidgetManipulatorProbe(Probe):
    def __init__(self, finder, manipulation, description):
        super(WidgetManipulatorProbe, self).__init__()
        self._finder = finder
        self._manipulate = manipulation
        self._description = description

    def describe_to(self, description):
        self._finder.describe_to(description)
        description.append_text(" and %s " % self._description)

    def describe_failure_to(self, description):
        self._finder.describe_failure_to(description)

    def is_satisfied(self):
        return self._finder.is_satisfied()

    def test(self):
        self._finder.test()
        if self._finder.is_satisfied():
            for widget in self._finder.widgets():
                self._manipulate(widget)


class WidgetScreenBoundsProbe(Probe):
    def __init__(self, selector):
        super(WidgetScreenBoundsProbe, self).__init__()
        self._selector = selector
        self._bounds = None

    @property
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

        if not self._selector.is_satisfied():
            self._bounds = None
            return

        widget = self._selector.widget()
        if widget.isVisible():
            self._bounds = QRect(widget.mapToGlobal(QPoint(0, 0)), widget.size())
        else:
            self._bounds = None

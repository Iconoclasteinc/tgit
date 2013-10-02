# -*- coding: utf-8 -*-

from PyQt4.QtCore import QPoint, QRect

from tests.cute.prober import Probe


class WidgetAssertionProbe(Probe):
    def __init__(self, selector, assertion):
        super(WidgetAssertionProbe, self).__init__()
        self._selector = selector
        self._assertion = assertion
        self._assertionMet = False

    def test(self):
        self._selector.test()
        self._assertionMet = \
            self._selector.isSatisfied() and \
            self._assertion.matches(self._selector.widget())

    def isSatisfied(self):
        return self._assertionMet

    def describeTo(self, description):
        description.append_description_of(self._selector). \
            append_text("\nand check that it is "). \
            append_description_of(self._assertion)

    def describeFailureTo(self, description):
        self._selector.describeFailureTo(description)
        if self._selector.isSatisfied():
            description.append_text("\n    it ")
            self._assertion.describe_mismatch(self._selector.widget(), description)


class WidgetPropertyAssertionProbe(Probe):
    def __init__(self, selector, query, matcher):
        super(WidgetPropertyAssertionProbe, self).__init__()
        self._selector = selector
        self._propertyValueQuery = query
        self._propertyValueMatcher = matcher
        self._propertyValue = None

    def test(self):
        self._selector.test()
        if self._selector.isSatisfied():
            self._propertyValue = self._propertyValueQuery(self._selector.widget())

    def isSatisfied(self):
        return self._selector.isSatisfied and \
               self._propertyValueMatcher.matches(self._propertyValue)

    def describeTo(self, description):
        description.append_description_of(self._selector) \
            .append_text("\nand check that its ") \
            .append_description_of(self._propertyValueQuery) \
            .append_text(" is ") \
            .append_description_of(self._propertyValueMatcher)

    def describeFailureTo(self, description):
        self._selector.describeFailureTo(description)
        if self._selector.isSatisfied():
            description.append_text("\n    its ") \
                .append_description_of(self._propertyValueQuery) \
                .append_text(" ")
            self._propertyValueMatcher.describe_mismatch(self._propertyValue, description)


class WidgetManipulatorProbe(Probe):
    def __init__(self, finder, manipulation, description):
        super(WidgetManipulatorProbe, self).__init__()
        self._finder = finder
        self._manipulate = manipulation
        self._description = description

    def describeTo(self, description):
        self._finder.describeTo(description)
        description.append_text("\nand %s " % self._description)

    def describeFailureTo(self, description):
        self._finder.describeFailureTo(description)

    def isSatisfied(self):
        return self._finder.isSatisfied()

    def test(self):
        self._finder.test()
        if self._finder.isSatisfied():
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

    def describeTo(self, description):
        description.append_text("dimensions of ")
        description.append_description_of(self._selector)

    def describeFailureTo(self, description):
        self._selector.describeFailureTo(description)
        if self._selector.isSatisfied():
            description.append_text(" which had no dimensions")

    def isSatisfied(self):
        return (self._bounds is not None and self._bounds.width > 0 and
                self._bounds.height() > 0) or False

    def test(self):
        self._selector.test()

        if not self._selector.isSatisfied():
            self._bounds = None
            return

        widget = self._selector.widget()
        if widget.isVisible():
            self._bounds = QRect(widget.mapToGlobal(QPoint(0, 0)), widget.size())
        else:
            self._bounds = None


class ValueMatcherProbe(Probe):
    def __init__(self, matcher, message):
        super(ValueMatcherProbe, self).__init__()
        self._valueMatcher = matcher
        self._message = message
        self._hasReceivedAValue = False
        self._receivedValue = None

    def test(self):
        pass

    def isSatisfied(self):
        return self._valueMatcher.matches(self._receivedValue)

    def describeTo(self, description):
        description.append_text(self._message).append_text(" ") \
            .append_description_of(self._valueMatcher)

    def describeFailureTo(self, description):
        description.append_text(self._message).append_text(" ")
        if self._hasReceivedAValue:
            description.append_text("received ").append_value(self._receivedValue)
        else:
            description.append_text("received nothing")

    def setReceivedValue(self, receivedValue):
        self._receivedValue = receivedValue
        self._hasReceivedAValue = True
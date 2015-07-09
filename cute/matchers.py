# -*- coding: utf-8 -*-
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from . import properties


def named(name):
    return with_(properties.name(), wrap_matcher(name))


def with_buddy(buddy):
    return with_(properties.label_buddy(), wrap_matcher(buddy))


def with_pixmap_height(height):
    return with_(properties.pixmap_height(), wrap_matcher(height))


def with_pixmap_width(width):
    return with_(properties.pixmap_width(), wrap_matcher(width))


def with_text(text):
    return with_(properties.text(), wrap_matcher(text))


def with_data(data):
    return with_(properties.data(), wrap_matcher(data))


def with_list_item_text(text):
    return with_(properties.list_item_text(), wrap_matcher(text))


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


def existing():
    return anything()


def with_children(type_, matcher):
    return ChildrenOfTypeMatcher(type_, matcher)


def showing_on_screen():
    return StateMatcher(lambda o: o.isVisible(), "showing on screen", "hidden")


def hidden():
    return StateMatcher(lambda o: not o.isVisible(), "hidden", "visible")


def enabled():
    return StateMatcher(lambda o: o.isEnabled(), "enabled", "disabled")


def disabled():
    return StateMatcher(lambda o: not o.isEnabled(), "disabled", "enabled")


def checked():
    return StateMatcher(lambda o: o.isChecked(), "checked", "unchecked")


def unchecked():
    return StateMatcher(lambda o: not o.isChecked(), "unchecked", "checked")


def active_window():
    return StateMatcher(lambda w: w.isActiveWindow(), "ready", "not ready")


class QueryResultMatcher(BaseMatcher):
    def __init__(self, query, matcher):
        super().__init__()
        self._query = query
        self._result_matcher = matcher

    def _matches(self, widget):
        return widget and self._result_matcher.matches(self._query(widget))

    def describe_to(self, description):
        description.append_text("with ") \
            .append_description_of(self._query) \
            .append_text(" ") \
            .append_description_of(self._result_matcher)

    def describe_mismatch(self, widget, mismatch_description):
        if widget is None:
            mismatch_description.append_text("was ").append_description_of(widget)
        else:
            mismatch_description.append_description_of(self._query).append_text(" ")
            self._result_matcher.describe_mismatch(self._query(widget), mismatch_description)


class StateMatcher(BaseMatcher):
    def __init__(self, state, description, opposite_description):
        super().__init__()
        self._state = state
        self._state_description = description
        self._opposite_state_description = opposite_description

    def _matches(self, widget):
        return self._state(widget)

    def describe_to(self, description):
        description.append(self._state_description)

    def describe_mismatch(self, widget, mismatch_description):
        mismatch_description.append_text("was ").append_text(self._opposite_state_description)


class ChildrenOfTypeMatcher(BaseMatcher):
    def __init__(self, type_, matcher):
        super().__init__()
        self.matcher = matcher
        self.type = type_

    def _matches(self, widget):
        return self.matcher.matches(widget.findChildren(self.type))

    def describe_to(self, description):
        description.append_text("with children of type ").append_value(self.type).append_text(" ").append(self.matcher)

    def describe_mismatch(self, widget, mismatch_description):
        self.matcher.describe_mismatch(widget.findChildren(self.type), mismatch_description)

# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
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


def with_list_item_text(text):
    return with_(properties.list_item_text(), wrap_matcher(text))


def with_title(text):
    return with_(properties.title(), wrap_matcher(text))


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


def existing():
    return anything()


def showing_on_screen():
    return StateMatcher(QWidget.isVisible, 'showing on screen', 'hidden')


def hidden():
    return StateMatcher(lambda w: not w.isVisible(), 'hidden', 'visible')


def enabled():
    return StateMatcher(lambda w: w.isEnabled(), 'enabled', 'disabled')


def disabled():
    return StateMatcher(lambda w: not w.isEnabled(), 'disabled', 'enabled')


def checked():
    return StateMatcher(lambda b: b.isChecked(), 'checked', 'unchecked')


def unchecked():
    return StateMatcher(lambda b: not b.isChecked(), 'unchecked', 'checked')


class QueryResultMatcher(BaseMatcher):
    def __init__(self, query, matcher):
        super(BaseMatcher, self).__init__()
        self._query = query
        self._result_matcher = matcher

    def _matches(self, item):
        return item and self._result_matcher.matches(self._query(item))

    def describe_to(self, description):
        description.append_text('with ') \
            .append_description_of(self._query) \
            .append_text(" ") \
            .append_description_of(self._result_matcher)

    def describe_mismatch(self, item, mismatch_description):
        if item is None:
            mismatch_description.append_text('was ').append_description_of(item)
        else:
            mismatch_description.append_description_of(self._query).append_text(" ")
            self._result_matcher.describe_mismatch(self._query(item), mismatch_description)


class StateMatcher(BaseMatcher):
    def __init__(self, state, description, opposite_description):
        super(StateMatcher, self).__init__()
        self._state = state
        self._state_description = description
        self._opposite_state_description = opposite_description

    def _matches(self, item):
        return self._state(item)

    def describe_to(self, description):
        description.append(self._state_description)

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was ') \
            .append_text(self._opposite_state_description)
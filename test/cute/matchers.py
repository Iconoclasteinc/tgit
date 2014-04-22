# -*- coding: utf-8 -*-
from hamcrest import anything

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from PyQt4.QtGui import QWidget

from test.cute import properties


def named(name):
    return with_(properties.name(), wrap_matcher(name))


def withBuddy(buddy):
    return with_(properties.labelBuddy(), wrap_matcher(buddy))


def withPixmapHeight(height):
    return with_(properties.pixmapHeight(), wrap_matcher(height))


def withPixmapWidth(width):
    return with_(properties.pixmapWidth(), wrap_matcher(width))


def withText(text):
    return with_(properties.text(), wrap_matcher(text))


def withListItemText(text):
    return with_(properties.listItemText(), wrap_matcher(text))


def withTitle(text):
    return with_(properties.title(), wrap_matcher(text))


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


def existing():
    return anything()


def showingOnScreen():
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
        self._resultMatcher = matcher

    def _matches(self, item):
        return item and self._resultMatcher.matches(self._query(item))

    def describe_to(self, description):
        description.append_text('with ') \
            .append_description_of(self._query) \
            .append_text(" ") \
            .append_description_of(self._resultMatcher)

    def describe_mismatch(self, item, mismatch_description):
        if item is None:
            mismatch_description.append_text('was ').append_description_of(item)
        else:
            mismatch_description.append_description_of(self._query).append_text(" ")
            self._resultMatcher.describe_mismatch(self._query(item), mismatch_description)


class StateMatcher(BaseMatcher):
    def __init__(self, state, description, oppositeDescription):
        super(StateMatcher, self).__init__()
        self._state = state
        self._stateDescription = description
        self._oppositeStateDescription = oppositeDescription

    def _matches(self, item):
        return self._state(item)

    def describe_to(self, description):
        description.append(self._stateDescription)

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was ') \
            .append_text(self._oppositeStateDescription)
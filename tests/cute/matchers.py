# -*- coding: utf-8 -*-

from PyQt4.Qt import QWidget
from hamcrest.core.core.isequal import equal_to
from hamcrest.core.base_matcher import BaseMatcher

from tests.cute import properties


def named(name):
    return with_(properties.name(), equal_to(name))


def withBuddy(matcher):
    return with_(properties.buddy(), matcher)


def withPixmapHeight(height):
    return with_(properties.pixmapHeight(), equal_to(height))


def withPixmapWidth(width):
    return with_(properties.pixmapWidth(), equal_to(width))


def withButtonText(text):
    return with_(properties.buttonText(), equal_to(text))


def withListItemText(text):
    return with_(properties.listItemText(), equal_to(text))


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


def showingOnScreen():
    return StateMatcher(QWidget.isVisible, "showing on screen", "hidden")


def hidden():
    return StateMatcher(lambda w: not w.isVisible(), "hidden", "visible")


def enabled():
    return StateMatcher(QWidget.isEnabled, "enabled", "disabled")


def disabled():
    return StateMatcher(lambda w: not w.isEnabled(), "disabled", "enabled")


class QueryResultMatcher(BaseMatcher):
    def __init__(self, query, matcher):
        super(BaseMatcher, self).__init__()
        self._query = query
        self._resultMatcher = matcher

    def _matches(self, item):
        return item and self._resultMatcher.matches(self._query(item))

    def describe_to(self, description):
        description.append_text("with ") \
            .append_description_of(self._query) \
            .append_text(" ") \
            .append_description_of(self._resultMatcher)

    def describe_mismatch(self, item, mismatch_description):
        if item is None:
            mismatch_description.append_text("was ").append_description_of(item)
        else:
            mismatch_description.append_text("was with ") \
                .append_description_of(self._query) \
                .append_text(" ")
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
        mismatch_description.append_text("was ") \
            .append_text(self._oppositeStateDescription)
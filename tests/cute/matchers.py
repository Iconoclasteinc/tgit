# -*- coding: utf-8 -*-

from PyQt4.Qt import QWidget
from hamcrest.core.core.isequal import equal_to
from hamcrest.core.base_matcher import BaseMatcher

from tests.cute import properties


def named(name):
    return with_(properties.name(), equal_to(name))


def withButtonText(text):
    return with_(properties.buttonText(), equal_to(text))


def withListItemText(text):
    return with_(properties.listItemText(), equal_to(text))


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


def showingOnScreen():
    return ShowingOnScreenMatcher()


class QueryResultMatcher(BaseMatcher):
    def __init__(self, query, matcher):
        super(BaseMatcher, self).__init__()
        self._query = query
        self._resultMatcher = matcher

    def _matches(self, item):
        return item and self._resultMatcher.matches(self._query(item))

    def describe_to(self, description):
        description.append_text("with "). \
            append_description_of(self._query). \
            append_text(" "). \
            append_description_of(self._resultMatcher)


class ShowingOnScreenMatcher(BaseMatcher):
    def _matches(self, item):
        if not isinstance(item, QWidget):
            return False

        return item.isVisible()

    def describe_to(self, description):
        description.append("showing on screen")




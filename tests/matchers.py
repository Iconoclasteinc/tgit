# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt, QWidget
from hamcrest.core.core.isequal import equal_to
from hamcrest.core.base_matcher import BaseMatcher

import properties


def named(name):
    return with_(properties.name(), equal_to(name))


def with_button_text(text):
    return with_(properties.button_text(), equal_to(text))


def with_list_item_text(text):
    return with_(properties.list_item_text(), equal_to(text))


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


def showing_on_screen():
    return ShowingOnScreenMatcher()


class QueryResultMatcher(BaseMatcher):
    def __init__(self, query, matcher):
        super(BaseMatcher, self).__init__()
        self._query = query
        self._result_matcher = matcher

    def _matches(self, item):
        return item and self._result_matcher.matches(self._query(item))

    def describe_to(self, description):
        description.append_text("with "). \
            append_description_of(self._query). \
            append_text(" "). \
            append_description_of(self._result_matcher)


class ShowingOnScreenMatcher(BaseMatcher):
    def _matches(self, item):
        if not isinstance(item, QWidget):
            return False

        return item.isVisible()

    def describe_to(self, description):
        description.append("showing on screen")




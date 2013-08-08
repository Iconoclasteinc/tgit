# -*- coding: utf-8 -*-

from hamcrest.core.core.isequal import IsEqual
from hamcrest.core.base_matcher import BaseMatcher
from PyQt4.QtGui import QWidget

import queries


def named(name):
    return with_(queries.name(), IsEqual(name))


def showing_on_screen():
    return ShowingOnScreenMatcher()


def with_(query, matcher):
    return QueryResultMatcher(query, matcher)


class QueryResultMatcher(BaseMatcher):

    def __init__(self, query, matcher):
        self.query = query
        self.result_matcher = matcher

    def _matches(self, item):
        return item and self.result_matcher.matches(self.query(item))

    def describe_to(self, description):
        description.append_text("with "). \
            append_description_of(self.query). \
            append_text(" "). \
            append_description_of(self.result_matcher)


class ShowingOnScreenMatcher(BaseMatcher):

    def _matches(self, item):
        if not isinstance(item, QWidget):
            return False

        return item.isVisible()

    def describe_to(self, description):
        description.append("showing on screen")




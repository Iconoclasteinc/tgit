# -*- coding: utf-8 -*-

import pytest
from flexmock import flexmock as mock
from hamcrest import contains, assert_that, empty

from test.util.builders import make_project
from testing.matchers import snapshot_with_path
from tgit.project_history import ProjectHistory

pytestmark = pytest.mark.unit


@pytest.fixture()
def history():
    return ProjectHistory()


@pytest.fixture()
def subscriber():
    return mock()


def test_is_initially_emtpy(history):
    assert_that(history, contains(), "history with no element")
    assert_that(history, empty(), "empty history")


def test_maintains_a_list_of_past_projects_in_reverse_order_of_opening(history):
    history.project_opened(make_project(filename='oldest.tgit'))
    history.project_opened(make_project(filename='previous.tgit'))
    history.project_opened(make_project(filename='latest.tgit'))

    assert_that(history, contains(snapshot_with_path("latest.tgit"),
                                  snapshot_with_path("previous.tgit"),
                                  snapshot_with_path("oldest.tgit")), "past projects")


def test_reports_history_changed_when_project_opened(history, subscriber):
    subscriber.should_receive("history_changed").once()
    history.history_changed.subscribe(subscriber.history_changed)

    history.project_opened(make_project(filename="latest"))

# -*- coding: utf-8 -*-

import pytest
from flexmock import flexmock as mock
from hamcrest import contains, assert_that, empty

from testing.builders import make_project, make_snapshot
from testing.matchers import snapshot_with
from tgit.project_history import ProjectHistory

pytestmark = pytest.mark.unit


@pytest.fixture()
def subscriber():
    return mock()


def test_is_initially_emtpy():
    history = ProjectHistory()
    assert_that(history, contains(), "history with no element")
    assert_that(history, empty(), "empty history")


def test_maintains_a_list_of_past_projects_in_reverse_order_of_opening():
    history = ProjectHistory()
    history.project_opened(make_project(filename='oldest.tgit'))
    history.project_opened(make_project(filename='previous.tgit'))
    history.project_opened(make_project(filename='latest.tgit'))

    assert_that(history, contains(snapshot_with(path="latest.tgit"),
                                  snapshot_with(path="previous.tgit"),
                                  snapshot_with(path="oldest.tgit")), "past projects")


def test_updates_history_and_reports_history_change_when_project_changes(subscriber):
    history = ProjectHistory(make_snapshot(path="updated.tgit", name="original"))

    subscriber.should_receive("history_changed").once()
    history.on_history_changed.subscribe(subscriber.history_changed)

    history.project_opened(make_project(filename="updated.tgit", release_name="updated"))

    assert_that(history, contains(snapshot_with(path="updated.tgit", name="updated")), "updated project history")


def test_reorders_history_to_reflect_latest_updates():
    history = ProjectHistory(make_snapshot(path="1.tgit"),
                             make_snapshot(path="2.tgit"),
                             make_snapshot(path="3.tgit"))

    history.project_saved(make_project(filename="2.tgit"))

    assert_that(history, contains(snapshot_with(path="2.tgit"),
                                  snapshot_with(path="1.tgit"),
                                  snapshot_with(path="3.tgit")), "updated project history")


def test_limits_history_to_last_10_entries():
    history = ProjectHistory()
    for index in range(15):
        history.project_opened(make_project(filename=str(index)))

    assert_that(history, contains(*(snapshot_with(path=str(index)) for index in reversed(range(5, 15)))))

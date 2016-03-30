# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, is_, match_equality as matching, contains

from test.util.builders import make_project_history, make_project
from testing.matchers import snapshot_with_path
from tgit.project_history import load_from

pytestmark = pytest.mark.unit


@pytest.fixture()
def store():
    return mock()


@pytest.fixture()
def studio():
    return mock(project_opened=mock())


def test_loads_project_history_from_store_and_then_reports_to_history_when_a_project_is_opened(studio, store):
    history = make_project_history()
    store.should_receive("load_history").and_return(history)

    studio.project_opened.should_receive("subscribe").with_args(history.project_opened).once()

    assert_that(load_from(studio, store), is_(history), "history")


def test_saves_history_to_store_whenever_it_changes(studio, store):
    history = make_project_history()
    store.should_receive("load_history").and_return(history)
    studio.project_opened.should_receive("subscribe").with_args(history.project_opened)

    store.should_receive("store_history").with_args(matching(contains(snapshot_with_path("/new")))).once()

    history = load_from(studio, store)
    history.project_opened(make_project("/new"))

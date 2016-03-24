# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock

from test.util.builders import make_project_history
from tgit.project_history import load

pytestmark = pytest.mark.unit


@pytest.fixture()
def history_store():
    return mock()


@pytest.fixture()
def studio():
    return mock(project_opened=mock())


def test_loads_history_from_store_and_then_reports_when_project_opened_in_studio_to_history(studio, history_store):
    history = make_project_history()
    history_store.should_receive("load_history").and_return(history)

    studio.project_opened.should_receive("subscribe").with_args(history.project_opened).once()

    load(studio, from_store=history_store)

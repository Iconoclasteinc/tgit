# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, none, is_

from tgit.project_studio import ProjectStudio

pytestmark = pytest.mark.unit


@pytest.fixture()
def studio():
    return ProjectStudio()


@pytest.fixture()
def subscriber():
    return mock()


def test_has_initially_no_project_being_worked_on(studio):
    assert_that(studio.current_project, none(), "initial project")


def test_keeps_track_of_current_project(studio):
    studio.project_loaded("/path/to/project")

    assert_that(studio.current_project, is_("/path/to/project"), "opened project")


def test_signals_when_project_opened(studio, subscriber):
    subscriber.should_receive("project_opened").with_args("/path/to/project").once()
    studio.project_opened.subscribe(subscriber.project_opened)

    studio.project_loaded("/path/to/project")

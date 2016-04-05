# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, none, is_

from testing.builders import make_project
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
    current_project = make_project()
    studio.project_loaded(current_project)

    assert_that(studio.current_project, is_(current_project), "current project")


def test_signals_project_opened_when_project_loaded(studio, subscriber):
    opened_project = make_project()

    subscriber.should_receive("project_opened").with_args(opened_project).once()
    studio.on_project_opened.subscribe(subscriber.project_opened)

    studio.project_loaded(opened_project)


def test_signals_project_opened_when_project_created(studio, subscriber):
    new_project = make_project()

    subscriber.should_receive("project_opened").with_args(new_project).once()
    studio.on_project_opened.subscribe(subscriber.project_opened)

    studio.project_created(new_project)


def test_signals_project_saved_when_project_saved(studio, subscriber):
    updated_project = make_project()

    subscriber.should_receive("project_saved").with_args(updated_project).once()
    studio.on_project_saved.subscribe(subscriber.project_saved)

    studio.project_saved(updated_project)

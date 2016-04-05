# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock

from testing.builders import make_project
from tgit import project

pytestmark = pytest.mark.unit


@pytest.fixture()
def studio():
    return mock()


@pytest.fixture
def catalog():
    return mock()


def test_saves_project_to_catalog_and_then_reports_save_success_to_studio(studio, catalog):
    project_to_save = make_project()

    catalog.should_receive("save_project").with_args(project_to_save).once().ordered()
    studio.should_receive("project_saved").with_args(project_to_save).once().ordered()

    project.save_to(studio, catalog=catalog)(project_to_save)

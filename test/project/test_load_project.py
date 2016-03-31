# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, contains

from test.util.builders import make_portfolio, make_project
from tgit import project

pytestmark = pytest.mark.unit


@pytest.fixture()
def studio():
    return mock()


@pytest.fixture()
def portfolio():
    return make_portfolio()


@pytest.fixture
def catalog():
    return mock()


def test_loads_project_from_catalog_and_then_reports_load_success_to_studio(studio, portfolio, catalog):
    project_to_load = make_project()
    catalog.should_receive("load_project").with_args("/path/to/project.tgit").and_return(project_to_load)
    studio.should_receive("project_loaded").with_args(project_to_load).once()

    project.load_to(studio, portfolio, from_catalog=catalog)(filename="/path/to/project.tgit")

    assert_that(portfolio, contains(project_to_load), "album portfolio")

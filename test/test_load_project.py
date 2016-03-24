# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, has_key, contains
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from test.util.builders import make_album, make_portfolio
from tgit.project import load

pytestmark = pytest.mark.unit


@pytest.fixture()
def studio():
    return mock()


@pytest.fixture()
def portfolio():
    return make_portfolio()


@pytest.fixture
def project_catalog():
    class InMemoryProjectCatalog:
        def __init__(self):
            self._projects = {}

        def project_exists(self, filename):
            return filename in self._projects

        def load_project(self, filename):
            return self._projects[filename]

        def save_project(self, album):
            self._projects[album.filename] = album

        add = save_project

        def assert_contains(self, album):
            assert_that(self._projects, has_key(album.filename), "list of albums in catalog")
            assert_that(self._projects[album.filename], wrap_matcher(album), "album {}".format(album.filename))

    return InMemoryProjectCatalog()


def test_loads_project_from_catalog_and_then_reports_load_success_to_studio(studio, portfolio, project_catalog):
    project_to_load = make_album("/path/to/project.tgit")
    project_catalog.add(project_to_load)

    studio.should_receive("project_loaded").with_args("/path/to/project.tgit").once()

    load(studio, portfolio, from_catalog=project_catalog)(filename="/path/to/project.tgit")

    assert_that(portfolio, contains(project_to_load), "album portfolio")



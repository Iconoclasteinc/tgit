# -*- coding: utf-8 -*-
import os

import pytest
from flexmock import flexmock as mock

from hamcrest import assert_that, contains, match_equality as matching

from test.util.builders import make_portfolio, make_track
from testing.matchers import project_with, track_with
from tgit import project

pytestmark = pytest.mark.unit


@pytest.fixture()
def studio():
    return mock()


@pytest.fixture()
def portfolio():
    return make_portfolio()


@pytest.fixture
def album_catalog():
    return mock()


@pytest.fixture
def track_catalog():
    return mock()


def test_creates_and_adds_new_project_to_catalog_and_then_reports_creation_to_studio(studio, portfolio, album_catalog):
    new_project = matching(
        project_with(type="mp3", filename=os.path.normpath("/workspace/Project/Project.tgit"), release_name="Project"))
    album_catalog.should_receive("save_project").with_args(new_project).once().ordered()
    studio.should_receive("project_created").with_args(new_project).once().ordered()

    project.create_in(studio, portfolio, to_catalog=album_catalog)(type_="mp3", name="Project",
                                                                   location=os.path.normpath("/workspace"))

    assert_that(portfolio, contains(new_project), "portfolio content")


def test_imports_project_from_an_existing_track_if_specified(studio, portfolio, album_catalog, track_catalog):
    reference_track = make_track(filename="track.mp3", release_name="Track Release", lead_performer="Track Artist",
                                 track_title="Track Title")
    track_catalog.should_receive("load_track").with_args("track.mp3").and_return(reference_track)

    imported_project = matching(project_with(release_name="Project", lead_performer="Track Artist",
                                             tracks=contains(track_with(track_title="Track Title"))))

    album_catalog.should_receive("save_project").with_args(imported_project).once().ordered()
    studio.should_receive("project_created").with_args(imported_project).once().ordered()

    project.create_in(studio, portfolio, to_catalog=album_catalog, from_catalog=track_catalog)(
        type_="mp3", name="Project", location="/workspace", reference_track_file="track.mp3")

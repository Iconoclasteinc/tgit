# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, equal_to, match_equality as matching

from test.util.builders import make_project, make_image
from testing.matchers import image_with
from tgit.metadata import Image
from tgit.project_history import ProjectSnapshot


@pytest.fixture()
def scaler():
    return mock()


def test_snapshots_project_filename():
    project = make_project(filename="project.tgit")
    snapshot = ProjectSnapshot.of(project)
    assert_that(snapshot.path, equal_to("project.tgit"), "snapshot's path")


def test_snapshots_project_name():
    project = make_project(release_name="Original")
    snapshot = ProjectSnapshot.of(project)
    project.release_name = "Updated"
    assert_that(snapshot.name, equal_to("Original"), "snapshot's name")


def test_snapshots_project_type():
    project = make_project(type_="flac")
    snapshot = ProjectSnapshot.of(project)
    project.type = "mp3"
    assert_that(snapshot.type, equal_to("flac"), "snapshot's type")


def test_snapshots_thumbnail_of_project_main_cover(scaler):
    project = make_project(images=[make_image(mime="image/png", data=b'<image data>')])
    scaler.should_receive("scale").with_args(
        matching(image_with(mime="image/png", data=b'<image data>')), 64, 64).and_return(
        Image(mime="image/png", data=b'<scaled image data>'))

    snapshot = ProjectSnapshot.of(project, image_editor=scaler)

    project.remove_images()
    assert_that(snapshot.cover_art, image_with(mime="image/png", data=b'<scaled image data>'), "snapshot's thumbnail")

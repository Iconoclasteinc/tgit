# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that
from hamcrest import equal_to

from test.util.builders import make_project, make_image
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
    assert_that(snapshot.type_, equal_to("flac"), "snapshot's type")


def test_snapshots_thumbnail_of_project_main_cover(scaler):
    project = make_project(images=[make_image(data=b'<image data>')])
    scaler.should_receive("scale").with_args(b'<image data>', 36, 36).and_return(b'<scaled image data>')

    snapshot = ProjectSnapshot.of(project, scaler=scaler)

    project.remove_images()
    assert_that(snapshot.cover_art, equal_to(b'<scaled image data>'), "snapshot's cover thumbnail")
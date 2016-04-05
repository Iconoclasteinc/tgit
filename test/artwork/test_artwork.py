# -*- coding: utf-8 -*-
import pytest
from flexmock import flexmock
from hamcrest import assert_that, equal_to, has_items, has_item, contains, has_properties
from test.util.builders import make_album, make_image

from test import exception_with_message
from testing import resources
from tgit import fs
from tgit.artwork import ArtworkSelection
from tgit.metadata import Image
from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.unit


def make_cover_art_selection(project=make_album(), preferences=UserPreferences()):
    return ArtworkSelection(project, preferences)


def test_defaults_in_picture_directory():
    prefs = UserPreferences()
    prefs.artwork_selection_folder = "directory"

    assert_that(make_cover_art_selection(preferences=prefs).directory, equal_to("directory"), "The default directory.")


def test_supports_jpeg_format():
    assert_that(make_cover_art_selection().extensions, has_items("jpeg", "jpg", "jpe"), "JPEG extensions supported.")


def test_supports_png_format():
    assert_that(make_cover_art_selection().extensions, has_item("png"), "PNG extension supported.")


def test_changes_project_artwork_to_specified_image_file():
    project = make_album(images=[make_image(mime="image/gif", data="old cover")])

    image = "image/jpeg", fs.read(resources.path("front-cover.jpg"))
    make_cover_art_selection(project=project).artwork_loaded(image)

    assert_that(project.images, contains(has_properties(mime="image/jpeg",
                                                        data=fs.read(resources.path("front-cover.jpg")),
                                                        type=Image.FRONT_COVER,
                                                        desc="Front Cover")), "images")


def test_updates_directory_on_navigation():
    selection = make_cover_art_selection()
    selection.directory_changed("new directory")

    assert_that(selection.directory, equal_to("new directory"), "The current directory.")


def test_reports_failure():
    listener = flexmock()
    listener.should_receive("failed").with_args(exception_with_message("failed")).once()

    selection = make_cover_art_selection()
    selection.on_failure.subscribe(listener.failed)

    selection.failed(Exception("failed"))

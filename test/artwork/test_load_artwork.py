# -*- coding: utf-8 -*-
from flexmock import flexmock
from hamcrest import match_equality, instance_of
import pytest

from test.util import resources
from tgit import artwork, fs

pytestmark = pytest.mark.unit


def test_reports_image_on_successful_load():
    cover_file = resources.path("front-cover.jpg")
    cover_file_data = fs.read(cover_file)

    cover_art_selection = flexmock()
    cover_art_selection.should_receive("artwork_loaded").with_args(("image/jpeg", cover_file_data)).once()

    artwork.load(cover_art_selection)(cover_file)


def test_reports_failure_on_file_not_found():
    cover_file = resources.path("missing_file.jpg")

    cover_art_selection = flexmock()
    cover_art_selection.should_receive("failed").with_args(match_equality(instance_of(FileNotFoundError))).once()

    artwork.load(cover_art_selection)(cover_file)

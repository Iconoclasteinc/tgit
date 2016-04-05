import os

import pytest
from hamcrest import assert_that, is_not, empty, is_, starts_with

from testing import resources
from tgit.audio import WindowsMediaLibrary

pytestmark = pytest.mark.unit


@pytest.yield_fixture
def media_library():
    library = WindowsMediaLibrary()
    yield library
    library.dispose()


def test_creates_temp_directory(media_library):
    media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    assert_that(os.path.exists(media_library._directory), is_(True), "the media library's temporary directory exists")


def test_creates_temp_file_from_filename(media_library):
    media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    assert_that(os.listdir(media_library._directory), is_not(empty()), "the media library's content")


def test_removes_all_temp_files_on_close(media_library):
    media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    media_library.dispose()
    assert_that(os.path.exists(media_library._directory), is_(False), "the media library's temporary directory exists")


def test_creates_qmediacontent_for_temp_file(media_library):
    media_content = media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    assert_that(os.path.normpath(media_content.canonicalUrl().toLocalFile()), starts_with(media_library._directory),
                "the media content's source file")

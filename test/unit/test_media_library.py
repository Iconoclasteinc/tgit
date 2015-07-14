# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import os
import shutil

from hamcrest import assert_that, is_not, empty, is_, starts_with

import pytest

from test.util import resources
from tgit.audio import WindowsMediaLibrary


@pytest.yield_fixture
def media_library():
    library = WindowsMediaLibrary()
    yield library
    library.close()


def test_creates_temp_directory(media_library):
    media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    assert_that(os.path.exists(media_library._directory), is_(True), "the media library's temporary directory exists")


def test_creates_temp_file_from_filename(media_library):
    media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    assert_that(os.listdir(media_library._directory), is_not(empty()), "the media library's content")


def test_removes_all_temp_files_on_close(media_library):
    media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    media_library.close()
    assert_that(os.path.exists(media_library._directory), is_(False), "the media library's temporary directory exists")


def test_creates_qmediacontent_for_temp_file(media_library):
    media_content = media_library.fetch(resources.path("audio", "Rolling in the Deep.mp3"))
    assert_that(os.path.normpath(media_content.canonicalUrl().toLocalFile()), starts_with(media_library._directory),
                "the media content's source file")

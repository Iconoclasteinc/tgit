# -*- coding: utf-8 -*-
from hamcrest import assert_that, equal_to

from test.util import resources
from tgit.util import fs


def test_sanitization_replaces_invalid_characters_in_filename_with_underscores():
    assert_that(fs.sanitize('1/2<3>4:5"6/7\\8?9*10|'), equal_to('1_2_3_4_5_6_7_8_9_10_'), 'sanitized name')


def test_sanitization_strips_leading_and_trailing_whitespace_from_filename():
    assert_that(fs.sanitize('  filename   '), equal_to('filename'), 'sanitized name')


def test_ignores_copy_to_same_destination(tmpdir):
    track_file = tmpdir.join("track.mp3").strpath
    fs.copy(resources.path("base.mp3"), track_file)

    fs.copy(track_file, track_file)

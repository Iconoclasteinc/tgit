# -*- coding: utf-8 -*-
import os

from hamcrest import assert_that, equal_to, contains, empty, ends_with

from test.util import resources
from tgit import fs


def test_sanitization_replaces_invalid_characters_in_filename_with_underscores():
    assert_that(fs.sanitize('1/2<3>4:5"6/7\\8?9*10|'), equal_to('1_2_3_4_5_6_7_8_9_10_'), 'sanitized name')


def test_sanitization_strips_leading_and_trailing_whitespace_from_filename():
    assert_that(fs.sanitize('  filename   '), equal_to('filename'), 'sanitized name')


def test_ignores_copy_to_same_destination(tmpdir):
    track_file = tmpdir.join("track.mp3").strpath
    fs.copy(resources.path("base.mp3"), track_file)

    fs.copy(track_file, track_file)


def test_guesses_file_extension_from_mime_type():
    assert_that(fs.guess_extension("image/png"), equal_to(".png"), "extension for png images")


def test_creates_directory_tree(tmpdir):
    folder = tmpdir.join("path/to/folder").strpath
    fs.mkdirs(folder)

    assert_that(os.path.exists(folder), "folder not created")
    assert_that(os.path.isdir(folder), "not a folder")


def test_list_file_entries_in_folder(tmpdir):
    entries = [tmpdir.join(filename).strpath for filename in ("file1", "file2", "file3")]
    for filename in entries:
        touch(filename)

    for folder in ("dir1", "dir2", "dir3"):
        tmpdir.mkdir(folder)

    assert_that(fs.list_dir(tmpdir.strpath), contains(*entries), "file entries")


def test_ignores_errors_that_might_occur_when_removing_files(tmpdir):
    missing_file = tmpdir.join("missing.mp3").strpath
    fs.remove(missing_file)


def test_normalizes_filenames_to_fully_composed_unicode_strings(tmpdir):
    fully_composed_form = tmpdir.join('Spicy Jalape\u00f1o.tgit').strpath
    fully_decomposed_form = tmpdir.join('Spicy Jalapen\u0303o.tgit').strpath

    touch(fully_decomposed_form)

    assert_that(fs.abspath(fully_decomposed_form), equal_to(fully_composed_form), "absolute path")


def test_removes_files_from_folder_if_they_match_given_condition(tmpdir):
    for filename in "track1.mp3", "track2.flac", "track3.mp3":
        touch(tmpdir.join(filename).strpath)

    fs.remove_files(folder=tmpdir.strpath, matching=lambda entry: entry.endswith(".mp3"))
    assert_that(fs.list_dir(tmpdir.strpath), contains(ends_with("track2.flac")), "files left after removing mp3 files")

    fs.remove_files(folder=tmpdir.strpath)
    assert_that(fs.list_dir(tmpdir.strpath), empty(), "files left after removing remaining files")


def touch(filename):
    with open(filename, "wt") as file:
        file.write("")

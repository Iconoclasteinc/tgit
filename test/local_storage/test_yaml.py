# -*- coding: utf-8 -*-
from hamcrest import assert_that, has_item, contains_string, contains, has_entry
import pytest

from test.util import resources
from tgit.local_storage import yaml
from tgit.metadata import Image


@pytest.yield_fixture
def project_file(tmpdir):
    folder = tmpdir.mkdir("album")

    def path(filename):
        return folder.join(filename).strpath

    yield path
    folder.remove()


def read_lines(file):
    content = open(file, "r", encoding="utf-8").read()
    return content.split("\n")


def test_saves_data_to_yaml_file(project_file):
    album_file = project_file("album.tgit")
    data = dict(version="1.6.0",
                release_name="Title",
                compilation=True,
                lead_performer="Artist",
                isni="0000123456789",
                guestPerformers=[("Guitar", "Guitarist"), ("Piano", "Pianist")],
                label_name="Label",
                catalogNumber="XXX123456789",
                upc="123456789999",
                comments="Comments\n...",
                releaseTime="2009-01-01", recording_time="2008-09-15", recordingStudios="Studios",
                producer="Producer", mixer="Engineer", primary_style="Style",
                images=[("image/jpeg", "Front.jpeg", Image.FRONT_COVER, "Front")],
                tracks=("1st", "2nd", "3rd"))

    yaml.write_data(album_file, data)

    lines = read_lines(album_file)
    assert_that(lines, has_item(contains_string("version: 1.6.0")), "version")
    assert_that(lines, has_item(contains_string("release_name: Title")), "release name")
    assert_that(lines, has_item(contains_string("compilation: true")), "compilation")
    assert_that(lines, has_item(contains_string("lead_performer: Artist")), "lead performer")
    assert_that(lines, has_item(contains_string("isni: 0000123456789")), "isni")
    assert_that(lines, has_item(contains_string("label_name: Label")), "label name")
    assert_that(lines, has_item(contains_string("upc: '123456789999'")), "upc")
    assert_that(lines, has_item(contains_string("comments: 'Comments")), "comments")
    assert_that(lines, has_item(contains_string(" ...'")), "comments")
    assert_that(lines, has_item(contains_string("releaseTime: '2009-01-01'")), "release time")
    assert_that(lines, has_item(contains_string("recording_time: '2008-09-15'")), "recording time")
    assert_that(lines, has_item(contains_string("recordingStudios: Studios")), "recording studios")
    assert_that(lines, has_item(contains_string("producer: Producer")), "producer")
    assert_that(lines, has_item(contains_string("mixer: Engineer")), "mixer")
    assert_that(lines, has_item(contains_string("primary_style: Style")), "primary style")
    assert_that(lines, has_item(contains_string("guestPerformers:")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Guitar")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Guitarist")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Piano")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Pianist")), "guest performers")
    assert_that(lines, has_item(contains_string("images:")), "images")
    assert_that(lines, has_item(contains_string("  - image/jpeg")), "image mime type")
    assert_that(lines, has_item(contains_string("  - Front.jpeg")), "image filename")
    assert_that(lines, has_item(contains_string("  - 1")), "image type")
    assert_that(lines, has_item(contains_string("  - Front")), "image desc")
    assert_that(lines, has_item(contains_string("- 1st")), "1st track")
    assert_that(lines, has_item(contains_string("- 2nd")), "2nd track")
    assert_that(lines, has_item(contains_string("- 3rd")), "3rd track")


def test_reads_data_from_yaml_file():
    data = yaml.read_data(resources.path("album.tgit"))

    assert_that(data, has_entry("version", "1.6.0"), "version")
    assert_that(data, has_entry("type", "mp3"), "album type")
    assert_that(data, has_entry("release_name", "Title"), "release name")
    assert_that(data, has_entry("compilation", True), "compilation")
    assert_that(data, has_entry("lead_performer", "Artist"), "lead performer")
    assert_that(data, has_entry("isni", "0000123456789"), "isni")
    assert_that(data, has_entry("guestPerformers", contains(("Guitar", "Guitarist"), ("Piano", "Pianist"))),
                "guest performers")
    assert_that(data, has_entry("label_name", "Label"), "label name")
    assert_that(data, has_entry("catalogNumber", "XXX123456789"), "catalog number")
    assert_that(data, has_entry("upc", "123456789999"), "upc")
    assert_that(data, has_entry("comments", "Comments\n..."), "comments")
    assert_that(data, has_entry("releaseTime", "2009-01-01"), "release time")
    assert_that(data, has_entry("recording_time", "2008-09-15"), "recording time")
    assert_that(data, has_entry("recordingStudios", "Studios"), "recording studios")
    assert_that(data, has_entry("producer", "Producer"), "producer")
    assert_that(data, has_entry("mixer", "Engineer"), "mixer")
    assert_that(data, has_entry("primary_style", "Style"), "primary style")
    assert_that(data, has_entry("images", contains(("image/jpeg", "Front.jpeg", Image.FRONT_COVER, "Front"))),
                "attached pictures")
    assert_that(data, has_entry("tracks", contains("1st", "2nd", "3rd")))


def test_writes_unicode_strings_in_yaml_file(project_file):
    album_file = project_file("album.tgit")
    data = dict(entry="Les naïfs ægithales hâtifs pondant à Noël...")

    yaml.write_data(album_file, data)
    lines = read_lines(album_file)
    assert_that(lines, has_item(contains_string("Les naïfs ægithales hâtifs pondant à Noël...")), "unicode string")

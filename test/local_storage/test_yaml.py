# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, has_item, contains_string, contains, has_entry, equal_to

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
                lead_performer=("Artist",),
                lead_performer_region=("FR",),
                isnis={"Artist": "0000123456789"},
                guest_performers=[("Guitar", "Guitarist"), ("Piano", "Pianist")],
                label_name="Label",
                catalog_number="XXX123456789",
                upc="123456789999",
                comments="Comments\n...",
                release_time="2009-01-01", recording_time="2008-09-15", original_release_time="2009-01-15",
                contributors=[("Sound", "Sound Engineer"), ("Effects", "Effects Engineer")],
                images=[("image/jpeg", "Front.jpeg", Image.FRONT_COVER, "Front")],
                tracks=("1st", "2nd", "3rd"))

    yaml.write_data(album_file, data)

    lines = read_lines(album_file)
    print(lines)
    assert_that(lines, has_item(contains_string("version: 1.6.0")), "version")
    assert_that(lines, has_item(contains_string("release_name: Title")), "release name")
    assert_that(lines, has_item(contains_string("compilation: true")), "compilation")
    assert_that(lines, has_item(contains_string("lead_performer: !!python/tuple")), "lead performer")
    assert_that(lines, has_item(contains_string("- Artist")), "lead performer")
    assert_that(lines, has_item(contains_string("lead_performer_region:")), "lead performer region")
    assert_that(lines, has_item(contains_string("- FR")), "lead performer region")
    assert_that(lines, has_item(contains_string("isnis:")), "isnis")
    assert_that(lines, has_item(contains_string("  Artist: 0000123456789")), "isnis")
    assert_that(lines, has_item(contains_string("label_name: Label")), "label name")
    assert_that(lines, has_item(contains_string("upc: '123456789999'")), "upc")
    assert_that(lines, has_item(contains_string("comments: 'Comments")), "comments")
    assert_that(lines, has_item(contains_string(" ...'")), "comments")
    assert_that(lines, has_item(contains_string("release_time: '2009-01-01'")), "release time")
    assert_that(lines, has_item(contains_string("recording_time: '2008-09-15'")), "recording time")
    assert_that(lines, has_item(contains_string("original_release_time: '2009-01-15'")), "original release time")
    assert_that(lines, has_item(contains_string("guest_performers:")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Guitar")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Guitarist")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Piano")), "guest performers")
    assert_that(lines, has_item(contains_string("  - Pianist")), "guest performers")
    assert_that(lines, has_item(contains_string("contributors:")), "contributors")
    assert_that(lines, has_item(contains_string("  - Sound")), "contributors")
    assert_that(lines, has_item(contains_string("  - Sound Engineer")), "contributors")
    assert_that(lines, has_item(contains_string("  - Effects")), "contributors")
    assert_that(lines, has_item(contains_string("  - Effects Engineer")), "contributors")
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

    assert_that(data, has_entry("version", "1.11.0"), "version")
    assert_that(data, has_entry("type", "mp3"), "album type")
    assert_that(data, has_entry("release_name", "Title"), "release name")
    assert_that(data, has_entry("compilation", True), "compilation")
    assert_that(data, has_entry("lead_performer", equal_to("Artist")), "lead performer")
    assert_that(data, has_entry("lead_performer_region", ("FR",)), "lead performer region")
    assert_that(data, has_entry("isnis", has_entry("Artist", "0000000123456789")), "isnis")
    assert_that(data, has_entry("guest_performers", contains(("Guitar", "Guitarist"), ("Piano", "Pianist"))),
                "guest performers")
    assert_that(data, has_entry("label_name", "Label"), "label name")
    assert_that(data, has_entry("catalog_number", "XXX123456789"), "catalog number")
    assert_that(data, has_entry("upc", "123456789999"), "upc")
    assert_that(data, has_entry("comments", "Comments\n..."), "comments")
    assert_that(data, has_entry("release_time", "2009-01-01"), "release time")
    assert_that(data, has_entry("recording_time", "2008-09-15"), "recording time")
    assert_that(data, has_entry("original_release_time", "2009-01-15"), "original_release time")
    assert_that(data, has_entry("contributors", contains(("Sound", "Sound Engineer"), ("Effects", "Effects Engineer"))),
                "contributors")
    assert_that(data, has_entry("images", contains(("image/jpeg", "Front.jpeg", Image.FRONT_COVER, "Front"))),
                "attached pictures")
    assert_that(data, has_entry("tracks", contains("1st", "2nd", "3rd")))


def test_writes_unicode_strings_in_yaml_file(project_file):
    album_file = project_file("album.tgit")
    data = dict(entry="Les naïfs ægithales hâtifs pondant à Noël...")

    yaml.write_data(album_file, data)
    lines = read_lines(album_file)
    assert_that(lines, has_item(contains_string("Les naïfs ægithales hâtifs pondant à Noël...")), "unicode string")

# -*- coding: utf-8 -*-
from hamcrest import has_item, contains_string, assert_that, equal_to, contains, is_
import pytest

from test.util.workspace import AlbumWorkspace
from test.util import builders as build, resources
from tgit.local_storage import local_project
from tgit.metadata import Image
from tgit.util import fs


@pytest.yield_fixture
def workspace(tmpdir):
    album_workspace = AlbumWorkspace(tmpdir.mkdir("workspace"))
    yield album_workspace
    album_workspace.delete()


def read_lines(file):
    content = open(file, "r").read()
    return content.split("\n")


def test_saves_album_metadata_to_disk(workspace):
    album_file = workspace.path("album.tgit")
    album = build.album(filename=album_file,
                        release_name="Title", compilation=True, lead_performer="Artist", isni="0000123456789",
                        guestPerformers=[("Guitar", "Guitarist"), ("Piano", "Pianist")], label_name="Label",
                        catalogNumber="XXX123456789", upc="123456789999", comments="Comments\n...",
                        releaseTime="2009-01-01", recording_time="2008-09-15", recordingStudios="Studios",
                        producer="Producer", mixer="Engineer", primary_style="Style",
                        images=[build.image("image/jpeg", fs.binary_content_of(resources.path("front-cover.jpg")),
                                            Image.FRONT_COVER, "Front Cover")])

    local_project.save_album(album)

    lines = read_lines(album_file)
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
    assert_that(lines, has_item(contains_string("  data: !!binary |")), "images")
    assert_that(lines, has_item(
        contains_string("    /9j/4AAQSkZJRgABAQEASABIAAD/4gxYSUNDX1BST0ZJTEUAAQEAAAxITGlubwIQAABtbnRyUkdC")), "images")
    assert_that(lines, has_item(contains_string("  desc: Front Cover")), "images")
    assert_that(lines, has_item(contains_string("  mime: image/jpeg")), "images")
    assert_that(lines, has_item(contains_string("  type: 1")), "images")


def test_load_album_from_project_file():
    album = local_project.load_album(resources.path("album_mp3.tgit"))

    assert_that(album.type, equal_to("mp3"), "album type")
    assert_that(album.release_name, equal_to("Title"), "release name")
    assert_that(album.compilation, is_(True), "compilation")
    assert_that(album.lead_performer, equal_to("Artist"), "lead performer")
    assert_that(album.isni, equal_to("0000123456789"), "isni")
    assert_that(album.guestPerformers, equal_to([("Guitar", "Guitarist"), ("Piano", "Pianist")]), "guest performers")
    assert_that(album.label_name, equal_to("Label"), "label name")
    assert_that(album.catalogNumber, equal_to("XXX123456789"), "catalog number")
    assert_that(album.upc, equal_to("123456789999"), "upc")
    assert_that(album.comments, equal_to("Comments\n..."), "comments")
    assert_that(album.releaseTime, equal_to("2009-01-01"), "release time")
    assert_that(album.recording_time, equal_to("2008-09-15"), "recording time")
    assert_that(album.recordingStudios, equal_to("Studios"), "recording studios")
    assert_that(album.producer, equal_to("Producer"), "producer")
    assert_that(album.mixer, equal_to("Engineer"), "mixer")
    assert_that(album.primary_style, equal_to("Style"), "primary style")
    assert_that(album.images, contains(
        Image("image/jpeg", fs.binary_content_of(resources.path("front-cover.jpg")), Image.FRONT_COVER, "Front Cover")),
        "attached pictures")

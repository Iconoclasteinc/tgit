from hamcrest.library.collection.is_empty import empty
from hamcrest import assert_that, equal_to, has_entries, contains, has_property, all_of, contains_inanyorder, is_not, \
    has_key, has_length, is_in, is_, none
import pytest

from tgit.metadata import Metadata, Image

pytestmark = pytest.mark.unit


def test_is_a_mutable_container():
    metadata = Metadata(artist="James Blunt")
    assert_that(metadata["artist"], equal_to("James Blunt"), "accessed item")
    metadata["artist"] = "Adele"
    assert_that(metadata["artist"], equal_to("Adele"), "assigned item")
    metadata["album"] = "Adele 21"
    assert_that(metadata, has_length(2), "length")
    assert_that("artist", is_in(metadata), "member")
    del metadata["artist"]
    assert_that("title", is_not(is_in(metadata)), "member")


def test_accesses_entries_as_attr0ibutes():
    metadata = Metadata(artist="James Blunt")
    assert_that(metadata.artist, equal_to("James Blunt"), "accessed item")


def test_missing_tag_is_considered_none():
    metadata = Metadata()
    assert_that(metadata["missing"], none(), "missing value")


def test_is_initially_empty():
    metadata = Metadata()
    assert_that(metadata, empty(), "tags")
    assert_that(list(metadata.images), empty(), "images")
    assert_that(metadata.empty(), is_(True), "emptiness")


def test_is_not_empty_when_containing_images():
    metadata = Metadata()
    metadata.addImage("img/jpeg", "...")
    assert_that(metadata.empty(), is_(False), "emptiness")


def test_is_not_empty_when_holding_tags():
    metadata = Metadata()
    metadata["artist"] = "John Doe"
    metadata.addImage("img/jpeg", "...")
    assert_that(metadata.empty(), is_(False), "emptiness")


def test_is_empty_when_cleared():
    metadata = Metadata()
    metadata["artist"] = "John Doe"
    metadata.addImage("img/jpeg", "...")
    metadata.clear()
    assert_that(metadata.empty(), is_(True), "emptiness")


def test_updates_tags_and_replaces_images_when_updated():
    metadata = Metadata()
    metadata["artist"] = "Pascal Obispo"
    metadata.addImage("img/jpeg", "missing")

    other = Metadata()
    other["album"] = "Un jour comme aujourd'hui"
    other.addImage("img/png", "cover.png")

    metadata.update(other)
    assert_that(metadata, has_entries(artist="Pascal Obispo", album="Un jour comme aujourd'hui"), "updated tags")
    assert_that(metadata.images, contains(has_property("data", "cover.png")), "updated images")


def test_copies_a_selection_of_its_tags_with_images():
    metadata = Metadata(artist="Alain Souchon", album="C'est déjà ça", track="Foule sentimentale")
    metadata.addImage("img/jpeg", "front-cover.jpg")
    metadata.addImage("img/jpeg", "back-cover.jpg")

    selection = metadata.copy("artist", "album", "label")

    assert_that(selection, has_length(2))
    assert_that(selection, all_of(has_entries(artist="Alain Souchon", album="C'est déjà ça"),
                                  is_not(has_key("track")), is_not(has_key("label"))), "selected tags")
    assert_that(selection.images, contains(
        has_property("data", "front-cover.jpg"), has_property("data", "back-cover.jpg")), "selected images")


def test_looks_up_images_by_type():
    metadata = Metadata()
    metadata.addImage("img/jpeg", "front-cover.jpg", Image.FRONT_COVER)
    metadata.addImage("img/png", "front-cover.png", Image.FRONT_COVER)
    metadata.addImage("img/jpeg", "back-cover.jpg", Image.BACK_COVER)

    assert_that(metadata.imagesOfType(Image.FRONT_COVER),
                contains_inanyorder(has_property("data", "front-cover.jpg"),
                                    has_property("data", "front-cover.png")),
                "front cover images")

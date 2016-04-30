# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, has_property, equal_to
from hamcrest import contains_inanyorder

from testing.builders import metadata
from tgit.chain_of_title import ChainOfTitle

pytestmark = pytest.mark.unit


def test_builds_contributors_from_metadata():
    chain = ChainOfTitle(metadata(lyricist=["Joel Miller"], composer=["John Roney"]))

    assert_that(chain.contributors, contains_inanyorder(
        has_property("name", "Joel Miller"), has_property("name", "John Roney")), "The contributors")


def test_builds_contributors_from_metadata_with_duplicates_in_both_lyricist_and_composer():
    chain = ChainOfTitle(metadata(lyricist=["Joel Miller", "John Lennon"], composer=["John Roney", "John Lennon"]))

    assert_that(len(chain.contributors), equal_to(3), "The number of contributors")
    assert_that(chain.contributors, contains_inanyorder(
        has_property("name", "Joel Miller"),
        has_property("name", "John Roney"),
        has_property("name", "John Lennon")), "The contributors")


def test_builds_publishers_from_metadata():
    chain = ChainOfTitle(metadata(publisher=["Joel Miller", "John Roney"]))

    assert_that(chain.publishers, contains_inanyorder(
        has_property("name", "Joel Miller"), has_property("name", "John Roney")), "The publishers")

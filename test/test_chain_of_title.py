# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, has_entry, has_entries

from testing.builders import make_metadata, make_track
from tgit.chain_of_title import ChainOfTitle

pytestmark = pytest.mark.unit


def test_updates_contributors():
    track = make_track(metadata_from=make_metadata(lyricist=["Joel Miller"], composer=["John Roney"],
                                                   publisher=["Effendi Records"]))
    chain_of_title = ChainOfTitle(track)

    chain_of_title.update_contributor(**joel_miller())
    chain_of_title.update_contributor(**john_roney())
    chain_of_title.update_contributor(**effendi_records())

    assert_that(track.chain_of_title, has_contributor("Joel Miller", joel_miller()), "The contributors")
    assert_that(track.chain_of_title, has_contributor("John Roney", john_roney()), "The contributors")
    assert_that(track.chain_of_title, has_contributor("Effendi Records", effendi_records()), "The contributors")


def has_contributor(name, contributor):
    return has_entry(name, has_entries(contributor))


def joel_miller():
    return dict(name="Joel Miller", affiliation="SOCAN", publisher="Effendi Records", share="25")


def john_roney():
    return dict(name="John Roney", affiliation="ASCAP", publisher="Effendi Records", share="25")


def effendi_records():
    return dict(name="Effendi Records", share="25")

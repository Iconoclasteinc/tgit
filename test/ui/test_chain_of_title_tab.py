# -*- coding: utf-8 -*-
from hamcrest import has_entries

import pytest

from cute.probes import KeywordsValueMatcherProbe

from cute.widgets import window
from test.ui import show_, close_, ignore
from testing.builders import metadata, make_track
from testing.drivers.chain_of_title_tab_driver import ChainOfTitleTabDriver
from tgit.chain_of_title import ChainOfTitle
from tgit.ui import make_chain_of_title_tab
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab

pytestmark = pytest.mark.ui


def show_page(track, chain, on_contributor_changed=ignore):
    page = make_chain_of_title_tab(track, chain, on_contributor_changed=on_contributor_changed)
    show_(page)
    return page


@pytest.yield_fixture()
def driver(prober, automaton):
    tab_driver = ChainOfTitleTabDriver(window(ChainOfTitleTab), prober, automaton)
    yield tab_driver
    close_(tab_driver, pause=30)


def test_displays_column_headings(driver):
    track = make_track()
    _ = show_page(track, ChainOfTitle(track))

    driver.shows_contributors_column_headers("Name", "Affiliation", "Publisher", "Share (%)")
    driver.shows_publishers_column_headers("Name", "Share (%)")


def test_displays_contributor_names(driver):
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"], composer=["John Roney"]))
    _ = show_page(track, ChainOfTitle(track))

    driver.has_contributors_count(2)
    driver.shows_contributor_row_details("Joel Miller", None, None, None)
    driver.shows_contributor_row_details("John Roney", None, None, None)


def test_displays_publisher_names(driver):
    track = make_track(metadata_from=metadata(publisher=["Rebecca Ann Maloy"]))
    _ = show_page(track, ChainOfTitle(track))

    driver.has_publishers_count(1)
    driver.shows_publisher_row_details("Rebecca Ann Maloy", None)


def test_displays_affiliation_choices(driver):
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"]))
    _ = show_page(track, ChainOfTitle(track))

    driver.shows_affiliation_options_on_row(0, "", "SOCAN", "ASCAP", "BMI")


def test_displays_publisher_choices(driver):
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"], publisher=["Big Deal Music", "Atlas Music"]))
    _ = show_page(track, ChainOfTitle(track))

    driver.shows_publisher_options_on_row(0, "", "Big Deal Music", "Atlas Music")


def test_signals_contributor_changed(driver):
    signal = KeywordsValueMatcherProbe("metadata changed")

    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"], publisher=["Big Deal Music"]))
    _ = show_page(track, ChainOfTitle(track), on_contributor_changed=signal.received)

    signal.expect(has_entries(affiliation="SOCAN"))
    driver.change_affiliation_of_contributor("Joel Miller", "SOCAN")
    driver.check(signal)

    signal.expect(has_entries(publisher="Big Deal Music"))
    driver.change_publisher_of_contributor("Joel Miller", "Big Deal Music")
    driver.check(signal)

    signal.expect(has_entries(share="50"))
    driver.change_share_of_contributor("Joel Miller", "50")
    driver.check(signal)

    signal.expect(has_entries(share="50"))
    driver.change_share_of_publisher("Big Deal Music", "50")
    driver.check(signal)

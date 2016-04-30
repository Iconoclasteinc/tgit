# -*- coding: utf-8 -*-
import pytest

from cute.widgets import window
from test.ui import show_, close_
from testing.builders import metadata
from testing.drivers.chain_of_title_tab_driver import ChainOfTitleTabDriver
from tgit.chain_of_title import ChainOfTitle
from tgit.ui import make_chain_of_title_tab
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab

pytestmark = pytest.mark.ui


def show_page(chain=ChainOfTitle(metadata())):
    page = make_chain_of_title_tab(chain)
    show_(page)
    return page


@pytest.yield_fixture()
def driver(prober, automaton):
    tab_driver = ChainOfTitleTabDriver(window(ChainOfTitleTab), prober, automaton)
    yield tab_driver
    close_(tab_driver)


def test_displays_column_headings(driver):
    _ = show_page()
    driver.shows_contributors_column_headers("Name", "Affiliation", "Publisher", "Share (%)")
    driver.shows_publishers_column_headers("Name", "Share (%)")


def test_displays_contributor_names(driver):
    _ = show_page(ChainOfTitle(metadata(lyricist=["Joel Miller"], composer=["John Roney"])))

    driver.has_contributors_count(2)
    driver.shows_contributor_row_details("Joel Miller", None, None, None)
    driver.shows_contributor_row_details("John Roney", None, None, None)


def test_displays_publisher_names(driver):
    _ = show_page(ChainOfTitle(metadata(publisher=["Rebecca Ann Maloy"])))

    driver.has_publishers_count(1)
    driver.shows_publisher_row_details("Rebecca Ann Maloy", None)

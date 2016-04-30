# -*- coding: utf-8 -*-
import pytest

from cute.widgets import window
from test.ui import show_, close_
from testing.builders import make_track
from testing.drivers.chain_of_title_tab_driver import ChainOfTitleTabDriver
from tgit.ui import make_chain_of_title_tab
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab

pytestmark = pytest.mark.ui


def show_page(track=make_track()):
    page = make_chain_of_title_tab(track)
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

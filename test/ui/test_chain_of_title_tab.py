# -*- coding: utf-8 -*-
from hamcrest import has_entries
import pytest

from cute.probes import KeywordsValueMatcherProbe
from cute.widgets import window
from test.ui import show_, close_, ignore
from testing.builders import make_chain_of_title
from testing.drivers.chain_of_title_tab_driver import ChainOfTitleTabDriver
from tgit.ui import make_chain_of_title_tab
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab

pytestmark = pytest.mark.ui


def show_page(chain_of_title, on_contributor_changed=ignore):
    page = make_chain_of_title_tab(chain_of_title, on_contributor_changed=on_contributor_changed)
    show_(page)
    return page


@pytest.yield_fixture()
def driver(prober, automaton):
    tab_driver = ChainOfTitleTabDriver(window(ChainOfTitleTab), prober, automaton)
    yield tab_driver
    close_(tab_driver, pause=30)


def test_displays_column_headings(driver):
    _ = show_page(make_chain_of_title())

    driver.shows_contributors_column_headers("Name", "Affiliation", "Publisher", "Share (%)")
    driver.shows_publishers_column_headers("Name", "Affiliation", "Share (%)")


def test_displays_contributors(driver):
    chain = make_chain_of_title(authors_composers=[joel_miller(), john_roney()], publishers=[effendi_records()])
    _ = show_page(chain)

    driver.has_contributors_count(2)
    driver.shows_contributor_row_details("Joel Miller", None, None, "25")
    driver.shows_affiliation_of_contributor("Joel Miller", "SOCAN")
    driver.shows_publisher_of_contributor("Joel Miller", "Effendi Records")

    driver.shows_contributor_row_details("John Roney", None, None, "25")
    driver.shows_affiliation_of_contributor("John Roney", "ASCAP")
    driver.shows_publisher_of_contributor("John Roney", "Effendi Records")

    driver.has_publishers_count(1)
    driver.shows_publisher_row_details("Effendi Records", None, "50")
    driver.shows_affiliation_of_publisher("Effendi Records", "BMI")


def test_displays_affiliation_choices(driver):
    _ = show_page(make_chain_of_title(authors_composers=[joel_miller()], publishers=[effendi_records()]))

    driver.shows_affiliation_options_for_contributor("Joel Miller", "", "SOCAN", "ASCAP", "BMI")
    driver.shows_affiliation_options_for_publisher("Effendi Records", "", "SOCAN", "ASCAP", "BMI")


def test_displays_publisher_choices(driver):
    _ = show_page(make_chain_of_title(authors_composers=[joel_miller()],
                                      publishers=[contributor("Big Deal Music"), contributor("Atlas Music")]))

    driver.shows_publisher_options_on_row(0, "", "Big Deal Music", "Atlas Music")


def test_signals_contributor_changed(driver):
    signal = KeywordsValueMatcherProbe("metadata changed")

    _ = show_page(make_chain_of_title(authors_composers=[contributor("Joel Miller")],
                                      publishers=[contributor("Big Deal Music")]),
                  on_contributor_changed=signal.received)

    signal.expect(has_entries(affiliation="SOCAN"))
    driver.change_affiliation_of_contributor("Joel Miller", "SOCAN")
    driver.check(signal)

    signal.expect(has_entries(publisher="Big Deal Music"))
    driver.change_publisher_of_contributor("Joel Miller", "Big Deal Music")
    driver.check(signal)

    signal.expect(has_entries(share="50"))
    driver.change_share_of_contributor("Joel Miller", "50")
    driver.check(signal)

    signal.expect(has_entries(affiliation="BMI"))
    driver.change_affiliation_of_publisher("Big Deal Music", "BMI")
    driver.check(signal)

    signal.expect(has_entries(share="50"))
    driver.change_share_of_publisher("Big Deal Music", "50")
    driver.check(signal)


def joel_miller():
    return dict(name="Joel Miller", affiliation="SOCAN", publisher="Effendi Records", share="25")


def john_roney():
    return dict(name="John Roney", affiliation="ASCAP", publisher="Effendi Records", share="25")


def effendi_records():
    return dict(name="Effendi Records", affiliation="BMI", share="50")


def contributor(name):
    return dict(name=name)

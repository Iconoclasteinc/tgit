# -*- coding: utf-8 -*-
from hamcrest import has_entries
import pytest
from cute.probes import KeywordsValueMatcherProbe

from cute.widgets import window
from test.ui import show_, close_, ignore
from testing.builders import make_album, make_track
from testing.drivers.contributors_tab_driver import ContributorsTabDriver
from tgit.ui import make_contributors_tab
from tgit.ui.pages.contributors_tab import ContributorsTab


def show_contributors(project=make_album(), track=make_track(), on_metadata_changed=ignore):
    page = make_contributors_tab(project, track, on_metadata_changed=on_metadata_changed)
    show_(page)
    return page


@pytest.yield_fixture()
def driver(prober, automaton):
    tab_driver = ContributorsTabDriver(window(ContributorsTab), prober, automaton)
    yield tab_driver
    close_(tab_driver)


def test_displays_column_headings(driver):
    _ = show_contributors(make_album())
    driver.shows_column_headers("Name", "Role", "IPI", "ISNI")
    driver.has_contributors_count(0)


def test_adds_empty_row_to_table_when_clicking_on_add_button(driver):
    _ = show_contributors(make_album())
    driver.add_contributor()
    driver.has_contributors_count(1)
    driver.has_added_empty_row()


def test_removes_row(driver):
    _ = show_contributors(make_album())
    driver.add_contributor()
    driver.remove_contributor_at(0)
    driver.has_contributors_count(0)


def test_disables_remove_button_when_list_is_empty(driver):
    _ = show_contributors(make_album())
    driver.add_contributor()
    driver.remove_contributor_at(0)
    driver.shows_remove_button(disabled=True)


def test_signals_lyricist(driver):
    track = make_track()
    project = make_album(tracks=[track])

    signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_contributors(project, track, on_metadata_changed=signal.received)

    signal.expect(has_entries(lyricist="Joel Miller"))
    driver.add_lyricist("Joel Miller")
    driver.check(signal)

    signal.expect(has_entries(lyricist=""))
    driver.remove_contributor_at(0)
    driver.check(signal)

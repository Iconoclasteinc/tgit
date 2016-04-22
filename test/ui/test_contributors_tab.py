# -*- coding: utf-8 -*-
from hamcrest import has_entries, contains
import pytest

from cute.probes import KeywordsValueMatcherProbe, MultiValueMatcherProbe
from cute.widgets import window
from test.ui import show_, close_, ignore
from testing.builders import make_album, make_track
from testing.drivers.contributors_tab_driver import ContributorsTabDriver
from tgit.ui import make_contributors_tab
from tgit.ui.pages.contributors_tab import ContributorsTab

pytestmark = pytest.mark.ui


def show_page(project=make_album(), track=make_track(), on_metadata_changed=ignore, on_isni_local_lookup=ignore,
              on_ipi_local_lookup=ignore, on_ipi_changed=ignore):
    page = make_contributors_tab(project, track,
                                 on_metadata_changed=on_metadata_changed,
                                 on_isni_local_lookup=on_isni_local_lookup,
                                 on_ipi_local_lookup=on_ipi_local_lookup,
                                 on_ipi_changed=on_ipi_changed)
    show_(page)
    return page


@pytest.yield_fixture()
def driver(prober, automaton):
    tab_driver = ContributorsTabDriver(window(ContributorsTab), prober, automaton)
    yield tab_driver
    close_(tab_driver)


def test_displays_column_headings(driver):
    _ = show_page(make_album())
    driver.shows_column_headers("Name", "Role", "IPI", "ISNI")
    driver.has_contributors_count(0)


def test_adds_empty_row_to_table_when_clicking_on_add_button(driver):
    _ = show_page(make_album())
    driver.add_contributor()
    driver.has_contributors_count(1)
    driver.has_added_empty_row()
    # Need to remove the contributor row otherwise following tests will fail...
    driver.remove_contributor_at(0)


def test_removes_row(driver):
    _ = show_page(make_album())
    driver.add_contributor()
    driver.remove_contributor_at(0)
    driver.has_contributors_count(0)


def test_disables_remove_button_when_list_is_empty(driver):
    _ = show_page(make_album())
    driver.add_contributor()
    driver.remove_contributor_at(0)
    driver.shows_remove_button(disabled=True)


def test_signals_lyricist(driver):
    track = make_track()
    project = make_album(tracks=[track])

    signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(project, track, on_metadata_changed=signal.received)

    signal.expect(has_entries(lyricist="Joel Miller"))
    driver.add_lyricist("Joel Miller")
    driver.check(signal)

    signal.expect(has_entries(lyricist=""))
    driver.remove_contributor_at(0)
    driver.check(signal)


def test_updates_isni_when_name_changes(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    track = make_track()
    album = make_album(tracks=[track])

    _ = show_page(album, track, on_isni_local_lookup=lookup)

    driver.add_lyricist("Joel Miller")
    driver.shows_isni_at_row("0000000123456789", row=0)
    driver.change_name_at_row("Rebecca Ann Maloy", row=0)
    driver.shows_isni_at_row("", row=0)
    # Need to remove the contributor row otherwise following tests will fail...
    driver.remove_contributor_at(0)


def test_updates_ipi_when_name_changes(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    track = make_track()
    album = make_album(tracks=[track])

    _ = show_page(album, track, on_ipi_local_lookup=lookup)

    driver.add_lyricist("Joel Miller")
    driver.shows_ipi_at_row("0000000123456789", row=0)
    driver.change_name_at_row("Rebecca Ann Maloy", row=0)
    driver.shows_ipi_at_row("", row=0)
    # Need to remove the contributor row otherwise following tests will fail...
    driver.remove_contributor_at(0)


def test_signals_on_lyricist_ipi_changed(driver):
    signal = MultiValueMatcherProbe("ipi changed", contains("Joel Miller", "0000000123456789"))

    track = make_track()
    album = make_album(tracks=[track])
    _ = show_page(album, track, on_ipi_changed=signal.received)

    driver.add_lyricist("Joel Miller")
    driver.change_ipi_at_row("0000000123456789", row=0)
    driver.check(signal)
    # Need to remove the contributor row otherwise following tests will fail...
    driver.remove_contributor_at(0)

# -*- coding: utf-8 -*-
from hamcrest import has_entries, has_items
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
    project.add_track(track)
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
    close_(tab_driver, pause=30)


def test_displays_column_headings(driver):
    _ = show_page()
    driver.shows_column_headers("Name", "Role", "IPI", "ISNI")
    driver.has_contributors_count(0)


def test_displays_collaborators(driver):
    def isni_lookup(text):
        return isnis.get(text)

    def ipi_lookup(text):
        return ipis.get(text)

    isnis = {"Joel Miller": "000000123456789", "John Roney": "9876543210000000", "Rebecca Maloy": "0102030405060789"}
    ipis = {"Joel Miller": "0102030405060789", "John Roney": "000000123456789", "Rebecca Maloy": "9876543210000000"}

    track = make_track(lyricist=["Joel Miller"], composer=["John Roney"], publisher=["Rebecca Maloy"])
    album = make_album(isnis=isnis, ipis=ipis)

    _ = show_page(album, track, on_isni_local_lookup=isni_lookup, on_ipi_local_lookup=ipi_lookup)
    driver.shows_row_details("Joel Miller", "0102030405060789", "000000123456789")
    driver.shows_role_on_row(0, "Author")
    driver.shows_row_details("John Roney", "000000123456789", "9876543210000000")
    driver.shows_role_on_row(1, "Composer")
    driver.shows_row_details("Rebecca Maloy", "9876543210000000", "0102030405060789")
    driver.shows_role_on_row(2, "Publisher")
    driver.has_contributors_count(3)


def test_updates_collaborators_identifiers(driver):
    def isni_lookup(text):
        return isnis.get(text)

    def ipi_lookup(text):
        return ipis.get(text)

    isnis = {"Joel Miller": "000000123456789", "John Roney": "9876543210000000", "Rebecca Maloy": "0102030405060789"}
    ipis = {"Joel Miller": "0102030405060789", "John Roney": "000000123456789", "Rebecca Maloy": "9876543210000000"}

    track = make_track(lyricist=["Joel Miller"], composer=["John Roney"], publisher=["Rebecca Maloy"])
    album = make_album(isnis=isnis, ipis=ipis)

    _ = show_page(album, track, on_isni_local_lookup=isni_lookup, on_ipi_local_lookup=ipi_lookup)
    isnis["Joel Miller"] = "0000001234567891"
    isnis["John Roney"] = "98765432100000001"
    isnis["Rebecca Maloy"] = "01020304050607891"
    ipis["Joel Miller"] = "01020304050607891"
    ipis["John Roney"] = "0000001234567891"
    ipis["Rebecca Maloy"] = "98765432100000001"
    album.metadataChanged()

    driver.shows_row_details("Joel Miller", "01020304050607891", "0000001234567891")
    driver.shows_role_on_row(0, "Author")
    driver.shows_row_details("John Roney", "0000001234567891", "98765432100000001")
    driver.shows_role_on_row(1, "Composer")
    driver.shows_row_details("Rebecca Maloy", "98765432100000001", "01020304050607891")
    driver.shows_role_on_row(2, "Publisher")
    driver.has_contributors_count(3)


def test_adds_empty_row_to_table_when_clicking_on_add_button(driver):
    _ = show_page()
    driver.add_contributor()
    driver.has_contributors_count(1)
    driver.has_added_empty_row()


def test_removes_row(driver):
    _ = show_page()
    driver.add_contributor()
    driver.remove_contributor_at(0)
    driver.has_contributors_count(0)


def test_disables_remove_button_when_list_is_empty(driver):
    _ = show_page()
    driver.add_contributor()
    driver.remove_contributor_at(0)
    driver.shows_remove_button(disabled=True)


def test_signals_collaborator(driver):
    signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(on_metadata_changed=signal.received)

    signal.expect(has_entries(lyricist=["Joel Miller"]))
    driver.add_lyricist("Joel Miller")
    driver.check(signal)

    signal.expect(has_entries(lyricist=[]))
    driver.remove_contributor_at(0)
    driver.check(signal)

    signal.expect(has_entries(composer=["Joel Miller"]))
    driver.add_composer("Joel Miller")
    driver.check(signal)

    signal.expect(has_entries(composer=[]))
    driver.remove_contributor_at(0)
    driver.check(signal)

    signal.expect(has_entries(publisher=["Joel Miller"]))
    driver.add_publisher("Joel Miller")
    driver.check(signal)

    signal.expect(has_entries(publisher=[]))
    driver.remove_contributor_at(0)
    driver.check(signal)


def test_signals_multiple_collaborator(driver):
    signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(on_metadata_changed=signal.received)

    signal.expect(has_entries(lyricist=["Joel Miller", "John Roney"]))
    driver.add_lyricist("Joel Miller")
    driver.add_lyricist("John Roney")
    driver.check(signal)

    signal.expect(has_entries(composer=["John Lennon", "Paul McCartney"]))
    driver.add_composer("John Lennon")
    driver.add_composer("Paul McCartney")
    driver.check(signal)

    signal.expect(has_entries(publisher=["David Murphy et cie", "Ad Litteram"]))
    driver.add_publisher("David Murphy et cie")
    driver.add_publisher("Ad Litteram")
    driver.check(signal)


def test_updates_isni_when_name_changes(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    _ = show_page(on_isni_local_lookup=lookup)

    driver.add_lyricist("Joel Miller")
    driver.shows_isni_at_row("0000000123456789", row=0)
    driver.change_name_at_row("Rebecca Ann Maloy", row=0)
    driver.shows_isni_at_row("", row=0)


def test_updates_ipi_when_name_changes(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    _ = show_page(on_ipi_local_lookup=lookup)

    driver.add_lyricist("Joel Miller")
    driver.shows_ipi_at_row("0000000123456789", row=0)
    driver.change_name_at_row("Rebecca Ann Maloy", row=0)
    driver.shows_ipi_at_row("", row=0)


def test_signals_on_lyricist_ipi_changed(driver):
    signal = MultiValueMatcherProbe("ipi changed", has_items("Joel Miller", "0000000123456789"))

    _ = show_page(on_ipi_changed=signal.received)

    driver.add_lyricist("Joel Miller")
    driver.change_ipi_at_row("0000000123456789", row=0)
    driver.check(signal)

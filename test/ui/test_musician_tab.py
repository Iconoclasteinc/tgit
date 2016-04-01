import pytest
from hamcrest import has_entries

from cute.probes import KeywordsValueMatcherProbe
from cute.widgets import window
from test.drivers.musician_tab_driver import MusicianTabDriver
from test.ui import ignore, show_, close_
from test.util.builders import make_album
from tgit.ui import make_musician_tab
from tgit.ui.pages.musician_tab import MusicianTab

pytestmark = pytest.mark.ui


@pytest.yield_fixture()
def driver(prober, automaton):
    page_driver = MusicianTabDriver(window(MusicianTab), prober, automaton)
    yield page_driver
    close_(page_driver)


def show_page(project=make_album(), on_metadata_changed=ignore):
    tab = make_musician_tab(project, on_metadata_changed=on_metadata_changed)
    show_(tab)
    return tab


def test_shows_musicians(driver):
    _ = show_page(project=make_album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]))

    driver.shows_only_musicians_in_table(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant"))


def test_removes_musicians(driver):
    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(project=make_album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]),
                  on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(guest_performers=[("Vocals", "Robert Plant")]))
    driver.remove_musician(row=1)
    driver.shows_only_musicians_in_table(("Vocals", "Robert Plant"))
    driver.check(metadata_changed_signal)


def test_adds_musicians(driver):
    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(guest_performers=[("Guitar", "Jimmy Page")]))
    driver.add_musician(instrument="Guitar", name="Jimmy Page", row=1)
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]))
    driver.add_musician(instrument="Vocals", name="Robert Plant", row=2)
    driver.check(metadata_changed_signal)


def test_displays_musician_table_only_once(driver):
    project = make_album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")])
    page = show_page(project=project)
    page.display(project)

    driver.shows_only_musicians_in_table(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant"))

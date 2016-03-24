# -*- coding: utf-8 -*-
import timeit

import pytest
from PyQt5.QtCore import QByteArray
from hamcrest import has_entries, assert_that, less_than, contains

from cute.matchers import named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe, KeywordsValueMatcherProbe
from cute.widgets import window
from test.drivers import ProjectEditionPageDriver
from test.ui import ignore, show_, close_
from test.util import resources, builders as build
from test.util.builders import make_album, make_anonymous_session, make_registered_session
from tgit import fs
from tgit.auth import Permission
from tgit.identity import IdentityCard, IdentityLookup
from tgit.metadata import Image
from tgit.ui.pages.project_edition_page import make_project_edition_page, ProjectEditionPage
from tgit.ui.pages.track_list_tab import TrackListTab

pytestmark = pytest.mark.ui


@pytest.yield_fixture()
def driver(prober, automaton):
    page_driver = ProjectEditionPageDriver(window(ProjectEditionPage, named("project_edition_page")), prober, automaton)
    yield page_driver
    close_(page_driver)


def create_track_list_tab(_):
    return TrackListTab(ignore)


def show_page(album, session=make_anonymous_session(), identity_lookup=IdentityLookup(),
              on_select_artwork=ignore, on_select_identity=ignore, **handlers):
    page = make_project_edition_page(album, session, identity_lookup,
                                     track_list_tab=create_track_list_tab,
                                     on_select_artwork=on_select_artwork,
                                     on_select_identity=on_select_identity,
                                     **handlers)
    show_(page)
    return page


def test_displays_invalid_image_placeholder_when_project_has_corrupted_picture(driver):
    _ = show_page(make_album(images=[build.image("image/jpeg", QByteArray(), Image.FRONT_COVER)]))
    driver.shows_picture_placeholder()


def test_displays_no_image_placeholder_when_project_has_no_cover(driver):
    _ = show_page(make_album())
    driver.shows_picture_placeholder()


def test_displays_main_project_cover_when_existing(driver):
    _ = show_page(make_album(
        images=[build.image("image/jpeg", _load_test_image("front-cover.jpg"), Image.FRONT_COVER)]))
    driver.shows_picture()


def test_displays_project_metadata(driver):
    _ = show_page(make_album(
        release_name="Album",
        lead_performer="Artist",
        lead_performer_region=("CA",),
        isnis={"Artist": "0000000123456789"},
        guest_performers=[("Guitar", "Guitarist"), ("Piano", "Pianist")],
        label_name="Label",
        catalog_number="XXX123456789",
        upc="123456789999",
        release_time="2009-01-01"), make_registered_session())

    driver.shows_title("Album")
    driver.shows_compilation(False)
    driver.shows_main_artist("Artist")
    driver.shows_main_artist_region("Canada")
    driver.shows_main_artist_isni("0000000123456789")
    driver.shows_label_name("Label")
    driver.shows_catalog_number("XXX123456789")
    driver.shows_upc("123456789999")
    driver.shows_release_time("2009-01-01")


def test_indicates_whether_project_is_a_compilation(driver):
    album = make_album(compilation=False)
    _ = show_page(album)
    driver.shows_compilation(False)

    album.compilation = True
    driver.shows_compilation(True)


def test_disables_main_artist_section_when_project_is_a_compilation(driver):
    _ = show_page(make_album(compilation=True))
    driver.shows_main_artist("Various Artists", disabled=True)
    driver.shows_main_artist_region("", disabled=True)
    driver.shows_main_artist_isni("", disabled=True)
    driver.shows_main_artist_isni_lookup_button(disabled=True)


def test_enables_main_artist_section_when_project_is_no_longer_a_compilation(driver):
    album = make_album(compilation=False)
    _ = show_page(album, make_registered_session())
    driver.shows_main_artist("", disabled=False)
    driver.shows_main_artist_region("", disabled=False)
    driver.shows_main_artist_isni("", disabled=False)
    driver.shows_main_artist_isni_lookup_button(disabled=True)


def test_disables_isni_lookup_when_main_artist_is_empty(driver):
    _ = show_page(make_album(), make_registered_session())
    driver.shows_main_artist_isni_lookup_button(disabled=True)


def test_enables_isni_lookup_when_user_logs_in(driver):
    session = make_anonymous_session()
    _ = show_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.shows_main_artist_isni_lookup_button(disabled=True)

    session.login_as("somebody@gmail.com", "api-key", [Permission.lookup_isni.value])
    driver.shows_main_artist_isni_lookup_button(disabled=False)


def test_disables_isni_lookup_when_user_logs_out(driver):
    session = make_registered_session()
    _ = show_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.shows_main_artist_isni_lookup_button(disabled=False)

    session.logout()
    driver.shows_main_artist_isni_lookup_button(disabled=True)


def test_disables_isni_lookup_when_main_artist_is_blank(driver):
    _ = show_page(make_album(lead_performer="     "))
    driver.shows_main_artist_isni_lookup_button(disabled=True)


def test_signals_when_artwork_selected(driver):
    album = make_album()
    signal = ValueMatcherProbe("select artwork")
    _ = show_page(album, on_select_artwork=lambda: signal.received())

    driver.add_artwork()
    driver.check(signal)


def test_efficiently_displays_image_cover_when_it_does_not_change(driver):
    album = make_album(images=[build.image("image/jpeg", _load_test_image("big-image.jpg"), Image.FRONT_COVER)])
    page = show_page(album)

    time = timeit.timeit(lambda: page.display(album), number=50)
    assert_that(time, less_than(1), "time to execute render 50 times")


def test_signals_when_remove_artwork_button_clicked(driver):
    signal = ValueMatcherProbe("remove artwork")
    _ = show_page(make_album(), on_remove_artwork=signal.received)

    driver.remove_artwork()
    driver.check(signal)


def test_updates_isni_when_main_artist_text_change(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    _ = show_page(make_album(), make_registered_session(), on_isni_local_lookup=lookup)

    driver.change_main_artist("Joel Miller")
    driver.shows_main_artist_isni("0000000123456789")


def test_clears_isni_when_main_artist_not_found(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    album = make_album(lead_performer="Joel Miller", isnis={"Joel Miller": "00000000123456789"})
    _ = show_page(album, make_registered_session(), on_isni_local_lookup=lookup)

    driver.change_main_artist("Rebecca Ann Maloy")
    driver.shows_main_artist_isni("")


def test_selects_identities_on_isni_lookup(driver):
    select_identity_signal = ValueMatcherProbe("select identity", "performer")

    _ = show_page(make_album(lead_performer="performer"), make_registered_session(),
                  on_select_identity=select_identity_signal.received)

    driver.lookup_isni_of_main_artist()
    driver.check(select_identity_signal)


def test_updates_main_artist_isni_on_isni_lookup(driver):
    identity_lookup = IdentityLookup()
    _ = show_page(make_album(lead_performer="performer"), make_registered_session(), identity_lookup)

    identity_lookup.identity_selected(IdentityCard(id="0000000123456789", type="individual"))
    driver.shows_main_artist_isni("0000000123456789")


def test_signals_found_isni_on_isni_lookup(driver):
    isni_changed_signal = MultiValueMatcherProbe("isni changed", contains("Joel Miller", "0000000123456789"))
    identity_lookup = IdentityLookup()
    _ = show_page(make_album(lead_performer="Joel Miller"), make_registered_session(), identity_lookup,
                  on_isni_changed=isni_changed_signal.received)

    identity_lookup.identity_selected(IdentityCard(id="0000000123456789", type="individual"))
    driver.confirm_isni()
    driver.check(isni_changed_signal)


def test_signals_when_project_metadata_edited(driver):
    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(make_album(), on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(release_name="Title"))
    driver.change_title("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(compilation=True))
    driver.toggle_compilation()
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(compilation=False))
    driver.toggle_compilation()
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer="Joel Miller"))
    driver.change_main_artist("Joel Miller")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer_region=("CA",)))
    driver.change_main_artist_region("Canada")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer_region=None))
    driver.change_main_artist_region("")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(label_name="Label"))
    driver.change_label_name("Label")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(catalog_number="XXX12345678"))
    driver.change_catalog_number("XXX12345678")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(upc="123456789999"))
    driver.change_upc("123456789999")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(release_time="2009-01-01"))
    driver.change_release_time(2009, 1, 1)
    driver.check(metadata_changed_signal)


def test_shows_musicians(driver):
    _ = show_page(album=make_album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]))

    driver.shows_only_musicians_in_table(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant"))


def test_removes_musicians(driver):
    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(album=make_album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]),
                  on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(guest_performers=[("Vocals", "Robert Plant")]))
    driver.remove_musician(row=1)
    driver.shows_only_musicians_in_table(("Vocals", "Robert Plant"))
    driver.check(metadata_changed_signal)


def test_adds_musicians(driver):
    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(album=make_album(), on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(guest_performers=[("Guitar", "Jimmy Page")]))
    driver.add_musician(instrument="Guitar", name="Jimmy Page", row=1)
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")]))
    driver.add_musician(instrument="Vocals", name="Robert Plant", row=2)
    driver.check(metadata_changed_signal)


def test_displays_musician_table_only_once(driver):
    album = make_album(guest_performers=[("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant")])
    page = show_page(album=album)
    page.display(album)

    driver.shows_only_musicians_in_table(("Guitar", "Jimmy Page"), ("Vocals", "Robert Plant"))


def _load_test_image(name):
    return fs.read(resources.path(name))
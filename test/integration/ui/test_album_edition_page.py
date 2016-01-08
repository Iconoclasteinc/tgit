# -*- coding: utf-8 -*-
import timeit
import types

import pytest
from PyQt5.QtCore import QByteArray
from hamcrest import has_entries, assert_that, less_than, instance_of, contains, equal_to
import requests

from cute.matchers import named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe, KeywordsValueMatcherProbe
from cute.widgets import window
from test.drivers import AlbumEditionPageDriver
from test.integration.ui import show_widget
from test.util import resources, builders as build
from test.util.builders import make_album, make_anonymous_session, make_registered_session
from tgit.auth import Permission
from tgit.authentication_error import AuthenticationError
from tgit.identity import IdentityCard
from tgit.insufficient_information_error import InsufficientInformationError
from tgit.metadata import Image
from tgit.ui.pages.album_edition_page import make_album_edition_page, AlbumEditionPage
from tgit import fs


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = AlbumEditionPageDriver(window(AlbumEditionPage, named("album_edition_page")), prober, automaton)
    yield page_driver
    page_driver.close()


ignore = lambda *_, **__: None


def raise_(e):
    raise e


def show_page(album, session=make_anonymous_session(),
              select_picture=ignore,
              select_identity=ignore,
              review_assignation=ignore,
              edit_performers=ignore,
              show_isni_assignation_failed=ignore,
              show_cheddar_connection_failed=ignore,
              show_cheddar_authentication_failed=ignore,
              **handlers):
    page = make_album_edition_page(album, session,
                                   edit_performers=edit_performers,
                                   select_picture=select_picture,
                                   select_identity=select_identity,
                                   show_isni_assignation_failed=show_isni_assignation_failed,
                                   show_cheddar_connection_failed=show_cheddar_connection_failed,
                                   show_cheddar_authentication_failed=show_cheddar_authentication_failed,
                                   review_assignation=review_assignation,
                                   **handlers)
    show_widget(page)
    return page


def test_displays_invalid_image_placeholder_when_album_has_corrupted_picture(driver):
    _ = show_page(make_album(images=[build.image("image/jpeg", QByteArray(), Image.FRONT_COVER)]))
    driver.shows_picture_placeholder()


def test_displays_no_image_placeholder_when_album_has_no_cover(driver):
    _ = show_page(make_album())
    driver.shows_picture_placeholder()


def test_displays_main_album_cover_when_existing(driver):
    _ = show_page(make_album(
        images=[build.image("image/jpeg", load_test_image("front-cover.jpg"), Image.FRONT_COVER)]))
    driver.shows_picture()


def test_displays_album_metadata(driver):
    _ = show_page(make_album(
        release_name="Album",
        lead_performer="Artist",
        lead_performer_region=("CA",),
        isnis={"Artist": "0000000123456789"},
        guest_performers=[("Guitar", "Guitarist"), ("Piano", "Pianist")],
        label_name="Label",
        catalog_number="XXX123456789",
        upc="123456789999",
        recording_time="2008-09-15",
        release_time="2009-01-01",
        comments="Comments\n..."))

    driver.shows_release_name("Album")
    driver.shows_compilation(False)
    driver.shows_lead_performer("Artist")
    driver.shows_lead_performer_region("Canada")
    driver.shows_isni("0000000123456789")
    driver.shows_guest_performers("Guitar: Guitarist; Piano: Pianist")
    driver.shows_label_name("Label")
    driver.shows_catalog_number("XXX123456789")
    driver.shows_upc("123456789999")
    driver.shows_recording_time("2008-09-15")
    driver.shows_release_time("2009-01-01")
    driver.shows_digital_release_time("2000-01-01")
    driver.shows_comments("Comments\n...")
    driver.shows_media_type("")
    # self.driver.shows_release_type("")


def test_indicates_whether_album_is_a_compilation(driver):
    album = make_album(compilation=False)
    _ = show_page(album)
    driver.shows_compilation(False)

    album.compilation = True
    driver.shows_compilation(True)


def test_disables_lead_performer_edition_when_album_is_a_compilation(driver):
    _ = show_page(make_album(compilation=True, lead_performer="Album Artist"))
    driver.shows_lead_performer("Various Artists", disabled=True)


def test_enables_isni_lookup_when_album_is_no_longer_a_compilation(driver):
    album = make_album(compilation=True, lead_performer="Album Artist")
    _ = show_page(album, make_registered_session())
    driver.enables_isni_lookup(False)

    album.compilation = False
    driver.enables_isni_lookup()


def test_disables_isni_lookup_when_lead_performer_is_empty(driver):
    _ = show_page(make_album(), make_registered_session())
    driver.enables_isni_lookup(False)


def test_enables_isni_lookup_when_user_logs_in(driver):
    session = make_anonymous_session()
    _ = show_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.enables_isni_lookup(False)

    session.login_as("somebody@gmail.com", "api-key", [Permission.lookup_isni.value])
    driver.enables_isni_lookup(True)


def test_disables_isni_lookup_when_user_logs_out(driver):
    session = make_registered_session()
    _ = show_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.enables_isni_lookup(True)

    session.logout()
    driver.enables_isni_lookup(False)


# noinspection PyUnresolvedReferences
@pytest.mark.xfail
def test_displays_tooltip_on_isni_lookup_when_anonymously_connected(driver):
    _ = show_page(session=(make_anonymous_session()), album=make_album(lead_performer="Album Artist"))
    driver.isni_lookup_has_tooltip("Please sign-in to activate ISNI lookup")


# noinspection PyUnresolvedReferences
@pytest.mark.xfail
def test_removes_tooltip_on_isni_lookup_when_signed_in(driver):
    _ = show_page(session=(make_registered_session()), album=make_album(lead_performer="Album Artist"))
    driver.isni_lookup_has_tooltip("")


def test_disables_isni_lookup_when_lead_performer_is_blank(driver):
    _ = show_page(make_album(lead_performer="     "))
    driver.enables_isni_lookup(False)


def test_disables_isni_assign_by_default(driver):
    _ = show_page(make_album(lead_performer="     "))
    driver.disables_isni_assign()


def test_signals_when_picture_selected(driver):
    album = make_album()
    signal = ValueMatcherProbe("select picture", "front-cover.jpg")
    _ = show_page(album,
                  select_picture=lambda callback: callback("front-cover.jpg"),
                  on_select_picture=signal.received)

    driver.add_picture()
    driver.check(signal)


def test_updates_guest_performers_with_edition_dialog_return_value(driver):
    _ = show_page(make_album(), edit_performers=lambda callback: callback(
        [("instrument1", "performer1"), ("instrument2", "performer2")]))
    driver.edit_performers()
    driver.shows_guest_performers("instrument1: performer1; instrument2: performer2")


def test_efficiently_displays_image_cover_when_it_does_not_change(driver):
    album = make_album(images=[build.image("image/jpeg", load_test_image("big-image.jpg"), Image.FRONT_COVER)])
    page = show_page(album)

    time = timeit.timeit(lambda: page.display(album), number=50)
    assert_that(time, less_than(1), "time to execute render 50 times")


def test_signals_when_remove_picture_button_clicked(driver):
    remove_picture_signal = ValueMatcherProbe("remove picture")
    _ = show_page(make_album(), on_remove_picture=remove_picture_signal.received)

    driver.remove_picture()
    driver.check(remove_picture_signal)


def test_updates_isni_when_lead_performer_text_change(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    _ = show_page(make_album(), on_isni_local_lookup=lookup)

    driver.change_lead_performer("Joel Miller")
    driver.shows_isni("0000000123456789")


def test_clears_isni_when_lead_performer_not_found(driver):
    def lookup(text):
        return "0000000123456789" if text == "Joel Miller" else None

    album = make_album(lead_performer="Joel Miller", isnis={"Joel Miller": "00000000123456789"})
    _ = show_page(album, on_isni_local_lookup=lookup)

    driver.change_lead_performer("Rebecca Ann Maloy")
    driver.shows_isni("")


def test_signals_when_lookup_isni_action_is_triggered(driver):
    lookup_isni_signal = MultiValueMatcherProbe("lookup ISNI", contains("performer", instance_of(types.FunctionType)))
    _ = show_page(make_album(lead_performer="performer"), make_registered_session(),
                  on_isni_lookup=lookup_isni_signal.received)

    driver.lookup_isni_of_lead_performer()
    driver.check(lookup_isni_signal)


def test_shows_connection_failed_error_on_isni_lookup(driver):
    show_error_signal = ValueMatcherProbe("ISNI lookup exception")

    _ = show_page(make_album(lead_performer="performer"), make_registered_session(),
                  show_cheddar_connection_failed=show_error_signal.received,
                  on_isni_lookup=lambda *_: raise_(requests.ConnectionError()))

    driver.lookup_isni_of_lead_performer()
    driver.check(show_error_signal)


def test_shows_authentication_failed_error_on_isni_lookup(driver):
    show_error_signal = ValueMatcherProbe("ISNI authentication")

    _ = show_page(make_album(lead_performer="performer"), make_registered_session(),
                  show_cheddar_authentication_failed=show_error_signal.received,
                  on_isni_lookup=lambda *_: raise_(AuthenticationError()))

    driver.lookup_isni_of_lead_performer()
    driver.check(show_error_signal)


def test_selects_identities_on_isni_lookup(driver):
    select_identity_signal = MultiValueMatcherProbe("select identity",
                                                    contains("identities", instance_of(types.FunctionType)))

    _ = show_page(make_album(lead_performer="performer"), make_registered_session(),
                  select_identity=select_identity_signal.received,
                  on_isni_lookup=lambda _, callback: callback("identities"))

    driver.lookup_isni_of_lead_performer()
    driver.check(select_identity_signal)


def test_updates_lead_performer_isni_on_isni_lookup(driver):
    _ = show_page(make_album(lead_performer="performer"), make_registered_session(),
                  select_identity=lambda _, callback: callback(
                      IdentityCard(id="0000000123456789", type=IdentityCard.INDIVIDUAL)),
                  on_isni_lookup=lambda _, callback: callback("identities"))

    driver.lookup_isni_of_lead_performer()
    driver.shows_isni("0000000123456789")


def test_signals_found_isni_on_isni_lookup(driver):
    isni_changed_signal = MultiValueMatcherProbe("isni changed", contains("Joel Miller", "0000000123456789"))
    _ = show_page(make_album(lead_performer="Joel Miller"), make_registered_session(),
                  on_isni_changed=isni_changed_signal.received,
                  select_identity=lambda _, callback: callback(
                      IdentityCard(id="0000000123456789", type=IdentityCard.INDIVIDUAL)),
                  on_isni_lookup=lambda _, callback: callback(""))

    driver.lookup_isni_of_lead_performer()
    driver.confirm_isni()
    driver.check(isni_changed_signal)


def test_signals_when_assign_isni_button_clicked(driver):
    assign_isni_signal = MultiValueMatcherProbe("assign ISNI", contains(
        equal_to("individual"),
        instance_of(types.FunctionType)))

    _ = show_page(make_album(),
                  session=(make_registered_session(permissions=[Permission.assign_isni.value])),
                  review_assignation=lambda on_review: on_review("individual"),
                  on_isni_assign=assign_isni_signal.received)

    driver.change_lead_performer("Joel Miller")
    driver.assign_isni_to_lead_performer()
    driver.check(assign_isni_signal)


def test_shows_connection_failed_error_on_isni_assignation(driver):
    show_error_signal = ValueMatcherProbe("ISNI assignation exception")

    _ = show_page(make_album(),
                  session=(make_registered_session(permissions=[Permission.assign_isni.value])),
                  show_cheddar_connection_failed=show_error_signal.received,
                  review_assignation=lambda on_review: on_review(""),
                  on_isni_assign=lambda *_: raise_(requests.ConnectionError()))

    driver.change_lead_performer("Joel Miller")
    driver.assign_isni_to_lead_performer()
    driver.check(show_error_signal)


def test_shows_assignation_failed_error_on_isni_assignation(driver):
    show_error_signal = ValueMatcherProbe("ISNI assignation exception", "insufficient information")

    _ = show_page(make_album(),
                  session=(make_registered_session(permissions=[Permission.assign_isni.value])),
                  show_isni_assignation_failed=show_error_signal.received,
                  review_assignation=lambda on_review: on_review(""),
                  on_isni_assign=lambda *_: raise_(InsufficientInformationError("insufficient information")))

    driver.change_lead_performer("Joel Miller")
    driver.assign_isni_to_lead_performer()
    driver.check(show_error_signal)


def test_shows_authentication_failed_error_on_isni_assignation(driver):
    show_error_signal = ValueMatcherProbe("ISNI authentication")

    _ = show_page(make_album(),
                  session=(make_registered_session(permissions=[Permission.assign_isni.value])),
                  show_cheddar_authentication_failed=show_error_signal.received,
                  review_assignation=lambda on_review: on_review(""),
                  on_isni_assign=lambda *_: raise_(AuthenticationError()))

    driver.change_lead_performer("Joel Miller")
    driver.assign_isni_to_lead_performer()
    driver.check(show_error_signal)


def test_shows_assigned_isni_on_isni_assignation(driver):
    _ = show_page(make_album(),
                  session=(make_registered_session(permissions=[Permission.assign_isni.value])),
                  review_assignation=lambda on_review: on_review(""),
                  on_isni_assign=lambda _, callback: callback(
                      IdentityCard(id="0000000123456789", type=IdentityCard.INDIVIDUAL)))

    driver.change_lead_performer("Joel Miller")
    driver.assign_isni_to_lead_performer()
    driver.shows_isni("0000000123456789")


def test_signals_assigned_isni_on_isni_assignation(driver):
    isni_changed_signal = MultiValueMatcherProbe("isni changed", contains("Joel Miller", "0000000123456789"))

    _ = show_page(make_album(),
                  session=(make_registered_session(permissions=[Permission.assign_isni.value])),
                  on_isni_changed=isni_changed_signal.received,
                  review_assignation=lambda on_review: on_review(""),
                  on_isni_assign=lambda _, callback: callback(
                      IdentityCard(id="0000000123456789", type=IdentityCard.INDIVIDUAL)))

    driver.change_lead_performer("Joel Miller")
    driver.assign_isni_to_lead_performer()
    driver.confirm_isni()
    driver.check(isni_changed_signal)


def test_signals_when_album_metadata_edited(driver):
    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(make_album(), on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(release_name="Title"))
    driver.change_release_name("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(compilation=True))
    driver.toggle_compilation()
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(compilation=False))
    driver.toggle_compilation()
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer="Joel Miller"))
    driver.change_lead_performer("Joel Miller")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer_region=("CA",)))
    driver.change_lead_performer_region("Canada")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer_region=None))
    driver.change_lead_performer_region("")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(
        guest_performers=[("Guitar", "Guitarist"), ("Guitar", "Bassist"), ("Piano", "Pianist")]))
    driver.change_guest_performers("Guitar: Guitarist; Guitar: Bassist; Piano: Pianist")
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

    metadata_changed_signal.expect(has_entries(comments="Comments\n...\n"))
    driver.add_comments("Comments")
    driver.add_comments("...")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(release_time="2009-01-01"))
    driver.change_release_time(2009, 1, 1)
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_time="2008-09-15"))
    driver.change_recording_time(2008, 9, 15)
    driver.check(metadata_changed_signal)


def load_test_image(name):
    return fs.read(resources.path(name))

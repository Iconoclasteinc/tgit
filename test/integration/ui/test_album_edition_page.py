# -*- coding: utf-8 -*-
import timeit
import types

from PyQt5.QtCore import QByteArray

from hamcrest import has_entries, assert_that, less_than, instance_of, contains
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe, MultiValueMatcherProbe
from cute.widgets import window
from test.drivers import AlbumEditionPageDriver
from test.integration.ui import show_widget
from test.util import resources, builders as build
from test.util.builders import make_album, make_anonymous_session, make_registered_session
from tgit.metadata import Image
from tgit.ui.album_edition_page import make_album_edition_page, AlbumEditionPage
from tgit.util import fs


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = AlbumEditionPageDriver(window(AlbumEditionPage, named("album_edition_page")), prober, automaton)
    yield page_driver
    page_driver.close()


ignore = lambda *_, **__: None


def show_track_page(album, session=make_anonymous_session(), select_picture=ignore, select_identity=ignore,
                    edit_performers=ignore, **handlers):
    page = make_album_edition_page(album, session, edit_performers, select_picture, select_identity, **handlers)
    show_widget(page)
    return page


def test_displays_invalid_image_placeholder_when_album_has_corrupted_picture(driver):
    _ = show_track_page(build.album(images=[build.image("image/jpeg", QByteArray(), Image.FRONT_COVER)]))
    driver.shows_picture_placeholder()


def test_displays_no_image_placeholder_when_album_has_no_cover(driver):
    _ = show_track_page(build.album())
    driver.shows_picture_placeholder()


def test_displays_main_album_cover_when_existing(driver):
    _ = show_track_page(build.album(
        images=[build.image("image/jpeg", load_test_image("front-cover.jpg"), Image.FRONT_COVER)]))
    driver.showsPicture()


def test_displays_album_metadata(driver):
    _ = show_track_page(build.album(
        release_name="Album",
        lead_performer="Artist",
        isni="123456789",
        guest_performers=[("Guitar", "Guitarist"), ("Piano", "Pianist")],
        label_name="Label",
        catalog_number="XXX123456789",
        upc="123456789999",
        recording_time="2008-09-15",
        release_time="2009-01-01",
        recording_studios="Studio A, Studio B",
        producer="Artistic Producer",
        mixer="Mixing Engineer",
        comments="Comments\n...",
        primary_style="Style"))

    driver.showsReleaseName("Album")
    driver.shows_compilation(False)
    driver.shows_lead_performer("Artist")
    driver.shows_isni("123456789", True)
    driver.showsArea("")
    driver.shows_guest_performers("Guitar: Guitarist; Piano: Pianist")
    driver.showsLabelName("Label")
    driver.showsCatalogNumber("XXX123456789")
    driver.showsUpc("123456789999")
    driver.shows_recording_time("2008-09-15")
    driver.showsReleaseTime("2009-01-01")
    driver.showsDigitalReleaseTime("2000-01-01")
    driver.showsRecordingStudios("Studio A, Studio B")
    driver.showsProducer("Artistic Producer")
    driver.showsMixer("Mixing Engineer")
    driver.showsComments("Comments\n...")
    driver.shows_primary_style("Style")
    driver.showsMediaType("")
    # self.driver.showsReleaseType("")


def test_indicates_whether_album_is_a_compilation(driver):
    album = build.album(compilation=False)
    _ = show_track_page(album)
    driver.shows_compilation(False)

    album.compilation = True
    driver.shows_compilation(True)


def test_disables_lead_performer_edition_when_album_is_a_compilation(driver):
    _ = show_track_page(build.album(compilation=True, lead_performer="Album Artist"))
    driver.shows_lead_performer("Various Artists", disabled=True)


def test_enables_isni_lookup_when_album_is_no_longer_a_compilation(driver):
    album = make_album(compilation=True, lead_performer="Album Artist")
    _ = show_track_page(album, make_registered_session())
    driver.enables_isni_lookup(False)

    album.compilation = False
    driver.enables_isni_lookup()


def test_disables_isni_lookup_when_lead_performer_is_empty(driver):
    _ = show_track_page(make_album(lead_performer=""), make_registered_session())
    driver.enables_isni_lookup(False)


def test_enables_isni_lookup_when_user_logs_in(driver):
    session = make_anonymous_session()
    _ = show_track_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.enables_isni_lookup(False)

    session.login_as("somebody@mgail.com", "api-key")
    driver.enables_isni_lookup(True)


def test_disables_isni_lookup_when_user_logs_out(driver):
    session = make_registered_session()
    _ = show_track_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.enables_isni_lookup(True)

    session.logout()
    driver.enables_isni_lookup(False)


def test_displays_tooltip_on_isni_lookup_when_anonymously_connected(driver):
    session = make_anonymous_session()
    _ = show_track_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.isni_lookup_has_tooltip("Please sign-in to activate ISNI lookup")


def test_removes_tooltip_on_isni_lookup_when_signed_in(driver):
    session = make_registered_session()
    _ = show_track_page(session=session, album=make_album(lead_performer="Album Artist"))
    driver.isni_lookup_has_tooltip("")


def test_disables_isni_lookup_when_lead_performer_is_blank(driver):
    _ = show_track_page(make_album(lead_performer="     "))
    driver.enables_isni_lookup(False)


def test_disables_isni_assign_by_default(driver):
    _ = show_track_page(make_album(lead_performer="     "))
    driver.disables_isni_assign()


def test_signals_when_picture_selected(driver):
    album = build.album()
    signal = ValueMatcherProbe("select picture", "front-cover.jpg")
    _ = show_track_page(album, select_picture=lambda callback: callback("front-cover.jpg"),
                        on_select_picture=signal.received)

    driver.addPicture()
    driver.check(signal)


def test_updates_guest_performers_with_edition_dialog_return_value(driver):
    _ = show_track_page(build.album(), edit_performers=lambda callback: callback(
        [("instrument1", "performer1"), ("instrument2", "performer2")]))
    driver.edit_performers()
    driver.shows_guest_performers("instrument1: performer1; instrument2: performer2")


def test_efficiently_displays_image_cover_when_it_does_not_change(driver):
    album = build.album(images=[build.image("image/jpeg", load_test_image("big-image.jpg"), Image.FRONT_COVER)])
    page = show_track_page(album)

    time = timeit.timeit(lambda: page.display(album), number=50)
    assert_that(time, less_than(1), "time to execute render 50 times")


def test_signals_when_remove_picture_button_clicked(driver):
    remove_picture_signal = ValueMatcherProbe("remove picture")
    _ = show_track_page(build.album(), on_remove_picture=remove_picture_signal.received)

    driver.removePicture()
    driver.check(remove_picture_signal)


def test_signals_when_lookup_isni_button_clicked(driver):
    lookup_isni_signal = MultiValueMatcherProbe("lookup ISNI", contains("performer", instance_of(types.FunctionType)))
    _ = show_track_page(make_album(lead_performer="performer"), make_registered_session(),
                        on_isni_lookup=lookup_isni_signal.received)

    driver.lookup_isni_of_lead_performer()
    driver.check(lookup_isni_signal)


def test_signals_when_clear_isni_button_clicked(driver):
    clear_isni_signal = ValueMatcherProbe("clear ISNI")
    _ = show_track_page(build.album(isni="0000123456789"), on_clear_isni=clear_isni_signal.received)

    driver.clear_isni()
    driver.check(clear_isni_signal)


def test_signals_when_assign_isni_button_clicked(driver):
    page = show_track_page(build.album(lead_performer="performer"))

    assign_isni_signal = ValueMatcherProbe("assign ISNI")
    page.assign_isni.connect(assign_isni_signal.received)

    driver.assign_isni_to_lead_performer()
    driver.check(assign_isni_signal)


def test_signals_when_album_metadata_edited(driver):
    metadata_changed_signal = ValueMatcherProbe("metadata changed")
    page = show_track_page(build.album(), on_metadata_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(release_name="Title"))
    driver.changeReleaseName("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(compilation=True))
    driver.toggle_compilation()
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(compilation=False))
    driver.toggle_compilation()
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer="Artist"))
    driver.changeLeadPerformer("Artist")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(
        guest_performers=[("Guitar", "Guitarist"), ("Guitar", "Bassist"), ("Piano", "Pianist")]))
    driver.changeGuestPerformers("Guitar: Guitarist; Guitar: Bassist; Piano: Pianist")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(label_name="Label"))
    driver.changeLabelName("Label")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(catalog_number="XXX12345678"))
    driver.changeCatalogNumber("XXX12345678")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(upc="123456789999"))
    driver.changeUpc("123456789999")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(comments="Comments\n...\n"))
    driver.addComments("Comments")
    driver.addComments("...")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(release_time="2009-01-01"))
    driver.changeReleaseTime(2009, 1, 1)
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_time="2008-09-15"))
    driver.change_recording_time(2008, 9, 15)
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studios="Studios"))
    driver.changeRecordingStudios("Studios")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(producer="Producer"))
    driver.changeProducer("Producer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(mixer="Mixer"))
    driver.changeMixer("Mixer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(primary_style="Jazz"))
    driver.select_primary_style("Jazz")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(primary_style="Custom"))
    driver.changePrimaryStyle("Custom")
    driver.check(metadata_changed_signal)


def load_test_image(name):
    return fs.read(resources.path(name))

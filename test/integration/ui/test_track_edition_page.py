# -*- coding: utf-8 -*-

from datetime import timedelta
import types

import pytest

from hamcrest import has_entries, equal_to, instance_of, assert_that, has_key, is_not
import requests

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import TrackEditionPageDriver
from test.integration.ui import show_widget
from test.util import builders as build
from test.util.builders import make_album
from tgit.authentication_error import AuthenticationError
from tgit.identity import IdentityCard
from tgit.insufficient_information_error import InsufficientInformationError
from tgit.ui.pages.track_edition_page import make_track_edition_page, TrackEditionPage


# noinspection PyUnusedLocal
@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = TrackEditionPageDriver(window(TrackEditionPage, named("track_edition_page")), prober, automaton)
    yield page_driver
    page_driver.close()


ignore = lambda *_, **__: None


def raise_(e):
    raise e


def show_page(album, track, on_track_changed=ignore, review_assignation=ignore,
              show_isni_assignation_failed=ignore, show_cheddar_connection_failed=ignore,
              show_cheddar_authentication_failed=ignore, **handlers):
    page = make_track_edition_page(album, track, on_track_changed, review_assignation, show_isni_assignation_failed,
                                   show_cheddar_connection_failed, show_cheddar_authentication_failed, **handlers)
    show_widget(page)
    return page


def test_displays_album_summary_in_banner(driver):
    track = build.track()
    album = build.album(release_name="Album Title", lead_performer=("Artist",), label_name="Record Label",
                        tracks=[build.track(), track, build.track()])

    _ = show_page(album, track)

    driver.shows_album_title("Album Title")
    driver.shows_album_lead_performer("Artist")
    driver.shows_track_number("2")


def test_indicates_when_album_performed_by_various_artists(driver):
    track = build.track()
    album = build.album(compilation=True, tracks=[track])

    _ = show_page(album, track)

    driver.shows_album_lead_performer("Various Artists")


def test_displays_track_metadata(driver):
    track = build.track(bitrate=192000,
                        duration=timedelta(minutes=4, seconds=35).total_seconds(),
                        lead_performer=("Artist",),
                        track_title="Song",
                        versionInfo="Remix",
                        featuredGuest="Featuring",
                        lyricist=("Lyricist", "0000000123456789"),
                        composer="Composer",
                        publisher="Publisher",
                        isrc="Code",
                        iswc="T-345246800-1",
                        labels="Tag1 Tag2 Tag3",
                        lyrics="Lyrics\n...\n...",
                        language="eng",
                        production_company="Initial Producer",
                        production_company_region=("CA",),
                        recording_studio="Studio A, Studio B",
                        recording_studio_region=("CA",),
                        music_producer="Artistic Producer",
                        mixer="Mixing Engineer",
                        primary_style="Style")
    album = build.album(compilation=True, tracks=[track])

    _ = show_page(album, track)

    driver.shows_track_title("Song")
    driver.shows_lead_performer("Artist")
    driver.shows_version_info("Remix")
    driver.shows_bitrate("192 kbps")
    driver.shows_duration("04:35")
    driver.shows_featured_guest("Featuring")
    driver.shows_lyricist("Lyricist")
    driver.shows_composer("Composer")
    driver.shows_publisher("Publisher")
    driver.shows_lyricist_isni("0000000123456789")
    driver.shows_isrc("Code")
    driver.shows_iswc("T-345246800-1")
    driver.shows_tags("Tag1 Tag2 Tag3")
    driver.shows_lyrics("Lyrics\n...\n...")
    driver.shows_language("eng")
    driver.shows_preview_time("00:00")
    driver.shows_recording_studio("Studio A, Studio B")
    driver.shows_recording_studio_region("Canada")
    driver.shows_production_company("Initial Producer")
    driver.shows_production_company_region("Canada")
    driver.shows_music_producer("Artistic Producer")
    driver.shows_mixer("Mixing Engineer")
    driver.shows_primary_style("Style")


def test_disables_lead_performer_edition_when_album_is_not_a_compilation(driver):
    track = build.track()
    album = build.album(lead_performer=("Album Artist",), compilation=False, tracks=[track])

    _ = show_page(album, track)

    driver.shows_lead_performer("Album Artist", disabled=True)


def test_signals_when_track_metadata_change(driver):
    track = build.track()
    album = build.album(compilation=True, tracks=[track])

    page = show_page(album, track)

    metadata_changed_signal = ValueMatcherProbe("metadata changed")
    page.metadata_changed.connect(metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(track_title="Title"))
    driver.change_track_title("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer=("Artist",)))
    driver.change_lead_performer("Artist")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(versionInfo="Remix"))
    driver.change_version_info("Remix")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(featuredGuest="Featuring"))
    driver.change_featured_guest("Featuring")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lyricist=("Lyricist",)))
    driver.change_lyricist("Lyricist")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lyricist=("Joel Miller", "0000000123456789")))
    driver.change_lyricist("Joel Miller")
    driver.change_lyricist_isni("0000000123456789")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(composer="Composer"))
    driver.change_composer("Composer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(publisher="Publisher"))
    driver.change_publisher("Publisher")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(isrc="ZZZ123456789"))
    driver.change_isrc("ZZZ123456789")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(iswc="T-345246800-1"))
    driver.change_iswc("T-345246800-1")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(labels="Tag1 Tag2 Tag3"))
    driver.change_tags("Tag1 Tag2 Tag3")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lyrics="Lyrics\n...\n"))
    driver.add_lyrics("Lyrics")
    driver.add_lyrics("...")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(language="fra"))
    driver.select_language("fra")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(language="eng"))
    driver.change_language("eng")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(production_company="Producer"))
    driver.change_production_company("Producer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(production_company_region=("CA",)))
    driver.change_production_company_region("Canada")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(production_company_region=None))
    driver.change_production_company_region("")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studio="Studios"))
    driver.change_recording_studio("Studios")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studio_region=("CA",)))
    driver.change_recording_studio_region("Canada")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studio_region=None))
    driver.change_recording_studio_region("")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(music_producer="Producer"))
    driver.change_music_producer("Producer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(mixer="Mixer"))
    driver.change_mixer("Mixer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(primary_style="Jazz"))
    driver.select_primary_style("Jazz")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(primary_style="Custom"))
    driver.change_primary_style("Custom")
    driver.check(metadata_changed_signal)


def test_signals_lead_performer_only_when_album_is_compilation(driver):
    track = build.track()
    album = build.album(compilation=False, tracks=[track])

    page = show_page(album, track)

    metadata_changed_signal = ValueMatcherProbe("metadata changed")
    page.metadata_changed.connect(metadata_changed_signal.received)

    metadata_changed_signal.expect(is_not(has_key("lead_performer")))
    driver.change_track_title("Title")
    driver.check(metadata_changed_signal)


def test_displays_software_notice_in_local_time(driver):
    track = build.track(tagger="TGiT", tagger_version="1.0", tagging_time="2014-03-23 20:33:00 +0000")
    album = build.album(tracks=[track])

    _ = show_page(album, track)

    # This will likely fail when ran on another timezone or even when daylight savings
    # change, but I don't yet know how to best write the test

    # edit: use renderAsOf(track, dateFormat)
    driver.shows_software_notice("Tagged with TGiT v1.0 on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_unavailable(driver):
    track = build.track()
    album = build.album(tracks=[track])
    _ = show_page(album, track)
    driver.shows_software_notice("")


def test_omits_tagger_information_from_software_notice_if_unavailable(driver):
    track = build.track(tagging_time="2014-03-23 20:33:00 UTC+0000")
    album = build.album(tracks=[track])
    _ = show_page(album, track)
    driver.shows_software_notice("Tagged on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_tagging_date_malformed(driver):
    track = build.track(tagger="TGiT", tagger_version="1.0", tagging_time="invalid-time-format")
    album = build.album(tracks=[track])
    _ = show_page(album, track)
    driver.shows_software_notice("Tagged with TGiT v1.0")


def test_signals_when_assign_lyricist_isni_button_clicked(driver):
    assign_isni_signal = ValueMatcherProbe("assign ISNI", instance_of(types.FunctionType))

    track = build.track()
    album = make_album(tracks=[track])

    _ = show_page(album,
                  track,
                  review_assignation=lambda on_review: on_review(),
                  on_lyricist_isni_assign=assign_isni_signal.received)

    driver.assign_isni_to_lyricist()
    driver.check(assign_isni_signal)


def test_shows_connection_failed_error_on_lyricist_isni_assignation(driver):
    show_error_signal = ValueMatcherProbe("ISNI assignation exception")

    track = build.track()
    album = make_album(tracks=[track])

    _ = show_page(album, track,
                  show_cheddar_connection_failed=show_error_signal.received,
                  review_assignation=lambda on_review: on_review(),
                  on_lyricist_isni_assign=lambda *_: raise_(requests.ConnectionError()))

    driver.assign_isni_to_lyricist()
    driver.check(show_error_signal)


def test_shows_assignation_failed_error_on_lyricist_isni_assignation(driver):
    show_error_signal = ValueMatcherProbe("ISNI assignation exception", "insufficient information")

    track = build.track()
    album = make_album(tracks=[track])

    _ = show_page(album, track,
                  show_isni_assignation_failed=show_error_signal.received,
                  review_assignation=lambda on_review: on_review(),
                  on_lyricist_isni_assign=lambda *_: raise_(InsufficientInformationError("insufficient information")))

    driver.assign_isni_to_lyricist()
    driver.check(show_error_signal)


def test_shows_authentication_failed_error_on_lyricist_isni_assignation(driver):
    show_error_signal = ValueMatcherProbe("ISNI authentication")

    track = build.track()
    album = make_album(tracks=[track])

    _ = show_page(album, track,
                  show_cheddar_authentication_failed=show_error_signal.received,
                  review_assignation=lambda on_review: on_review(),
                  on_lyricist_isni_assign=lambda *_: raise_(AuthenticationError()))

    driver.assign_isni_to_lyricist()
    driver.check(show_error_signal)


def test_shows_assigned_isni_on_lyricist_isni_assignation(driver):
    track = build.track()
    album = make_album(tracks=[track])

    page = show_page(album, track,
                     review_assignation=lambda on_review: on_review(),
                     on_lyricist_isni_assign=lambda callback: callback(
                         IdentityCard(id="0000000123456789", type=IdentityCard.INDIVIDUAL)))

    driver.assign_isni_to_lyricist()
    assert_that(page._lyricist_isni.text(), equal_to("0000000123456789"))


def test_signals_assigned_isni_on_isni_assignation(driver):
    metadata_changed_signal = ValueMatcherProbe("metadata changed")

    track = build.track()
    album = make_album(tracks=[track])

    page = show_page(album, track,
                     review_assignation=lambda on_review: on_review(),
                     on_lyricist_isni_assign=lambda callback: callback(
                         IdentityCard(id="0000000123456789", type=IdentityCard.INDIVIDUAL)))

    page.metadata_changed.connect(metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(lyricist=("Joel Miller", "0000000123456789")))
    driver.change_lyricist("Joel Miller")
    driver.assign_isni_to_lyricist()
    driver.confirm_lyricist_isni()
    driver.check(metadata_changed_signal)

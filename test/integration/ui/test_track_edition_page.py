# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_entries
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from drivers import TrackEditionPageDriver
from test.integration.ui import show_widget
from test.util import builders as build
from tgit.ui.track_edition_page import make_track_edition_page, TrackEditionPage


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    page_driver = TrackEditionPageDriver(window(TrackEditionPage, named("track_edition_page")), prober, automaton)
    yield page_driver
    page_driver.close()


ignore = lambda *_, **__: None


def show_track_page(album, track, on_track_changed=ignore):
    page = make_track_edition_page(album, track, on_track_changed)
    show_widget(page)
    return page


def test_displays_album_summary_in_banner(driver):
    track = build.track()
    album = build.album(release_name="Album Title", lead_performer="Artist", label_name="Record Label",
                        tracks=[build.track(), track, build.track()])

    _ = show_track_page(album, track)

    driver.shows_album_title("Album Title")
    driver.shows_album_lead_performer("Artist")
    driver.shows_track_number("2")


def test_indicates_when_album_performed_by_various_artists(driver):
    track = build.track()
    album = build.album(compilation=True, tracks=[track])

    _ = show_track_page(album, track)

    driver.shows_album_lead_performer("Various Artists")


def test_displays_track_metadata(driver):
    track = build.track(bitrate=192000,
                        duration=timedelta(minutes=4, seconds=35).total_seconds(),
                        lead_performer="Artist",
                        track_title="Song",
                        versionInfo="Remix",
                        featuredGuest="Featuring",
                        lyricist="Lyricist",
                        composer="Composer",
                        publisher="Publisher",
                        isrc="Code",
                        iswc="T-345246800-1",
                        labels="Tag1 Tag2 Tag3",
                        lyrics="Lyrics\n...\n...",
                        language="eng")
    album = build.album(compilation=True, tracks=[track])

    _ = show_track_page(album, track)

    driver.shows_track_title("Song")
    driver.shows_lead_performer("Artist")
    driver.shows_version_info("Remix")
    driver.shows_bitrate("192 kbps")
    driver.shows_duration("04:35")
    driver.shows_featured_guest("Featuring")
    driver.shows_lyricist("Lyricist")
    driver.shows_composer("Composer")
    driver.shows_publisher("Publisher")
    driver.shows_isrc("Code")
    driver.shows_iswc("T-345246800-1")
    driver.shows_tags("Tag1 Tag2 Tag3")
    driver.shows_lyrics("Lyrics\n...\n...")
    driver.shows_language("eng")
    driver.shows_preview_time("00:00")


def test_disables_lead_performer_edition_when_album_is_not_a_compilation(driver):
    track = build.track()
    album = build.album(lead_performer="Album Artist", compilation=False, tracks=[track])

    _ = show_track_page(album, track)

    driver.shows_lead_performer("Album Artist", disabled=True)


def test_signals_when_track_metadata_change(driver):
    track = build.track()
    album = build.album(compilation=True, tracks=[track])

    page = show_track_page(album, track)

    metadata_changed_signal = ValueMatcherProbe("metadata changed")
    page.metadata_changed.connect(metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(track_title="Title"))
    driver.change_track_title("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer="Artist"))
    driver.change_lead_performer("Artist")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(versionInfo="Remix"))
    driver.change_version_info("Remix")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(featuredGuest="Featuring"))
    driver.change_featured_guest("Featuring")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lyricist="Lyricist"))
    driver.change_lyricist("Lyricist")
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


def test_displays_software_notice_in_local_time(driver):
    track = build.track(tagger="TGiT", tagger_version="1.0", tagging_time="2014-03-23 20:33:00 +0000")
    album = build.album(tracks=[track])

    _ = show_track_page(album, track)

    # This will likely fail when ran on another timezone or even when daylight savings
    # change, but I don't yet know how to best write the test

    # edit: use renderAsOf(track, dateFormat)
    driver.shows_software_notice("Tagged with TGiT v1.0 on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_unavailable(driver):
    track = build.track()
    album = build.album(tracks=[track])
    _ = show_track_page(album, track)
    driver.shows_software_notice("")


def test_omits_tagger_information_from_software_notice_if_unavailable(driver):
    track = build.track(tagging_time="2014-03-23 20:33:00 UTC+0000")
    album = build.album(tracks=[track])
    _ = show_track_page(album, track)
    driver.shows_software_notice("Tagged on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_tagging_date_malformed(driver):
    track = build.track(tagger="TGiT", tagger_version="1.0", tagging_time="invalid-time-format")
    album = build.album(tracks=[track])
    _ = show_track_page(album, track)
    driver.shows_software_notice("Tagged with TGiT v1.0")
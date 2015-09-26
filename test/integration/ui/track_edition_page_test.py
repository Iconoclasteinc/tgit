# -*- coding: utf-8 -*-

from datetime import timedelta

from hamcrest import has_entries

from cute.probes import ValueMatcherProbe
from test.integration.ui import show_widget
from test.util import builders as build
from tgit.ui.track_edition_page import make_track_edition_page

ignore = lambda *_, **__: None


def show_track_page(album, track, on_track_changed=ignore):
    page = make_track_edition_page(album, track, on_track_changed)
    show_widget(page)
    return page


def test_displays_album_summary_in_banner(track_edition_page_driver):
    track = build.track()
    album = build.album(release_name="Album Title", lead_performer="Artist", label_name="Record Label",
                        tracks=[build.track(), track, build.track()])

    _ = show_track_page(album, track)

    track_edition_page_driver.shows_album_title("Album Title")
    track_edition_page_driver.shows_album_lead_performer("Artist")
    track_edition_page_driver.shows_track_number("2")


def test_indicates_when_album_performed_by_various_artists(track_edition_page_driver):
    track = build.track()
    album = build.album(compilation=True, tracks=[track])

    _ = show_track_page(album, track)

    track_edition_page_driver.shows_album_lead_performer("Various Artists")


def test_displays_track_metadata(track_edition_page_driver):
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
                        labels="Tag1 Tag2 Tag3",
                        lyrics="Lyrics\n...\n...",
                        language="eng")
    album = build.album(compilation=True, tracks=[track])

    _ = show_track_page(album, track)

    track_edition_page_driver.shows_track_title("Song")
    track_edition_page_driver.shows_lead_performer("Artist")
    track_edition_page_driver.shows_version_info("Remix")
    track_edition_page_driver.shows_bitrate("192 kbps")
    track_edition_page_driver.shows_duration("04:35")
    track_edition_page_driver.shows_featured_guest("Featuring")
    track_edition_page_driver.shows_lyricist("Lyricist")
    track_edition_page_driver.shows_composer("Composer")
    track_edition_page_driver.shows_publisher("Publisher")
    track_edition_page_driver.shows_isrc("Code")
    track_edition_page_driver.shows_iswc("")
    track_edition_page_driver.shows_tags("Tag1 Tag2 Tag3")
    track_edition_page_driver.shows_lyrics("Lyrics\n...\n...")
    track_edition_page_driver.shows_language("eng")
    track_edition_page_driver.shows_preview_time("00:00")


def test_disables_lead_performer_edition_when_album_is_not_a_compilation(track_edition_page_driver):
    track = build.track()
    album = build.album(lead_performer="Album Artist", compilation=False, tracks=[track])

    _ = show_track_page(album, track)

    track_edition_page_driver.shows_lead_performer("Album Artist", disabled=True)


def test_signals_when_track_metadata_change(track_edition_page_driver):
    track = build.track()
    album = build.album(compilation=True, tracks=[track])

    page = show_track_page(album, track)

    metadata_changed_signal = ValueMatcherProbe("metadata changed")
    page.metadata_changed.connect(metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(track_title="Title"))
    track_edition_page_driver.change_track_title("Title")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer="Artist"))
    track_edition_page_driver.change_lead_performer("Artist")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(versionInfo="Remix"))
    track_edition_page_driver.change_version_info("Remix")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(featuredGuest="Featuring"))
    track_edition_page_driver.change_featured_guest("Featuring")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lyricist="Lyricist"))
    track_edition_page_driver.change_lyricist("Lyricist")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(composer="Composer"))
    track_edition_page_driver.change_composer("Composer")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(publisher="Publisher"))
    track_edition_page_driver.change_publisher("Publisher")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(isrc="ZZZ123456789"))
    track_edition_page_driver.change_isrc("ZZZ123456789")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(labels="Tag1 Tag2 Tag3"))
    track_edition_page_driver.change_tags("Tag1 Tag2 Tag3")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lyrics="Lyrics\n...\n"))
    track_edition_page_driver.add_lyrics("Lyrics")
    track_edition_page_driver.add_lyrics("...")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(language="fra"))
    track_edition_page_driver.select_language("fra")
    track_edition_page_driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(language="eng"))
    track_edition_page_driver.change_language("eng")
    track_edition_page_driver.check(metadata_changed_signal)


def test_displays_software_notice_in_local_time(track_edition_page_driver):
    track = build.track(tagger="TGiT", tagger_version="1.0", tagging_time="2014-03-23 20:33:00 +0000")
    album = build.album(tracks=[track])

    _ = show_track_page(album, track)

    # This will likely fail when ran on another timezone or even when daylight savings
    # change, but I don't yet know how to best write the test

    # edit: use renderAsOf(track, dateFormat)
    track_edition_page_driver.shows_software_notice("Tagged with TGiT v1.0 on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_unavailable(track_edition_page_driver):
    track = build.track()
    album = build.album(tracks=[track])
    _ = show_track_page(album, track)
    track_edition_page_driver.shows_software_notice("")


def test_omits_tagger_information_from_software_notice_if_unavailable(track_edition_page_driver):
    track = build.track(tagging_time="2014-03-23 20:33:00 UTC+0000")
    album = build.album(tracks=[track])
    _ = show_track_page(album, track)
    track_edition_page_driver.shows_software_notice("Tagged on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_tagging_date_malformed(track_edition_page_driver):
    track = build.track(tagger="TGiT", tagger_version="1.0", tagging_time="invalid-time-format")
    album = build.album(tracks=[track])
    _ = show_track_page(album, track)
    track_edition_page_driver.shows_software_notice("Tagged with TGiT v1.0")

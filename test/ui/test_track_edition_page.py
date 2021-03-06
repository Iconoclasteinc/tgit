from datetime import timedelta

import pytest
from hamcrest import has_entries, has_key, is_not

from cute.matchers import named
from cute.probes import KeywordsValueMatcherProbe
from cute.widgets import window
from test.ui import show_, close_, ignore
from testing import builders as build
from testing.builders import make_album, make_track
from testing.drivers import TrackEditionPageDriver
from tgit.ui.pages.chain_of_title_tab import ChainOfTitleTab
from tgit.ui.pages.contributors_tab import ContributorsTab
from tgit.ui.pages.track_edition_page import make_track_edition_page, TrackEditionPage

pytestmark = pytest.mark.ui


@pytest.yield_fixture()
def driver(prober, automaton):
    page_driver = TrackEditionPageDriver(window(TrackEditionPage, named("track_edition_page")), prober, automaton)
    yield page_driver
    close_(page_driver)


def create_contributors_tab(*_):
    return ContributorsTab(ignore, ignore)


def create_chain_of_title_tab(*_):
    return ChainOfTitleTab()


def show_page(album, track, contributors_tab=create_contributors_tab, chain_of_title_tab=create_chain_of_title_tab,
              **handlers):
    page = make_track_edition_page(album, track, contributors_tab, chain_of_title_tab, **handlers)
    show_(page)
    return page


def test_displays_album_summary_in_banner(driver):
    track = make_track()
    album = make_album(release_name="Album Title", lead_performer="Artist", label_name="Record Label",
                       tracks=[build.track(), track, build.track()])

    _ = show_page(album, track)

    driver.shows_album_title("Album Title")
    driver.shows_album_lead_performer("Artist")
    driver.shows_track_number("2")


def test_indicates_when_album_performed_by_various_artists(driver):
    track = make_track()
    album = make_album(compilation=True, tracks=[track])

    _ = show_page(album, track)

    driver.shows_album_lead_performer("Various Artists")


def test_displays_track_metadata(driver):
    track = make_track(bitrate=192000,
                       duration=timedelta(minutes=4, seconds=35).total_seconds(),
                       lead_performer="Artist",
                       track_title="Song",
                       version_info="Remix",
                       featured_guest="Featuring",
                       comments="Comments\n...",
                       isrc="Code",
                       iswc="T-345246800-1",
                       labels="Tag1 Tag2 Tag3",
                       lyrics="Lyrics\n...\n...",
                       language="eng",
                       recording_time="2008-09-15",
                       production_company="Initial Producer",
                       production_company_region=("CA", "MTL"),
                       recording_studio="Studio A, Studio B",
                       recording_studio_region=("CA", "MTL"),
                       recording_studio_address="2020 des zinzins, Montreal",
                       music_producer="Artistic Producer",
                       mixer="Mixing Engineer",
                       primary_style="Style")
    album = make_album(compilation=True, tracks=[track])

    _ = show_page(album, track)

    driver.shows_track_title("Song")
    driver.shows_lead_performer("Artist")
    driver.shows_version_info("Remix")
    driver.shows_bitrate("192 kbps")
    driver.shows_duration("04:35")
    driver.shows_featured_guest("Featuring")
    driver.shows_isrc("Code")
    driver.shows_iswc("T-345246800-1")
    driver.shows_tags("Tag1 Tag2 Tag3")
    driver.shows_lyrics("Lyrics\n...\n...")
    driver.shows_language("English")
    driver.shows_recording_studio("Studio A, Studio B")
    driver.shows_recording_studio_region("CA MTL")
    driver.shows_recording_studio_address("2020 des zinzins, Montreal")
    driver.shows_production_company("Initial Producer")
    driver.shows_production_company_region("CA MTL")
    driver.shows_recording_time("2008-09-15")
    driver.shows_music_producer("Artistic Producer")
    driver.shows_mixer("Mixing Engineer")
    driver.shows_primary_style("Style")
    driver.shows_comments("Comments\n...")


def test_displays_undefined_lyrics_language_in_case_no_language_specified(driver):
    track = make_track()
    album = make_album(tracks=[track])

    _ = show_page(album, track)

    driver.shows_language("Undetermined")


def test_disables_lead_performer_edition_when_album_is_not_a_compilation(driver):
    track = make_track()
    album = make_album(lead_performer="Album Artist", compilation=False, tracks=[track])

    _ = show_page(album, track)

    driver.shows_lead_performer("Album Artist", disabled=True)


def test_signals_when_track_metadata_change(driver):
    track = make_track()
    album = make_album(compilation=True, tracks=[track])

    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(album, track, on_track_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(has_entries(track_title="Title"))
    driver.change_track_title("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(lead_performer="Artist"))
    driver.change_lead_performer("Artist")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(version_info="Remix"))
    driver.change_version_info("Remix")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(featured_guest="Featuring"))
    driver.change_featured_guest("Featuring")
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
    driver.change_lyrics("Lyrics", "...")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(language="fra"))
    driver.select_language("French")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(production_company="Producer"))
    driver.change_production_company("Producer")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(production_company_region=("CA", "MTL")))
    driver.change_production_company_region("CA MTL")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studio="Studios"))
    driver.change_recording_studio("Studios")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studio_region=("CA", "MTL")))
    driver.change_recording_studio_region("CA MTL")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_studio_address="2020 des zinzins, Montreal"))
    driver.change_recording_studio_address("2020 des zinzins, Montreal")
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

    metadata_changed_signal.expect(has_entries(comments="Comments\n...\n"))
    driver.change_comments("Comments", "...")
    driver.check(metadata_changed_signal)


def test_signals_main_artist_only_when_album_is_compilation(driver):
    track = make_track()
    album = make_album(compilation=False, tracks=[track])

    metadata_changed_signal = KeywordsValueMatcherProbe("metadata changed")
    _ = show_page(album, track, on_track_changed=metadata_changed_signal.received)

    metadata_changed_signal.expect(is_not(has_key("lead_performer")))
    driver.change_track_title("Title")
    driver.check(metadata_changed_signal)

    metadata_changed_signal.expect(has_entries(recording_time="2008-09-15"))
    driver.change_recording_time(2008, 9, 15)
    driver.check(metadata_changed_signal)


def test_displays_software_notice_in_local_time(driver):
    track = make_track(tagger="TGiT", tagger_version="1.0", tagging_time="2014-03-23 20:33:00 +0000")
    album = make_album(tracks=[track])

    _ = show_page(album, track)

    # This will likely fail when ran on another timezone or even when daylight savings
    # change, but I don't yet know how to best write the test

    # edit: use renderAsOf(track, dateFormat)
    driver.shows_software_notice("Tagged with TGiT v1.0 on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_unavailable(driver):
    track = make_track()
    album = make_album(tracks=[track])
    _ = show_page(album, track)
    driver.shows_software_notice("")


def test_omits_tagger_information_from_software_notice_if_unavailable(driver):
    track = make_track(tagging_time="2014-03-23 20:33:00 UTC+0000")
    album = make_album(tracks=[track])
    _ = show_page(album, track)
    driver.shows_software_notice("Tagged on 2014-03-23 at 16:33:00")


def test_omits_software_notice_if_tagging_date_malformed(driver):
    track = make_track(tagger="TGiT", tagger_version="1.0", tagging_time="invalid-time-format")
    album = make_album(tracks=[track])
    _ = show_page(album, track)
    driver.shows_software_notice("Tagged with TGiT v1.0")

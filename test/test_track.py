from flexmock import flexmock
import pytest
from hamcrest import assert_that, has_entry, all_of, equal_to, has_key
from hamcrest import contains_inanyorder, contains, has_property

from test.test_signal import Subscriber
from testing import builders as build
from testing.builders import make_track, metadata
from tgit.track import Track

pytestmark = pytest.mark.unit


def test_defines_metadata_tags():
    assert_that(tuple(Track.tags()), contains_inanyorder(
        "track_title", "lead_performer", "version_info", "featured_guest", "publisher", "lyricist", "composer", "isrc",
        "iswc", "labels", "lyrics", "language", "tagger", "tagger_version", "tagging_time", "bitrate", "duration",
        "track_number", "total_tracks", "recording_studio", "production_company", "production_company_region",
        "recording_studio_region", "music_producer", "mixer", "primary_style", "comments", "recording_time",
        "recording_studio_address"))


def test_announces_metadata_changes_to_listeners():
    _assert_notifies_of_metadata_change("track_title", "Title")
    _assert_notifies_of_metadata_change("version_info", "Remix")
    _assert_notifies_of_metadata_change("featured_guest", "Featuring")
    _assert_notifies_of_metadata_change("lyricist", ["Joel Miller"])
    _assert_notifies_of_metadata_change("isrc", "Code")
    _assert_notifies_of_metadata_change("iswc", "T-345246800-1")
    _assert_notifies_of_metadata_change("track_number", 1)
    _assert_notifies_of_metadata_change("total_tracks", 3)
    _assert_notifies_of_metadata_change("recording_time", "Recorded")


def test_updates_the_track_chain_of_title():
    track = make_track()
    flexmock(track.chain_of_title).should_receive("update").once()
    track.update()


def test_returns_the_track_chain_of_title_contributors():
    track = make_track()
    assert_that(track.chain_of_title.contributors, all_of(has_key("authors_composers"), has_key("publishers")),
                "The contributors")


def test_updates_track_metadata():
    track = make_track()
    track.update(track_title="Title", lead_performer="Artist", version_info="Version",
                 featured_guest="Featuring", lyricist=["Lyricist"], composer=["Composer"],
                 publisher=["Publisher"], isrc="ZZZ123456789", labels="Tags",
                 lyrics="Lyrics\nLyrics\n...", language="und")

    assert_that(track.track_title, equal_to("Title"), "track title")
    assert_that(track.lead_performer, equal_to("Artist"), "lead performer")
    assert_that(track.version_info, equal_to("Version"), "version info")
    assert_that(track.featured_guest, equal_to("Featuring"), "featured guest")
    assert_that(track.lyricist, contains("Lyricist"), "lyricist")
    assert_that(track.composer, contains("Composer"), "composer")
    assert_that(track.publisher, contains("Publisher"), "publisher")
    assert_that(track.isrc, equal_to("ZZZ123456789"), "isrc")
    assert_that(track.labels, equal_to("Tags"), "tags")
    assert_that(track.lyrics, equal_to("Lyrics\nLyrics\n..."), "lyrics")
    assert_that(track.language, equal_to("und"), "language")


def test_creates_default_chain_of_title_from_metadata():
    source_metadata = metadata(lyricist=["Joel Miller"], composer=["John Roney"], publisher=["Effendi Records"])
    track = make_track(metadata_from=source_metadata)

    assert_that(track.chain_of_title.contributors,
                all_of(has_author_composer("John Roney", has_entry("name", "John Roney")),
                       has_author_composer("Joel Miller", has_entry("name", "Joel Miller")),
                       has_publisher("Effendi Records", has_entry("name", "Effendi Records"))),
                "The chain of title")


def _assert_notifies_of_metadata_change(prop, value):
    track = build.track()
    subscriber = Subscriber()
    track.metadata_changed.subscribe(subscriber)

    setattr(track, prop, value)

    assert_that(subscriber.events, contains(contains(has_property(prop, value))), "track changed events")


def has_author_composer(name, matching):
    return has_entry("authors_composers", has_entry(name, matching))


def has_publisher(name, matching):
    return has_entry("publishers", has_entry(name, matching))


def joel_miller():
    return dict(name="Joel Miller", affiliation="SOCAN", publisher="Effendi Records", share="25")


def john_roney():
    return dict(name="John Roney", affiliation="ASCAP", publisher="Effendi Records", share="25")


def effendi_records():
    return dict(name="Effendi Records", share="50")

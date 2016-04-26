import pytest
from hamcrest import assert_that
from hamcrest import contains_inanyorder, contains, has_property

from test.test_signal import Subscriber
from testing import builders as build
from tgit.track import Track

pytestmark = pytest.mark.unit


def test_defines_metadata_tags():
    assert_that(tuple(Track.tags()), contains_inanyorder(
        "track_title", "lead_performer", "version_info", "featured_guest", "publisher", "lyricist", "composer", "isrc",
        "iswc", "labels", "lyrics", "language", "tagger", "tagger_version", "tagging_time", "bitrate", "duration",
        "track_number", "total_tracks", "recording_studio", "production_company", "production_company_region",
        "recording_studio_region", "music_producer", "mixer", "primary_style", "comments", "recording_time"))


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


def _assert_notifies_of_metadata_change(prop, value):
    track = build.track()
    subscriber = Subscriber()
    track.metadata_changed.subscribe(subscriber)

    setattr(track, prop, value)

    assert_that(subscriber.events, contains(contains(has_property(prop, value))), "track changed events")

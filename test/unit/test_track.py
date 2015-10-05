# -*- coding: utf-8 -*-

from hamcrest import contains_inanyorder, contains, has_entry
from hamcrest import assert_that

from test.test_signal import Subscriber
from test.util import builders as build
from tgit.track import Track


def test_defines_metadata_tags():
    assert_that(tuple(Track.tags()), contains_inanyorder(
        'track_title', 'lead_performer', 'versionInfo', 'featuredGuest', 'publisher',
        'lyricist', 'composer', 'isrc', "iswc", 'labels', 'lyrics', 'language', 'tagger',
        'tagger_version', 'tagging_time', 'bitrate', 'duration', 'track_number', 'total_tracks'))


def test_announces_metadata_changes_to_listeners():
    assert_notifies_of_metadata_change('track_title', 'Title')
    assert_notifies_of_metadata_change('versionInfo', 'Remix')
    assert_notifies_of_metadata_change('featuredGuest', 'Featuring')
    assert_notifies_of_metadata_change('isrc', 'Code')
    assert_notifies_of_metadata_change("iswc", "T-345246800-1")
    assert_notifies_of_metadata_change('track_number', 1)
    assert_notifies_of_metadata_change('total_tracks', 3)


def assert_notifies_of_metadata_change(prop, value):
    track = build.track()
    subscriber = Subscriber()
    track.metadata_changed.subscribe(subscriber)

    setattr(track, prop, value)

    assert_that(subscriber.events, contains(contains(has_entry(prop, value))), "track changed events")

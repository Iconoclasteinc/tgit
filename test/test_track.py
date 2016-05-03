import pytest
from hamcrest import assert_that, has_entry, has_entries, not_, has_key, any_of, empty, all_of
from hamcrest import contains_inanyorder, contains, has_property

from test.test_signal import Subscriber
from testing import builders as build
from testing.builders import make_track, metadata, make_metadata
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


def test_creates_default_chain_of_title_from_metadata():
    source_metadata = metadata(lyricist=["Joel Miller"], composer=["John Roney"], publisher=["Effendi Records"])
    track = make_track(metadata_from=source_metadata)

    assert_that(track.chain_of_title.contributors,
                all_of(has_author_composer("John Roney", has_entry("name", "John Roney")),
                       has_author_composer("Joel Miller", has_entry("name", "Joel Miller")),
                       has_publisher("Effendi Records", has_entry("name", "Effendi Records"))),
                "The chain of title")


def test_removes_contributor_from_chain_of_title():
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller", "John Roney"],
                                              composer=["John Lennon", "Yoko Ono"],
                                              publisher=["Effendi Records", "Universals"]))
    track.lyricist = ["Joel Miller"]
    track.composer = ["John Lennon"]
    track.publisher = ["Effendi Records"]
    track.update_chain_of_title()

    assert_that(track.chain_of_title, not_(any_of(has_key("John Roney"), has_key("Yoko Ono"), has_key("Universals"))),
                "The chain of title")


def test_adds_contributor_to_chain_of_title():
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"], composer=["John Lennon"],
                                              publisher=["Effendi Records"]))
    track.lyricist = ["Joel Miller", "John Roney"]
    track.composer = ["John Lennon", "Yoko Ono"]
    track.publisher = ["Effendi Records", "Universals"]
    track.update_chain_of_title()

    assert_that(track.chain_of_title.contributors,
                all_of(has_author_composer("John Roney", has_entry("name", "John Roney")),
                       has_author_composer("Yoko Ono", has_entry("name", "Yoko Ono")),
                       has_publisher("Universals", has_entry("name", "Universals"))),
                "The chain of title")


def test_removes_linked_publisher_from_a_contributor_when_removing_a_publisher():
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"], composer=["John Roney"],
                                              publisher=["Effendi Records"]))
    track.load_chain_of_title({
        "authors_composers": {"Joel Miller": joel_miller(), "John Roney": john_roney()},
        "publishers": {"Effendi Records": effendi_records()}
    })

    track.publisher = []
    track.update_chain_of_title()

    assert_that(track.chain_of_title.contributors,
                all_of(has_author_composer("John Roney", has_entry("publisher", "")),
                       has_author_composer("Joel Miller", has_entry("publisher", "")),
                       has_entry("publishers", not_(has_key("Effendi Records")))),
                "The chain of title")


def test_signals_chain_of_value_changed_on_contributor_added():
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"]))
    track.lyricist = ["Joel Miller", "John Roney"]

    subscriber = Subscriber()
    track.chain_of_title_changed.subscribe(subscriber)

    track.update_chain_of_title()

    assert_that(subscriber.events, contains(contains(has_property("contributors", all_of(
        has_author_composer("John Roney", has_entry("name", "John Roney")),
        has_author_composer("Joel Miller", has_entry("name", "Joel Miller")))))), "The chain of title")


def test_does_not_signal_chain_of_value_when_contributors_have_not_changed():
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"]))

    subscriber = Subscriber()
    track.chain_of_title_changed.subscribe(subscriber)

    track.update_chain_of_title()

    assert_that(subscriber.events, empty(), "The chain of title")


def test_signals_chain_of_value_changed_when_contributor_role_changes_from_lyricist_to_publisher():
    track = make_track(metadata_from=metadata(lyricist=["Joel Miller"]))
    track.load_chain_of_title({"authors_composers": {"Joel Miller": joel_miller()}, "publishers": {}})

    track.publisher = ["Joel Miller"]
    track.lyricist = []

    subscriber = Subscriber()
    track.chain_of_title_changed.subscribe(subscriber)

    track.update_chain_of_title()

    assert_that(subscriber.events, contains(contains(
        has_property("contributors", has_publisher("Joel Miller", has_entry("name", "Joel Miller"))))),
                "The chain of title")


def test_updates_contributors():
    track = make_track(metadata_from=make_metadata(lyricist=["Joel Miller"], composer=["John Roney"],
                                                   publisher=["Effendi Records"]))
    track.update_contributor(**joel_miller())
    track.update_contributor(**john_roney())
    track.update_contributor(**effendi_records())

    assert_that(track.chain_of_title.contributors, has_author_composer("Joel Miller", has_entries(joel_miller())),
                "The contributors")
    assert_that(track.chain_of_title.contributors, has_author_composer("John Roney", has_entries(john_roney())),
                "The contributors")
    assert_that(track.chain_of_title.contributors, has_publisher("Effendi Records", has_entries(effendi_records())),
                "The contributors")


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

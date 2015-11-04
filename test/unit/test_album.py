# -*- coding: utf-8 -*-

from flexmock import flexmock
from hamcrest import (assert_that, equal_to, is_, contains, has_property, none, has_length, has_item, is_not,
                      match_equality as matching, contains_inanyorder, not_, has_key, all_of)
from hamcrest.library.collection.is_empty import empty

from test.test_signal import Subscriber, event
from test.util import builders as build
from test.util.builders import make_album, make_track
from tgit.album import Album, AlbumListener
from tgit.metadata import Image


def test_defines_metadata_tags():
    assert_that(tuple(Album.tags()), contains_inanyorder(
        "release_name", "compilation", "lead_performer", "lead_performer_region", "isni", "guest_performers",
        "label_name", "upc", "catalog_number", "recording_time", "release_time", "original_release_time",
        "recording_studios", "recording_studio_region", "production_company", "production_company_region", "music_producer", "mixer", "contributors", "comments",
        "primary_style"))


def test_initializes_with_album_only_metadata():
    metadata = build.metadata(track_title="Smash Smash",
                              release_name="Honeycomb",
                              lead_performer="Joel Miller",
                              images=[build.image(data=b"front.jpeg")])

    album = Album(metadata)

    assert_that(album.release_name, equal_to("Honeycomb"), "release name")
    assert_that(album.lead_performer, equal_to("Joel Miller"), "lead performer")
    assert_that(album.images, contains(has_property("data", b"front.jpeg")), "attached pictures")
    assert_that(album.metadata, not_(has_key("track_title")), "album metadata")


def test_contained_tracks_have_lead_performer_of_album_when_album_is_not_a_compilation():
    track = build.track(lead_performer="???")
    album = build.album(lead_performer="Joel Miller")

    album.add_track(track)

    assert_that(track.lead_performer, equal_to("Joel Miller"), "track lead performer")


def test_contained_tracks_have_various_lead_performers_when_album_is_a_compilation():
    track = build.track(lead_performer="Joel Miller")
    compilation = build.album(lead_performer="Various Artists", compilation=True)

    compilation.add_track(track)

    assert_that(track.lead_performer, equal_to("Joel Miller"), "track lead performer")


def assert_has_numbered_tracks(album):
    for position, track in enumerate(album.tracks):
        assert_that(track, all_of(has_property("track_number", position + 1),
                                  has_property("total_tracks", len(album))), "track at position #{}".format(position))


def test_numbers_tracks():
    album = make_album(tracks=(build.track(), build.track(), build.track()))

    assert_has_numbered_tracks(album)


def test_renumbers_tracks_when_removed():
    album = make_album(tracks=(build.track(), build.track(), build.track()))

    album.remove_track(0)

    assert_has_numbered_tracks(album)


def test_signals_track_insertion_events():
    album = build.album()
    subscriber = Subscriber()
    tracks = [build.track(), build.track(), build.track()]

    album.track_inserted.subscribe(subscriber)
    for track in tracks:
        album.add_track(track)

    for index, track in enumerate(tracks):
        assert_that(subscriber.events, has_item(event(index, track)), "track {0} insertion event".format(index))


def test_signals_track_removal_events():
    tracks = [build.track(), build.track(), build.track()]
    album = build.album()
    for track in tracks:
        album.add_track(track)

    subscriber = Subscriber()
    album.track_removed.subscribe(subscriber)

    for index in reversed(range(len(album))):
        album.remove_track(index)

    for index, track in enumerate(tracks):
        assert_that(subscriber.events, has_item(contains(index, track)), "track {0} removal event".format(index))


def has_title(title):
    return has_property("track_title", title)


def test_signals_track_move_events():
    album = make_album(tracks=(make_track(track_title="Salsa Coltrane"),
                               make_track(track_title="Zumbar"),
                               make_track(track_title="Chevere!")))
    subscriber = Subscriber()
    album.track_moved.subscribe(subscriber)

    album.move_track(1, 0)

    assert_that(subscriber.events, has_item(contains(has_title("Zumbar"), 1, 0)), "move event")


def test_renumbers_tracks_when_moved():
    album = make_album(tracks=(build.track(), build.track(), build.track()))

    album.move_track(1, 0)

    assert_has_numbered_tracks(album)


def test_is_initially_empty():
    assert_that(build.album().empty(), is_(True), "emptiness")


def test_is_no_longer_empty_when_holding_tracks():
    album = Album()
    album.add_track(build.track())
    assert_that(album.empty(), is_(False), "emptiness")


def test_associates_track_to_album():
    album = Album()
    track = build.track()
    album.add_track(track)
    assert_that(track.album, is_(album), "album of track")


def test_holds_a_list_of_tracks_in_order():
    album = Album()
    album.add_track(build.track(track_title="Track 1"))
    album.add_track(build.track(track_title="Track 2"))
    album.add_track(build.track(track_title="Track 3"))

    assert_that(album.tracks, contains(
        has_property("track_title", "Track 1"),
        has_property("track_title", "Track 2"),
        has_property("track_title", "Track 3")), "track titles")


def test_allows_removing_tracks():
    album = build.album(tracks=[
        build.track(track_title="Track 1"),
        build.track(track_title="Track 2"),
        build.track(track_title="Track 3")])

    album.remove_track(1)

    assert_that(album.tracks, has_length(2), "remaining tracks")
    assert_that(album.tracks, is_not(has_item(has_property("track_title", "Track 2"))), "tracks")


def test_supports_inserting_tracks_at_a_specific_positions():
    album = build.album(tracks=[
        build.track(track_title="Track 1"),
        build.track(track_title="Track 2"),
        build.track(track_title="Track 3")])

    first = album.remove_track(0)
    album.insert_track(first, 1)

    assert_that(album.tracks, contains(
        has_property("track_title", "Track 2"),
        has_property("track_title", "Track 1"),
        has_property("track_title", "Track 3")), "tracks")


def test_uses_first_front_cover_or_first_image_as_main_cover():
    album = build.album()
    assert_that(album.main_cover, is_(None))
    album.add_image("image/jepg", "back cover image")
    assert_that(album.main_cover, has_property("data", "back cover image"))
    album.add_front_cover("image/jpeg", "front cover image")
    assert_that(album.main_cover, has_property("data", "front cover image"))


def test_has_initially_no_metadata_or_images():
    album = Album()
    for tag in Album.tags():
        assert_that(getattr(album, tag), none(), tag)

    assert_that(album.images, empty(), "images")


def test_signals_state_changes_to_listener():
    _assert_notifies_listener_on_property_change("release_name", "Album")
    _assert_notifies_listener_on_property_change("lead_performer", "Artist")
    _assert_notifies_listener_on_property_change("isni", "123456789")
    _assert_notifies_listener_on_property_change("guest_performers", [("Musician", "Instrument")])
    _assert_notifies_listener_on_property_change("label_name", "Label")
    _assert_notifies_listener_on_property_change("recording_time", "Recorded")
    _assert_notifies_listener_on_property_change("release_time", "Released")
    _assert_notifies_listener_on_property_change("original_release_time", "Original Release")
    _assert_notifies_listener_on_property_change("upc", "Barcode")
    _assert_notifies_listener_on_images_change(Image("image/jpeg", "front-cover.jpg"))


def test_signals_track_insertion_to_listeners():
    album = build.album()
    listener = flexmock(AlbumListener())
    album.addAlbumListener(listener)

    first = build.track()
    listener.should_receive("trackAdded").with_args(first, 0).once()
    album.add_track(first)

    last = build.track()
    listener.should_receive("trackAdded").with_args(last, 1).once()
    album.add_track(last)

    middle = build.track()
    listener.should_receive("trackAdded").with_args(middle, 1).once()
    album.insert_track(middle, 1)


def test_signals_track_removal_to_listeners():
    album = build.album(tracks=[build.track(), build.track()])
    listener = flexmock(AlbumListener())
    album.addAlbumListener(listener)

    first, second = album.tracks[0], album.tracks[1]
    listener.should_receive("trackRemoved").with_args(second, 1).once()
    listener.should_receive("trackRemoved").with_args(first, 0).once()

    album.remove_track(position=1)
    album.remove_track(position=0)


def _assert_notifies_listener_on_property_change(prop, value):
    album = Album()
    album.addAlbumListener(_listener_expecting_notification(prop, value))
    setattr(album, prop, value)


def _listener_expecting_notification(prop, value):
    listener = flexmock(AlbumListener())
    listener.should_receive("albumStateChanged").with_args(matching(has_property(prop, value))).once()
    return listener


def _assert_notifies_listener_on_images_change(*images):
    _assert_notifies_listener_when_images_removed()
    for image in images:
        _assert_notifies_listeners_when_image_added(image)


def _assert_notifies_listener_when_images_removed():
    album = Album()
    album.addAlbumListener(_listener_expecting_notification("images", empty()))
    album.remove_images()


def _assert_notifies_listeners_when_image_added(image):
    album = Album()
    album.addAlbumListener(_listener_expecting_notification("images", has_item(image)))
    album.add_image(image.mime, image.data, image.type, image.desc)

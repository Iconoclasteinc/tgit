# -*- coding: utf-8 -*-

import unittest

from hamcrest import (assert_that, equal_to, is_, contains, has_property, none, has_length, has_item, is_not,
                      match_equality as matching, contains_inanyorder, not_, has_key, all_of)
from hamcrest.library.collection.is_empty import empty
from flexmock import flexmock

from test.test_signal import Subscriber, event
from test.util import builders as build
from test.util.builders import make_album, make_track
from tgit.metadata import Image
from tgit.album import Album, AlbumListener


def test_defines_metadata_tags():
    assert_that(tuple(Album.tags()), contains_inanyorder(
        'release_name', 'compilation', 'lead_performer', 'isni', 'guest_performers', 'label_name', 'upc',
        'catalog_number', 'recording_time', 'release_time', 'original_release_time', 'recording_studios', 'producer',
        'mixer', 'contributors', 'comments', 'primary_style'))


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
    track = build.track(lead_performer='???')
    album = build.album(lead_performer='Joel Miller')

    album.addTrack(track)

    assert_that(track.lead_performer, equal_to('Joel Miller'), 'track lead performer')


def test_contained_tracks_have_various_lead_performers_when_album_is_a_compilation():
    track = build.track(lead_performer='Joel Miller')
    compilation = build.album(lead_performer='Various Artists', compilation=True)

    compilation.addTrack(track)

    assert_that(track.lead_performer, equal_to('Joel Miller'), 'track lead performer')


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
        album.addTrack(track)

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



class AlbumTest(unittest.TestCase):
    def testIsInitiallyEmpty(self):
        assert_that(build.album().empty(), is_(True), 'emptiness')

    def testIsNoLongerEmptyWhenHoldingTracks(self):
        album = Album()
        album.addTrack(build.track())
        assert_that(album.empty(), is_(False), 'emptiness')

    def testAssociatesTrackToAlbum(self):
        album = Album()
        track = build.track()
        album.addTrack(track)
        assert_that(track.album, is_(album), 'album of track')

    def testHoldsAListOfTracksInOrder(self):
        album = Album()
        album.addTrack(build.track(track_title='Track 1'))
        album.addTrack(build.track(track_title='Track 2'))
        album.addTrack(build.track(track_title='Track 3'))

        assert_that(album.tracks, contains(
            has_property('track_title', 'Track 1'),
            has_property('track_title', 'Track 2'),
            has_property('track_title', 'Track 3')), 'track titles')

    def testAllowsRemovingTracks(self):
        album = build.album(tracks=[
            build.track(track_title='Track 1'),
            build.track(track_title='Track 2'),
            build.track(track_title='Track 3')])

        album.remove_track(1)

        assert_that(album.tracks, has_length(2), 'remaining tracks')
        assert_that(album.tracks, is_not(has_item(has_property('track_title', 'Track 2'))), 'tracks')

    def testSupportsInsertingTracksAtASpecificPositions(self):
        album = build.album(tracks=[
            build.track(track_title='Track 1'),
            build.track(track_title='Track 2'),
            build.track(track_title='Track 3')])

        first = album.removeTrack(0)
        album.insertTrack(first, 1)

        assert_that(album.tracks, contains(
            has_property('track_title', 'Track 2'),
            has_property('track_title', 'Track 1'),
            has_property('track_title', 'Track 3')), 'tracks')

    def testUsesFirstFrontCoverOrFirstImageAsMainCover(self):
        album = build.album()
        assert_that(album.mainCover, is_(None))
        album.addImage('image/jepg', 'back cover image')
        assert_that(album.mainCover, has_property('data', 'back cover image'))
        album.addFrontCover('image/jpeg', 'front cover image')
        assert_that(album.mainCover, has_property('data', 'front cover image'))

    def testHasInitiallyNoMetadataOrImages(self):
        album = Album()
        for tag in Album.tags():
            assert_that(getattr(album, tag), none(), tag)

        assert_that(album.images, empty(), 'images')

    def testSignalsStateChangesToListener(self):
        self.assertNotifiesListenerOnPropertyChange('release_name', 'Album')
        self.assertNotifiesListenerOnPropertyChange('lead_performer', 'Artist')
        self.assertNotifiesListenerOnPropertyChange('isni', '123456789')
        self.assertNotifiesListenerOnPropertyChange('guest_performers', [('Musician', 'Instrument')])
        self.assertNotifiesListenerOnPropertyChange('label_name', 'Label')
        self.assertNotifiesListenerOnPropertyChange('recording_time', 'Recorded')
        self.assertNotifiesListenerOnPropertyChange('release_time', 'Released')
        self.assertNotifiesListenerOnPropertyChange('original_release_time', 'Original Release')
        self.assertNotifiesListenerOnPropertyChange('upc', 'Barcode')
        self.assertNotifiesListenerOnImagesChange(Image('image/jpeg', 'front-cover.jpg'))

    def testSignalsTrackInsertionToListeners(self):
        album = build.album()
        listener = flexmock(AlbumListener())
        album.addAlbumListener(listener)

        first = build.track()
        listener.should_receive('trackAdded').with_args(first, 0).once()
        album.addTrack(first)

        last = build.track()
        listener.should_receive('trackAdded').with_args(last, 1).once()
        album.addTrack(last)

        middle = build.track()
        listener.should_receive('trackAdded').with_args(middle, 1).once()
        album.insertTrack(middle, 1)

    def testSignalsTrackRemovalToListeners(self):
        album = build.album(tracks=[build.track(), build.track()])
        listener = flexmock(AlbumListener())
        album.addAlbumListener(listener)

        first, second = album.tracks[0], album.tracks[1]
        listener.should_receive('trackRemoved').with_args(second, 1).once()
        listener.should_receive('trackRemoved').with_args(first, 0).once()

        album.remove_track(position=1)
        album.remove_track(position=0)

    def assertNotifiesListenerOnPropertyChange(self, prop, value):
        album = Album()
        album.addAlbumListener(self.listenerExpectingNotification(prop, value))
        setattr(album, prop, value)

    def listenerExpectingNotification(self, prop, value):
        listener = flexmock(AlbumListener())
        listener.should_receive('albumStateChanged').with_args(matching(has_property(prop, value))).once()
        return listener

    def assertNotifiesListenerOnImagesChange(self, *images):
        self.assertNotifiesListenerWhenImagesRemoved()
        for image in images:
            self.assertNotifiesListenersWhenImageAdded(image)

    def assertNotifiesListenerWhenImagesRemoved(self):
        album = Album()
        album.addAlbumListener(self.listenerExpectingNotification('images', empty()))
        album.removeImages()

    def assertNotifiesListenersWhenImageAdded(self, image):
        album = Album()
        album.addAlbumListener(self.listenerExpectingNotification('images', has_item(image)))
        album.addImage(image.mime, image.data, image.type, image.desc)

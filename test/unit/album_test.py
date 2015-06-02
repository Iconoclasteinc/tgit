# -*- coding: utf-8 -*-

import unittest

from hamcrest import (assert_that, equal_to, is_, contains, has_property, none,
                      has_length, has_item, is_not, match_equality as matching)
from hamcrest.library.collection.is_empty import empty
from flexmock import flexmock
from test.test_signal import Subscriber, event

from test.util import builders as build
from tgit.metadata import Image
from tgit.album import Album, AlbumListener


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


def track_numbers(album):
    return [album.track_number(track) for track in album.tracks]


def test_numbers_tracks():
    album = Album()
    tracks = [build.track(), build.track(), build.track()]
    for track in tracks:
        album.addTrack(track)

    assert_that(tracks[0].track_number, equal_to(1), 'track #1 number')
    assert_that(tracks[1].track_number, equal_to(2), 'track #2 number')
    assert_that(tracks[2].track_number, equal_to(3), 'track #3 number')

    for track in album.tracks:
        assert_that(track.total_tracks, equal_to(3), "track #{} total tracks".format(track.track_number))


def test_renumbers_tracks_when_removed():
    album = Album()
    tracks = [build.track(), build.track(), build.track()]
    for track in tracks:
        album.addTrack(track)

    album.removeTrack(tracks[0])

    assert_that(tracks[1].track_number, equal_to(1), 'track #1 number')
    assert_that(tracks[2].track_number, equal_to(2), 'track #2 number')

    for track in album.tracks:
        assert_that(track.total_tracks, equal_to(2), "track #{} total tracks left".format(track.track_number))


def test_signals_track_insertion_events():
    album = build.album()
    subscriber = Subscriber()
    tracks = [build.track(), build.track(), build.track()]

    album.track_inserted.subscribe(subscriber)
    for track in tracks:
        album.addTrack(track)

    for index, track in enumerate(tracks):
        assert_that(subscriber.events, has_item(event(index, track)), "track {0} insertion event".format(index))


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

        removed = album.tracks[1]
        album.removeTrack(removed)

        assert_that(album.tracks, has_length(2), 'remaining tracks')
        assert_that(album.tracks, is_not(has_item(has_property('track_title', 'Track 2'))), 'tracks')

    def testSupportsInsertingTracksAtASpecificPositions(self):
        album = build.album(tracks=[
            build.track(track_title='Track 1'),
            build.track(track_title='Track 2'),
            build.track(track_title='Track 3')])

        first = album.tracks[0]
        album.removeTrack(first)
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
        self.assertNotifiesListenerOnPropertyChange('guestPerformers', [('Musician', 'Instrument')])
        self.assertNotifiesListenerOnPropertyChange('label_name', 'Label')
        self.assertNotifiesListenerOnPropertyChange('recording_time', 'Recorded')
        self.assertNotifiesListenerOnPropertyChange('releaseTime', 'Released')
        self.assertNotifiesListenerOnPropertyChange('originalReleaseTime', 'Original Release')
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

        first = album.tracks[0]
        second = album.tracks[1]
        listener.should_receive('trackRemoved').with_args(second, 1).once()
        listener.should_receive('trackRemoved').with_args(first, 0).once()

        album.removeTrack(second)
        album.removeTrack(first)

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
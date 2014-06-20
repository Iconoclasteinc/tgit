# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, is_, contains, has_property, none,
                      has_length, has_item, is_not, match_equality as matching)
from hamcrest.library.collection.is_empty import empty
from flexmock import flexmock

from test.util import builders as build

from tgit.metadata import Image
from tgit.album import Album, AlbumListener
import tgit.tag as tags


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
        album.addTrack(build.track(trackTitle='Track 1'))
        album.addTrack(build.track(trackTitle='Track 2'))
        album.addTrack(build.track(trackTitle='Track 3'))

        assert_that(album.tracks, contains(
            has_property('trackTitle', 'Track 1'),
            has_property('trackTitle', 'Track 2'),
            has_property('trackTitle', 'Track 3')), 'track titles')

    def testSupportsRemovingTracks(self):
        album = build.album(tracks=[
            build.track(trackTitle='Track 1'),
            build.track(trackTitle='Track 2'),
            build.track(trackTitle='Track 3')])

        removed = album.tracks[1]
        album.removeTrack(removed)

        assert_that(album.tracks, has_length(2), 'remaining tracks')
        assert_that(album.tracks, is_not(has_item(has_property('trackTitle', 'Track 2'))), 'tracks')

    def testRemovesAssociationOfTrackToAlbum(self):
        track = build.track()
        album = build.album(tracks=[track])

        album.removeTrack(track)
        assert_that(track.album, none(), 'associated album')
        assert_that(track.number, none(), 'track number')

    def testSupportsInsertingTracksAtASpecificPositions(self):
        album = build.album(tracks=[
            build.track(trackTitle='Track 1'),
            build.track(trackTitle='Track 2'),
            build.track(trackTitle='Track 3')])

        first = album.tracks[0]
        album.removeTrack(first)
        album.insertTrack(first, 1)

        assert_that(album.tracks, contains(
            has_property('trackTitle', 'Track 2'),
            has_property('trackTitle', 'Track 1'),
            has_property('trackTitle', 'Track 3')), 'tracks')

    def testNumbersTracks(self):
        album = Album()
        album.addTrack(build.track(trackTitle='Track 1'))
        album.addTrack(build.track(trackTitle='Track 2'))
        album.addTrack(build.track(trackTitle='Track 3'))

        assert_that(album.tracks, contains(
            has_property('number', 1),
            has_property('number', 2),
            has_property('number', 3)), 'track numbers')

        album.removeTrack(album.tracks[1])

        assert_that(album.tracks, contains(
            has_property('number', 1),
            has_property('number', 2)), 'track numbers')

        album.insertTrack(build.track(trackTile='Track 4'), 0)

        assert_that(album.tracks, contains(
            has_property('number', 1),
            has_property('number', 2),
            has_property('number', 3)), 'track numbers')

    def testUsesFirstFrontCoverOrFirstImageAsMainCover(self):
        album = build.album()
        assert_that(album.mainCover, is_(None))
        album.addImage('image/jepg', 'back cover image')
        assert_that(album.mainCover, has_property('data', 'back cover image'))
        album.addFrontCover('image/jpeg', 'front cover image')
        assert_that(album.mainCover, has_property('data', 'front cover image'))

    def testHasInitiallyNoMetadataOrImages(self):
        album = Album()
        for tag in tags.ALBUM_TAGS:
            assert_that(getattr(album, tag), none(), tag)

        assert_that(album.images, empty(), 'images')

    def testCopiesAlbumMetadataOfInitialFirstTrack(self):
        originalRelease = build.album(releaseName='First Album',
                                      images=[build.image('image/jpeg', 'first-cover.jpg')])
        track = build.track()
        track.album = originalRelease

        album = build.album()
        album.addTrack(track)
        album.removeTrack(track)
        album.addTrack(build.track(releaseName='Second Album'))

        assert_that(album.releaseName, equal_to('First Album'), 'metadata')
        assert_that(album.images, contains(has_property('data', 'first-cover.jpg')), 'images')

    def testSignalsStateChangesToListener(self):
        self.assertNotifiesListenerOnPropertyChange('releaseName', 'Album')
        self.assertNotifiesListenerOnPropertyChange('leadPerformer', 'Artist')
        self.assertNotifiesListenerOnPropertyChange('guestPerformers', 'Band')
        self.assertNotifiesListenerOnPropertyChange('labelName', 'Label')
        self.assertNotifiesListenerOnPropertyChange('recordingTime', 'Recorded')
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

    def testSignalsStateChangeWhenFirstTrackInserted(self):
        album = Album()
        album.addAlbumListener(self.listenerExpectingNotification('releaseName', 'Album'))

        track = build.track(album=build.album(releaseName='Album'))
        album.addTrack(track)

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
        listener.should_receive('albumStateChanged') \
            .with_args(matching(has_property(prop, value))) \
            .once()
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
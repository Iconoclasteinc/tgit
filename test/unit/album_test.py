# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, is_, contains, has_property, has_properties,
                      has_length, has_item, is_not, has_entry, match_equality as matching)
from hamcrest.library.collection.is_empty import empty
from flexmock import flexmock

from test.util import builders as build

from tgit.metadata import Image
from tgit.album import Album, AlbumListener
import tgit.tags as tags


class AlbumTest(unittest.TestCase):
    def testIsInitiallyEmpty(self):
        assert_that(build.album().empty(), is_(True), 'emptiness')

    def testIsNoLongerEmptyWhenHoldingTracks(self):
        album = Album()
        album.addTrack(build.track())
        assert_that(album.empty(), is_(False), 'emptiness')

    def testHoldsAListOfTracksInOrder(self):
        album = Album()
        album.addTrack(build.track(trackTitle='Track 1'))
        album.addTrack(build.track(trackTitle='Track 2'))
        album.addTrack(build.track(trackTitle='Track 3'))

        assert_that(album.tracks, contains(
            has_property('trackTitle', 'Track 1'),
            has_property('trackTitle', 'Track 2'),
            has_property('trackTitle', 'Track 3')), 'tracks')

    def testSupportsRemovingTracks(self):
        album = build.album(tracks=[
            build.track(trackTitle='Track 1'),
            build.track(trackTitle='Track 2'),
            build.track(trackTitle='Track 3')])

        second = album.tracks[1]
        album.removeTrack(second)

        assert_that(album.tracks, has_length(2), 'remaining tracks')
        assert_that(album.tracks, is_not(has_item(has_property('trackTitle', 'Track 2'))),
                    'tracks')

    def testSupportsInsertingTracksAtASpecificPositions(self):
        album = build.album(tracks=[
            build.track(trackTitle='Track 1'),
            build.track(trackTitle='Track 2'),
            build.track(trackTitle='Track 3')])

        first = album.tracks[0]
        album.removeTrack(first)
        album.addTrack(first, 1)

        assert_that(album.tracks, contains(
            has_property('trackTitle', 'Track 2'),
            has_property('trackTitle', 'Track 1'),
            has_property('trackTitle', 'Track 3')), 'tracks')

    def testHasInitiallyNoMetadataOrImages(self):
        album = Album()
        for tag in tags.ALBUM_TAGS:
            assert_that(getattr(album, tag), empty(), tag)

        assert_that(album.images, empty(), 'images')

    def testDefaultsToMetadataOfInitialFirstTrack(self):
        album = Album()
        master = build.track(releaseName='First Album',
                             images=[build.image('image/jpeg', 'first-cover.jpg')])
        album.addTrack(master)
        album.removeTrack(master)
        album.addTrack(build.track(releaseName='Second Album'))

        assert_that(album.releaseName, equal_to('First Album'), 'metadata')
        assert_that(album.images, contains(has_property('data', 'first-cover.jpg')), 'images')

    def testTagsTracksWithAlbumMetadata(self):
        metadata = build.metadata(releaseName='Album',
                                  leadPerformer='Artist',
                                  guestPerformers=[('Guitar', 'Guitarist')],
                                  labelName='Label',
                                  upc='Barcode',
                                  catalogNumber='Reference',
                                  recordingStudios='Studios',
                                  producer='',
                                  mixer='',
                                  contributors=[('Mastering', 'Mastering Eng.')],
                                  recordingTime='2010-01-01',
                                  releaseTime='2010-02-15',
                                  originalReleaseTime='1980-06-05',
                                  images=[build.image('image/jpeg', 'front-cover.jpg',
                                                      desc='Front Cover')])

        album = build.album(tracks=[
            build.track(releaseName='Other album'),
            build.track(producer='Producer')]
        )
        for tag, value in metadata.items():
            setattr(album, tag, value)

        # add a track after modifying album metadata
        album.addTrack(build.track(mixer='Mixer'))

        album.tag()
        for track in album.tracks:
            self.assertHasMetadata(track, metadata)

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
        album.addTrack(middle, 1)

    def testSignalsStateChangeWhenFirstTrackInserted(self):
        album = Album()
        album.addAlbumListener(self.listenerExpectingNotification('releaseName', 'Album'))

        album.addTrack(build.track(releaseName='Album'))

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

    def assertHasMetadata(self, track, metadata):
        for tag, value in metadata.items():
            assert_that(track.metadata, has_entry(tag, value), 'track metadata')
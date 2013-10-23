# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, is_, contains, has_property, has_length, has_item, is_not,
                      has_entry, match_equality as matching)
from hamcrest.library.collection.is_empty import empty
from flexmock import flexmock

from tgit.metadata import Image
from tgit import album
from tgit.album import Album, AlbumListener

from test.util import builders


class AlbumTest(unittest.TestCase):

    def setUp(self):
        self.album = Album()

    def testIsInitiallyEmpty(self):
        assert_that(self.album.empty(), is_(True), 'empty')

    def testHoldsAListOfTracksInOrder(self):
        self.appendTrack(trackTitle='Track 1')
        self.appendTrack(trackTitle='Track 2')
        self.appendTrack(trackTitle='Track 3')

        assert_that(self.album.tracks, contains(
            has_property('trackTitle', 'Track 1'),
            has_property('trackTitle', 'Track 2'),
            has_property('trackTitle', 'Track 3')), 'tracks')

    def testIsNoLongerEmptyWhenHoldingTracks(self):
        self.appendTrack()
        assert_that(self.album.empty(), is_(False), 'empty')

    def testSupportsRemovingTracks(self):
        self.appendTrack(trackTitle='Track 1')
        second = self.appendTrack(trackTitle='Track 2')
        self.appendTrack(trackTitle='Track 3')

        self.album.removeTrack(second)

        assert_that(self.album.tracks, has_length(2), 'remaining tracks')
        assert_that(self.album.tracks, is_not(has_item(has_property('trackTitle', 'Track 2'))),
                    'tracks')

    def testSupportsInsertingTracksAtASpecificPosition(self):
        first = self.appendTrack(trackTitle='Track 1')
        self.appendTrack(trackTitle='Track 2')
        self.appendTrack(trackTitle='Track 3')

        self.album.removeTrack(first)
        self.album.addTrack(first, 1)

        assert_that(self.album.tracks, contains(
            has_property('trackTitle', 'Track 2'),
            has_property('trackTitle', 'Track 1'),
            has_property('trackTitle', 'Track 3')), 'tracks')

    def testHasInitiallyNoMetadata(self):
        assert_that(self.album.releaseName, empty(), 'release name')
        assert_that(self.album.leadPerformer, empty(), 'lead performer')
        assert_that(self.album.guestPerformers, empty(), 'guest performers')
        assert_that(self.album.labelName, empty(), 'label name')
        assert_that(self.album.recordingTime, empty(), 'recording time')
        assert_that(self.album.releaseTime, empty(), 'release time')
        assert_that(self.album.originalReleaseTime, empty(), 'original release name')
        assert_that(self.album.upc, empty(), 'upc')
        assert_that(self.album.images, empty(), 'images')

    def testTagsTracksWithAlbumMetadata(self):
        self.appendTrack(releaseName='Album A')
        self.appendTrack(releaseName='Album B')
        self.appendTrack(releaseName='Album C')

        self.album.releaseName = 'Album X'
        self.album.leadPerformer = 'Artist'
        self.album.guestPerformers = 'Band'
        self.album.labelName = 'Label'
        self.album.recordingTime = 'Recorded'
        self.album.releaseTime = 'Released'
        self.album.originalReleaseTime = 'Original Release'
        self.album.upc = 'Barcode'
        self.album.addFrontCover('image/jpeg', 'front-cover.jpg')

        self.album.tag()
        for track in self.album.tracks:
            self.assertHasAlbumMetadata(track)

    def testNewlyAddedTracksAreTaggedWithAlbumMetadataAsWell(self):
        self.album.releaseName = 'Album'

        track = self.appendTrack()
        self.album.tag()
        self.assertHasAlbumMetadata(track)

    def testRemovesTrackTagsAndImagesWhenAlbumMetadataIsEmpty(self):
        track = builders.track(
            releaseName='Album',
            leadPerformer='Artist',
            guestPerformers='Band',
            labelName='Label',
            recordingTime='2008-09-15',
            releaseTime='2009-01-01',
            originalReleaseTime='1998-03-05',
            upc='Code',
            images=[builders.image('image/jpeg', 'cover.jpg')]
        )

        self.album.addTrack(track)
        self.album.tag()

        for track in self.album.tracks:
            self.assertHasAlbumMetadata(track)

    def testAnnouncesTrackRemovalToListeners(self):
        listener = flexmock(AlbumListener())
        self.album.addAlbumListener(listener)

        first = self.appendTrack()
        second = self.appendTrack()
        listener.should_receive('trackRemoved').with_args(second, 1).once()
        listener.should_receive('trackRemoved').with_args(first, 0).once()

        self.album.removeTrack(second)
        self.album.removeTrack(first)

    def testAnnouncesTrackInsertionToListeners(self):
        listener = flexmock(AlbumListener())
        self.album.addAlbumListener(listener)

        first = builders.track()
        listener.should_receive('trackAdded').with_args(first, 0).once()
        self.album.addTrack(first)

        last = builders.track()
        listener.should_receive('trackAdded').with_args(last, 1).once()
        self.album.addTrack(last)

        middle = builders.track()
        listener.should_receive('trackAdded').with_args(middle, 1).once()
        self.album.addTrack(middle, 1)

    def testAnnouncesStateChangesToListener(self):
        self.assertNotifiesListenerOnPropertyChange('releaseName', 'Album')
        self.assertNotifiesListenerOnPropertyChange('leadPerformer', 'Artist')
        self.assertNotifiesListenerOnPropertyChange('guestPerformers', 'Band')
        self.assertNotifiesListenerOnPropertyChange('labelName', 'Label')
        self.assertNotifiesListenerOnPropertyChange('recordingTime', 'Recorded')
        self.assertNotifiesListenerOnPropertyChange('releaseTime', 'Released')
        self.assertNotifiesListenerOnPropertyChange('originalReleaseTime', 'Original Release')
        self.assertNotifiesListenerOnPropertyChange('upc', 'Barcode')
        self.assertNotifiesListenerOnImagesChange(Image('image/jpeg', 'front-cover.jpg'))

    def assertNotifiesListenerOnPropertyChange(self, property, value):
        album = Album()
        listener = flexmock(AlbumListener())
        album.addAlbumListener(listener)
        listener.should_receive('albumStateChanged') \
            .with_args(matching(has_property(property, value))) \
            .once()

        setattr(album, property, value)

    def assertNotifiesListenerOnImagesChange(self, *images):
        album = Album()
        listener = flexmock(AlbumListener())
        album.addAlbumListener(listener)
        listener.should_receive('albumStateChanged')\
            .with_args(matching(has_property('images', empty()))) \
            .once()
        album.removeImages()
        for image in images:
            listener.should_receive('albumStateChanged')\
                .with_args(matching(has_property('images', has_item(image)))).once()
            album.addImage(image.mime, image.data, image.type, image.desc)

    def appendTrack(self, **metadata):
        track = builders.track(**metadata)
        self.album.addTrack(track)
        return track

    def assertHasAlbumMetadata(self, track):
        metadata = track.metadata

        assert_that(metadata, has_entry(album.TITLE, self.album.releaseName),
                    album.TITLE)
        assert_that(metadata, has_entry(album.LEAD_PERFORMER, self.album.leadPerformer),
                    album.LEAD_PERFORMER)
        assert_that(metadata, has_entry(album.GUEST_PERFORMERS, self.album.guestPerformers),
                    album.GUEST_PERFORMERS)
        assert_that(metadata, has_entry(album.LABEL_NAME, self.album.labelName),
                    album.GUEST_PERFORMERS)
        assert_that(metadata, has_entry(album.RECORDING_TIME, self.album.recordingTime),
                    album.RECORDING_TIME)
        assert_that(metadata, has_entry(album.RELEASE_TIME, self.album.releaseTime),
                    album.RELEASE_TIME)
        assert_that(metadata, has_entry(album.ORIGINAL_RELEASE_TIME,
                                        self.album.originalReleaseTime),
                    album.ORIGINAL_RELEASE_TIME)
        assert_that(metadata, has_entry(album.UPC, self.album.upc),
                    album.UPC)
        assert_that(metadata.images, contains(*self.album.images),
                    'images')
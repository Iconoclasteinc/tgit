# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, is_, contains, has_property, has_length, has_item,
                      is_not, has_entry, match_equality as matching)
from hamcrest.library.collection.is_empty import empty
from flexmock import flexmock

from test.util import builders as build

from tgit.metadata import Image
from tgit.album import Album, AlbumListener
import tgit.album as tags


class AlbumTest(unittest.TestCase):

    def testIsInitiallyEmpty(self):
        assert_that(build.album().empty(), is_(True), 'empty')

    def testIsNoLongerEmptyWhenHoldingTracks(self):
        album = Album()
        album.addTrack(build.track())
        assert_that(album.empty(), is_(False), 'empty')

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

    def testHasInitiallyNoMetadata(self):
        album = Album()
        assert_that(album.releaseName, empty(), 'release name')
        assert_that(album.leadPerformer, empty(), 'lead performer')
        assert_that(album.guestPerformers, empty(), 'guest performers')
        assert_that(album.labelName, empty(), 'label name')
        assert_that(album.recordingTime, empty(), 'recording time')
        assert_that(album.releaseTime, empty(), 'release time')
        assert_that(album.originalReleaseTime, empty(), 'original release name')
        assert_that(album.upc, empty(), 'upc')
        assert_that(album.images, empty(), 'images')

    def testUsesFirstInsertedTrackAsMetadataReference(self):
        album = Album()
        master = build.track(trackTitle='Song',
                             releaseName='Album',
                             leadPerformer='Artist',
                             guestPerformers='Band',
                             labelName='Label',
                             recordingTime='Recorded',
                             releaseTime='Released',
                             originalReleaseTime='Original Release',
                             upc='Barcode',
                             images=[build.image('image/jpeg', 'front-cover.jpg')])
        album.addTrack(master)

        assert_that(album.releaseName, equal_to('Album'), 'release name')
        assert_that(album.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(album.guestPerformers, equal_to('Band'), 'guest performers')
        assert_that(album.labelName, equal_to('Label'), 'label name')
        assert_that(album.recordingTime, equal_to('Recorded'), 'recording time')
        assert_that(album.releaseTime, equal_to('Released'), 'release time')
        assert_that(album.originalReleaseTime, equal_to('Original Release'),
                    'original release name')
        assert_that(album.upc, equal_to('Barcode'), 'upc')
        assert_that(album.images, contains(*master.metadata().images), 'images')

    def testLeavesMetadataUnchangedWhenOriginalTrackRemoved(self):
        album = Album()
        master = build.track(releaseName='Album')
        album.addTrack(master)

        album.removeTrack(master)
        album.addTrack(build.track(releaseName='Another Album'))

        assert_that(album.releaseName, equal_to('Album'), 'release name')

    def testTagsTracksWithAlbumMetadata(self):
        album = build.album(tracks=[
            build.track(releaseName='Album A'),
            build.track(releaseName='Album B'),
            build.track(releaseName='Album C')])

        album.releaseName = 'Album X'
        album.leadPerformer = 'Artist'
        album.guestPerformers = 'Band'
        album.labelName = 'Label'
        album.recordingTime = 'Recorded'
        album.releaseTime = 'Released'
        album.originalReleaseTime = 'Original Release'
        album.upc = 'Barcode'
        album.addFrontCover('image/jpeg', 'front-cover.jpg')

        album.addTrack(build.track('Album D'))

        album.tag()
        for track in album.tracks:
            self.assertHasAlbumMetadata(track, album)

    def testRemovesTrackTagsAndImagesWhenAlbumMetadataIsEmpty(self):
        album = Album()
        album.addTrack(build.track())
        album.addTrack(build.track(
            releaseName='Album',
            leadPerformer='Artist',
            guestPerformers='Band',
            labelName='Label',
            recordingTime='2008-09-15',
            releaseTime='2009-01-01',
            originalReleaseTime='1998-03-05',
            upc='Code',
            images=[build.image('image/jpeg', 'cover.jpg')]
        ))
        album.tag()

        for track in album.tracks:
            self.assertHasAlbumMetadata(track, album)

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

    def assertHasAlbumMetadata(self, track, album):
        metadata = track.metadata(*tags.ALBUM_TAGS)

        assert_that(metadata, has_entry(tags.TITLE, album.releaseName),
                    tags.TITLE)
        assert_that(metadata, has_entry(tags.LEAD_PERFORMER, album.leadPerformer),
                    tags.LEAD_PERFORMER)
        assert_that(metadata, has_entry(tags.GUEST_PERFORMERS, album.guestPerformers),
                    tags.GUEST_PERFORMERS)
        assert_that(metadata, has_entry(tags.LABEL_NAME, album.labelName),
                    tags.GUEST_PERFORMERS)
        assert_that(metadata, has_entry(tags.RECORDING_TIME, album.recordingTime),
                    tags.RECORDING_TIME)
        assert_that(metadata, has_entry(tags.RELEASE_TIME, album.releaseTime),
                    tags.RELEASE_TIME)
        assert_that(metadata, has_entry(tags.ORIGINAL_RELEASE_TIME, album.originalReleaseTime),
                    tags.ORIGINAL_RELEASE_TIME)
        assert_that(metadata, has_entry(tags.UPC, album.upc),
                    tags.UPC)
        assert_that(metadata.images, contains(*album.images),
                    'images')
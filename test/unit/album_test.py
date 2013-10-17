# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, is_, contains, has_property, has_length, has_item, is_not,
                      equal_to, has_entry, has_properties)
from hamcrest.library.collection.is_empty import empty

from tgit import album
from tgit.album import Album
from tgit.track import Track

from test.util import doubles


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
        self.album.insertTrack(1, first)

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
        assert_that(self.album.frontCoverPicture, is_((None, None)), 'front cover picture')

    def testUsesMetadataOfFirstTrack(self):
        first = Track(doubles.audio(releaseName='Album A',
                                    leadPerformer='Artist',
                                    guestPerformers='Band',
                                    labelName='Label',
                                    recordingTime='Recorded',
                                    releaseTime='Released',
                                    originalReleaseTime='Original Release',
                                    upc='Barcode',
                                    pictures=[doubles.picture('image/jpeg', 'front-cover.jpg')]))
        self.album.appendTrack(first)
        other = Track(doubles.audio(releaseName='Album B'))
        self.album.appendTrack(other)

        assert_that(self.album.releaseName, equal_to('Album A'), 'release name')
        assert_that(self.album.leadPerformer, equal_to('Artist'), 'lead performer')
        assert_that(self.album.guestPerformers, equal_to('Band'), 'guest performers')
        assert_that(self.album.labelName, equal_to('Label'), 'label name')
        assert_that(self.album.recordingTime, equal_to('Recorded'), 'recording time')
        assert_that(self.album.releaseTime, equal_to('Released'), 'release time')
        assert_that(self.album.originalReleaseTime, equal_to('Original Release'),
                    'original release time')
        assert_that(self.album.upc, equal_to('Barcode'), 'upc')
        assert_that(self.album.frontCoverPicture, is_(('image/jpeg', 'front-cover.jpg')),
                    'front cover picture')

        self.album.removeTrack(first)
        assert_that(self.album.releaseName, equal_to('Album B'), 'updated release name')

    def testUpdatesAllTracksOnMetadataChange(self):
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
        self.album.frontCoverPicture = ('image/jpeg', 'front-cover.jpg')

        self.album.save()
        for track in self.album.tracks:
            self.assertHasAlbumMetadata(track)

    def appendTrack(self, **metadata):
        track = Track(doubles.audio(**metadata))
        self.album.appendTrack(track)
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
        assert_that(metadata.images, contains(self.sameImageAs(self.album.frontCoverPicture)))

    def sameImageAs(self, picture):
        return has_properties(mime=picture[0], data=picture[1])
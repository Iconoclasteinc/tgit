# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, match_equality as matching, has_property, all_of, has_entry, contains,
                      contains_inanyorder)
from flexmock import flexmock

from test.util import builders as build
from tgit.track import TrackListener, Track


class TrackTest(unittest.TestCase):
    def testDefinesMetadataTags(self):
        assert_that(tuple(Track.tags()),
                    contains_inanyorder('trackTitle', 'compilation', 'leadPerformer', 'versionInfo', 'featuredGuest', 'publisher',
                                        'lyricist', 'composer', 'isrc', 'labels', 'lyrics', 'language', 'tagger',
                                        'taggingTime', 'bitrate', 'duration'))

    def testUpdatesMetadataFromAlbumMetadata(self):
        track = build.track(filename='track.mp3', trackTitle='Track Title')
        album = build.album(releaseName='Album Title',
                            leadPerformer='Album Artist',
                            images=[build.image('image/jpeg', '<image data>')])
        track.album = album

        assert_that(track.metadata, all_of(
            has_entry('releaseName', 'Album Title'),
            has_entry('leadPerformer', 'Album Artist'),
            has_property('images', contains(has_property('data', '<image data>')))), 'updated track metadata')

    def testIgnoresLeadPerformerChangesWhenAlbumIsACompilation(self):
        track = build.track(leadPerformer='Track Artist')
        track.update(build.metadata(compilation=True, leadPerformer='Album Artist'))
        assert_that(track.metadata, has_entry('leadPerformer', 'Track Artist'), 'track lead performer')

        track.update(build.metadata(compilation=True))
        assert_that(track.metadata, has_entry('leadPerformer', 'Track Artist'), 'track lead performer')

    def testAnnouncesStateChangesToListeners(self):
        self.assertNotifiesListenerOnPropertyChange('trackTitle', 'Title')
        self.assertNotifiesListenerOnPropertyChange('versionInfo', 'Remix')
        self.assertNotifiesListenerOnPropertyChange('featuredGuest', 'Featuring')
        self.assertNotifiesListenerOnPropertyChange('isrc', 'Code')

    def testAnnouncesMetadataChangesToListeners(self):
        track = build.track()
        listener = flexmock(TrackListener())
        track.addTrackListener(listener)
        listener.should_receive('trackStateChanged').with_args(track).once()
        track.update(build.metadata(releaseName='Album Title'))

    def assertNotifiesListenerOnPropertyChange(self, prop, value):
        track = build.track()
        track.addTrackListener(self.listenerExpectingNotification(prop, value))
        setattr(track, prop, value)

    def listenerExpectingNotification(self, prop, value):
        listener = flexmock(TrackListener())
        listener.should_receive('trackStateChanged').with_args(matching(has_property(prop, value))).once()
        return listener

# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, match_equality as matching, has_property, all_of, has_entry, contains)
from flexmock import flexmock

from test.util import builders as build
from tgit import tags
from tgit.track import TrackListener


class TrackTest(unittest.TestCase):
    def testUpdatesMetadataFromAlbumMetadata(self):
        track = build.track(filename='track.mp3', trackTitle='Track Title')
        album = build.album(releaseName='Album Title',
                            images=[build.image('image/jpeg', '<image data>')])
        track.album = album

        assert_that(track.metadata, all_of(
            has_entry(tags.RELEASE_NAME, 'Album Title'),
            has_property('images', contains(has_property('data', '<image data>')))), 'updated track metadata')

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

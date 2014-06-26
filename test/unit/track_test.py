# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, match_equality as matching, has_property, contains_inanyorder)
from flexmock import flexmock

from test.util import builders as build
from tgit.track import TrackListener, Track


class TrackTest(unittest.TestCase):
    def testDefinesMetadataTags(self):
        assert_that(tuple(Track.tags()),
                    contains_inanyorder('trackTitle', 'leadPerformer', 'versionInfo', 'featuredGuest', 'publisher',
                                        'lyricist', 'composer', 'isrc', 'labels', 'lyrics', 'language', 'tagger',
                                        'taggingTime', 'bitrate', 'duration'))

    def testAnnouncesStateChangesToListeners(self):
        self.assertNotifiesListenerOnPropertyChange('trackTitle', 'Title')
        self.assertNotifiesListenerOnPropertyChange('versionInfo', 'Remix')
        self.assertNotifiesListenerOnPropertyChange('featuredGuest', 'Featuring')
        self.assertNotifiesListenerOnPropertyChange('isrc', 'Code')

    def assertNotifiesListenerOnPropertyChange(self, prop, value):
        track = build.track()
        track.addTrackListener(self.listenerExpectingNotification(prop, value))
        setattr(track, prop, value)

    def listenerExpectingNotification(self, prop, value):
        listener = flexmock(TrackListener())
        listener.should_receive('trackStateChanged').with_args(matching(has_property(prop, value))).once()
        return listener

# -*- coding: utf-8 -*-

import unittest
from hamcrest import (assert_that, equal_to, match_equality as matching, has_property)
from flexmock import flexmock

from test.util import builders as build

import tgit.tags as tags
from tgit.track import TrackListener


class TrackTest(unittest.TestCase):

    def testAnnouncesStateChangesToListener(self):
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
        listener.should_receive('trackStateChanged') \
            .with_args(matching(has_property(prop, value))) \
            .once()
        return listener

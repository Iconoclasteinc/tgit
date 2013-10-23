# -*- coding: utf-8 -*-

import unittest
from flexmock import flexmock

from tgit.announcer import Announcer


class Listener(object):
    def eventOccurred(self, event):
        pass


class AnnouncerTest(unittest.TestCase):
    listenerCount = 5

    def setUp(self):
        self.announcer = Announcer()
        self.event = 'event'

    def testAnnouncesToAllSubscribedListeners(self):
        self._listenersAreSubscribed()
        self.announcer.eventOccurred(self.event)

    def testStopsAnnouncingToUnregisteredListeners(self):
        shouldNotNotified = flexmock(Listener())
        self.announcer.addListener(shouldNotNotified)

        self._listenersAreSubscribed()
        self.announcer.removeListener(shouldNotNotified)

        shouldNotNotified.should_receive('eventOccurred').never()
        self.announcer.eventOccurred(self.event)

    def _listenersAreSubscribed(self):
        for i in xrange(self.listenerCount):
            self._subscribeListener()

    def _subscribeListener(self):
        listener = flexmock(Listener())
        listener.should_receive('eventOccurred').with_args(self.event).once()
        self.announcer.addListener(listener)

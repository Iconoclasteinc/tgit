# -*- coding: utf-8 -*-

import time
from hamcrest.core.selfdescribing import SelfDescribing
from hamcrest.core.string_description import StringDescription

from tests.cute.events import MainEventLoop

DEFAULT_POLL_DELAY = 100
DEFAULT_POLL_TIMEOUT = 5000


class Probe(SelfDescribing):
    def test(self):
        pass

    def isSatisfied(self):
        pass

    def describeTo(self, description):
        pass

    def describeFailureTo(self, description):
        pass

    def describe_to(self, description):
        self.describeTo(description)


class Timeout(object):
    def __init__(self, durationInMs):
        self._duration = durationInMs
        self._startTime = time.time()

    def hasExpired(self):
        return self.elapsedTime(time.time()) > self._duration

    def elapsedTime(self, now):
        return (now - self._startTime) * 1000


class Prober(object):
    def check(self, probe):
        pass


class PollingProber(Prober):
    def __init__(self, delay=DEFAULT_POLL_DELAY, timeout=DEFAULT_POLL_TIMEOUT):
        super(PollingProber, self).__init__()
        self._pollDelay = delay
        self._pollTimeout = timeout

    def check(self, probe):
        if not self._poll(probe):
            raise AssertionError(self._describeFailureOf(probe))

    def _describeFailureOf(self, probe):
        description = StringDescription()
        description.append_text("\nTried to look for...\n    ")
        probe.describeTo(description)
        description.append_text("\nbut...\n    ")
        probe.describeFailureTo(description)
        return str(description)

    def _poll(self, probe):
        timeout = Timeout(self._pollTimeout)

        while True:
            self._runProbe(probe)

            if probe.isSatisfied(): return True
            if timeout.hasExpired(): return False
            self._waitFor(self._pollDelay)

    def _runProbe(self, probe):
        pass

    def _waitFor(self, duration):
        pass


class EventProcessingProber(PollingProber):
    def __init__(self,
                 delayInMs=DEFAULT_POLL_DELAY,
                 timeoutInMs=DEFAULT_POLL_TIMEOUT):
        super(EventProcessingProber, self).__init__(delayInMs, timeoutInMs)

    def _runProbe(self, probe):
        probe.test()

    def _waitFor(self, ms):
        MainEventLoop.processEventsFor(ms)


# -*- coding: utf-8 -*-

import time
from PyQt4.QtTest import QTest
from hamcrest.core.selfdescribing import SelfDescribing
from hamcrest.core.string_description import StringDescription

DEFAULT_POLL_DELAY = 100
DEFAULT_POLL_TIMEOUT = 5000


class Probe(SelfDescribing):

    def test(self):
        pass

    def is_satisfied(self):
        pass

    def describe_failure_to(self, description):
        pass


class InContext(object):

    def __init__(self, context, probe):
        self._text = context
        self._probe = probe

    def describe_to(self, description):
        description.append_text(self._text) \
            .append_text(" ").append_description_of(self._probe)

    def __getattr__(self, attr):
        return getattr(self._probe, attr)


def in_context(text, probe):
    return InContext(text, probe)


class Timeout(object):

    def __init__(self, duration_in_ms):
        self._duration = duration_in_ms
        self._start_time = time.time()

    def has_expired(self):
        return self.elapsed_time(time.time()) > self._duration

    def elapsed_time(self, now):
        return (now - self._start_time) * 1000


class Prober(object):

    def check(self, probe):
        pass


class PollingProber(Prober):

    def __init__(self, delay=DEFAULT_POLL_DELAY, timeout=DEFAULT_POLL_TIMEOUT):
        self._poll_delay = delay
        self._poll_timeout = timeout

    def check(self, probe):
        if not self._poll(probe):
            raise AssertionError(self._describe_failure_of(probe))

    def _describe_failure_of(self, probe):
        description = StringDescription()
        description.append_text("\nTried to:\n    ")
        probe.describe_to(description)
        description.append_text("\nbut:\n    ")
        probe.describe_failure_to(description)
        return str(description)

    def _poll(self, probe):
        timeout = Timeout(self._poll_timeout)

        while True:
            self._run_probe(probe)

            if probe.is_satisfied(): return True
            if timeout.has_expired(): return False
            self._wait_for(self._poll_delay)

    def _run_probe(self, probe):
        pass

    def _wait_for(self, duration):
        pass


class EventProcessingProber(PollingProber):

    def __init__(self,
                 delay_in_ms=DEFAULT_POLL_DELAY,
                 timeout_in_ms=DEFAULT_POLL_TIMEOUT):
        super(EventProcessingProber, self).__init__(delay_in_ms, timeout_in_ms)

    def _run_probe(self, probe):
        probe.test()

    def _wait_for(self, duration):
        QTest.qWait(duration)


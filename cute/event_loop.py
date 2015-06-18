# -*- coding: utf-8 -*-
import time

from PyQt5.QtCore import QCoreApplication, QEventLoop


def in_seconds(ms):
    return ms / 1000


SLEEP_DELAY = 10


class Timeout:
    def __init__(self, duration_in_ms):
        self._duration = duration_in_ms
        self._start = time.time()

    def has_expired(self):
        return time.time() - self._start >= in_seconds(self._duration)


def process_events_for(ms):
    timeout = Timeout(ms)
    while not timeout.has_expired():
        process_pending_events(ms)
        QCoreApplication.sendPostedEvents()
        time.sleep(in_seconds(SLEEP_DELAY))


def process_pending_events(for_ms=0):
    QCoreApplication.processEvents(QEventLoop.AllEvents, for_ms)

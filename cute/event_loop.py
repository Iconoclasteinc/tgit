# -*- coding: utf-8 -*-

from PyQt5.QtTest import QTest


def process_events_for(ms):
    QTest.qWait(ms)

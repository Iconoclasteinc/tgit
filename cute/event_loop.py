# -*- coding: utf-8 -*-
from PyQt5.QtCore import QCoreApplication, QEventLoop
from PyQt5.QtTest import QTest


def process_events_for(ms):
    QTest.qWait(ms)


def process_pending_events(ms=0):
    QCoreApplication.processEvents(QEventLoop.AllEvents, ms)

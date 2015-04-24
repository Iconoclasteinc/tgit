# -*- coding: utf-8 -*-

from PyQt5.QtCore import QCoreApplication, QEventLoop
from PyQt5.QtTest import QTest


class MainEventLoop(object):
    @staticmethod
    def process_pending_events():
        QCoreApplication.processEvents(QEventLoop.AllEvents)

    @staticmethod
    def process_events_for(ms):
        QTest.qWait(ms)
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QCoreApplication, QEventLoop
from PyQt4.QtTest import QTest


class MainEventLoop(object):
    @staticmethod
    def processPendingEvents():
        QCoreApplication.processEvents(QEventLoop.AllEvents)

    @staticmethod
    def processEventsFor(ms):
        QTest.qWait(ms)

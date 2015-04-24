# -*- coding: utf-8 -*-

from PyQt5.QtCore import QCoreApplication, QEventLoop
from PyQt5.QtTest import QTest


class MainEventLoop(object):
    @staticmethod
    def processPendingEvents():
        QCoreApplication.processEvents(QEventLoop.AllEvents)

    @staticmethod
    def processEventsFor(ms):
        QTest.qWait(ms)
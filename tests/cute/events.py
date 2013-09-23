# -*- coding: utf-8 -*-

from PyQt4.Qt import QTest, QCoreApplication, QEventLoop


class MainEventLoop(object):
    @staticmethod
    def processPendingEvents():
        QCoreApplication.processEvents(QEventLoop.AllEvents)

    @staticmethod
    def processEventsFor(ms):
        QTest.qWait(ms)

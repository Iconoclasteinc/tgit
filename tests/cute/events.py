# -*- coding: utf-8 -*-

from PyQt4.Qt import QTest, QCoreApplication, QEventLoop


class MainEventLoop(object):

    @staticmethod
    def process_pending_events():
        QCoreApplication.processEvents(QEventLoop.AllEvents)

    @staticmethod
    def process_events_for(ms):
        QTest.qWait(ms)

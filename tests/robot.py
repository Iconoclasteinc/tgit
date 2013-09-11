# -*- coding: utf-8 -*-

from events import MainEventLoop

from PyQt4.Qt import (QCursor, QTest, QApplication, QPoint, Qt)


class Robot(object):
    LEFT_BUTTON = 0
    RIGHT_BUTTON = 1

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    def type(self, char):
        QTest.keyClick(self._widget_under_cursor(), char)

    def move_mouse(self, x, y):
        target = self._widget_at(x, y)
        QTest.mouseMove(target, target.mapFromGlobal(QPoint(x, y)))

    def press_mouse(self, button=LEFT_BUTTON):
        QTest.mousePress(self._widget_under_cursor(), self._mouse_button(button))

    def release_mouse(self, button=LEFT_BUTTON):
        QTest.mouseRelease(self._widget_under_cursor(), self._mouse_button(button))

    def delay(self, ms):
        MainEventLoop.process_events_for(ms)

    _MOUSE_BUTTONS = (Qt.LeftButton, Qt.RightButton)

    def _mouse_button(self, button):
        return self._MOUSE_BUTTONS[button]

    def _widget_under_cursor(self):
        return self._widget_at(QCursor.pos().x(), QCursor.pos().y())

    def _widget_at(self, x, y):
        return QApplication.widgetAt(x, y)

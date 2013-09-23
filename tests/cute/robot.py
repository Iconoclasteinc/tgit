# -*- coding: utf-8 -*-

from PyQt4.Qt import (QCursor, QTest, QApplication, QPoint, Qt)

from tests.cute.events import MainEventLoop


class Robot(object):
    LEFT_BUTTON = Qt.LeftButton
    RIGHT_BUTTON = Qt.RightButton

    def __init__(self):
        self._activeModifiers = Qt.NoModifier

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    def activateModifiers(self, mask):
        self._activeModifiers = self._activeModifiers | mask

    def deactivateModifiers(self, mask):
        self._activeModifiers = self._activeModifiers & ~mask

    def pressKey(self, key):
        QTest.keyPress(self._widgetUnderCursor(), key, self._activeModifiers)

    def releaseKey(self, key):
        QTest.keyRelease(self._widgetUnderCursor(), key, self._activeModifiers)

    def type(self, key):
        QTest.keyClick(self._widgetUnderCursor(), key, self._activeModifiers)

    # todo To make it easier to follow mouse movements in tests, investigate a smooth
    # movement (bezier curve?). Currently, mouse just jumps to destination
    def moveMouse(self, x, y):
        target = self._widgetAt(x, y)
        # By default QTest will move mouse at the center of the widget,
        # but we want a very specific position
        QTest.mouseMove(target, self._relativePosition(target, QPoint(x, y)))

    def pressMouse(self, button=LEFT_BUTTON):
        self._mouseActionAtCursorPosition(QTest.mousePress, button)

    def releaseMouse(self, button=LEFT_BUTTON):
        self._mouseActionAtCursorPosition(QTest.mouseRelease, button)

    def doubleClickMouse(self, button=LEFT_BUTTON):
        self._mouseActionAtCursorPosition(QTest.mouseDClick, button)

    def delay(self, ms):
        MainEventLoop.processEventsFor(ms)

    def _mouseActionAtCursorPosition(self, action, button):
        target = self._widgetUnderCursor()
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        clickLocation = self._cursorRelativePositionTo(target)
        action(target, button, self._activeModifiers, clickLocation)

    def _widgetUnderCursor(self):
        return self._widgetAt(QCursor.pos().x(), QCursor.pos().y())

    def _widgetAt(self, x, y):
        return QApplication.widgetAt(x, y)

    def _cursorRelativePositionTo(self, target):
        return self._relativePosition(target, QCursor.pos())

    def _relativePosition(self, target, point):
        return target.mapFromGlobal(point)

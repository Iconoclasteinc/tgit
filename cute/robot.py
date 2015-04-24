# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from .events import MainEventLoop


def widgetAt(x, y):
    widget = QApplication.widgetAt(x, y)
    if not widget:
        raise AssertionError('No widget at screen position (%d, %d)!'
                             ' Have you moved the mouse while running the tests?' % (x, y))
    return widget


def widgetUnderCursor():
    return widgetAt(QCursor.pos().x(), QCursor.pos().y())


def cursorRelativePositionTo(target):
    return relativePosition(target, QCursor.pos())


def relativePosition(origin, point):
    return origin.mapFromGlobal(point)


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
        QTest.keyPress(widgetUnderCursor(), key, self._activeModifiers)

    def releaseKey(self, key):
        QTest.keyRelease(widgetUnderCursor(), key, self._activeModifiers)

    def type(self, key):
        QTest.keyClick(widgetUnderCursor(), key, self._activeModifiers)

    def moveMouse(self, x, y):
        # By default QTest will move mouse at the center of the widget,
        # but we want a very specific position
        QTest.mouseMove(widgetAt(x, y), relativePosition(widgetAt(x, y), QPoint(x, y)))

    def pressMouse(self, button=LEFT_BUTTON):
        self._mouseActionAtCursorPosition(QTest.mousePress, button)

    def releaseMouse(self, button=LEFT_BUTTON):
        self._mouseActionAtCursorPosition(QTest.mouseRelease, button)

    def doubleClickMouse(self, button=LEFT_BUTTON):
        self._mouseActionAtCursorPosition(QTest.mouseDClick, button)

    def delay(self, ms):
        MainEventLoop.processEventsFor(ms)

    def _mouseActionAtCursorPosition(self, action, button):
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        action(widgetUnderCursor(), button, self._activeModifiers, cursorRelativePositionTo(widgetUnderCursor()))
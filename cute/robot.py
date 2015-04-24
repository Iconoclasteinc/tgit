# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from .events import MainEventLoop


def widget_at(x, y):
    widget = QApplication.widgetAt(x, y)
    if not widget:
        raise AssertionError('No widget at screen position (%d, %d)!'
                             ' Have you moved the mouse while running the tests?' % (x, y))
    return widget


def widget_under_cursor():
    return widget_at(QCursor.pos().x(), QCursor.pos().y())


def cursor_relative_position_to(target):
    return _compute_relative_position(target, QCursor.pos())


def _compute_relative_position(origin, point):
    return origin.mapFromGlobal(point)


class Robot(object):
    LEFT_BUTTON = Qt.LeftButton
    RIGHT_BUTTON = Qt.RightButton

    def __init__(self):
        self._active_modifiers = Qt.NoModifier

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    def activate_modifiers(self, mask):
        self._active_modifiers = self._active_modifiers | mask

    def deactivate_modifiers(self, mask):
        self._active_modifiers = self._active_modifiers & ~mask

    def press_key(self, key):
        QTest.keyPress(widget_under_cursor(), key, self._active_modifiers)

    def release_key(self, key):
        QTest.keyRelease(widget_under_cursor(), key, self._active_modifiers)

    def type(self, key):
        QTest.keyClick(widget_under_cursor(), key, self._active_modifiers)

    @staticmethod
    def move_mouse(x, y):
        # By default QTest will move mouse at the center of the widget,
        # but we want a very specific position
        QTest.mouseMove(widget_at(x, y), _compute_relative_position(widget_at(x, y), QPoint(x, y)))

    def press_mouse(self, button=LEFT_BUTTON):
        self._mouse_action_at_cursor_position(QTest.mousePress, button)

    def release_mouse(self, button=LEFT_BUTTON):
        self._mouse_action_at_cursor_position(QTest.mouseRelease, button)

    def double_click_mouse(self, button=LEFT_BUTTON):
        self._mouse_action_at_cursor_position(QTest.mouseDClick, button)

    @staticmethod
    def delay(ms):
        MainEventLoop.process_events_for(ms)

    def _mouse_action_at_cursor_position(self, action, button):
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        action(widget_under_cursor(), button, self._active_modifiers, cursor_relative_position_to(widget_under_cursor()))
# -*- coding: utf-8 -*-

from PyQt4.Qt import (QCursor, QTest, QApplication, QPoint, Qt)

from .events import MainEventLoop


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
        QTest.keyPress(self._widget_under_cursor(), key, self._active_modifiers)

    def release_key(self, key):
        QTest.keyRelease(self._widget_under_cursor(), key, self._active_modifiers)

    def type(self, key):
        QTest.keyClick(self._widget_under_cursor(), key, self._active_modifiers)

    def move_mouse(self, x, y):
        target = self._widget_at(x, y)
        # By default QTest will move mouse at the center of the widget,
        # but we want a very specific position
        QTest.mouseMove(target, self._relative_position_to(target, QPoint(x, y)))

    def press_mouse(self, button=LEFT_BUTTON):
        self._mouse_action_at_cursor_position(QTest.mousePress, button)

    def release_mouse(self, button=LEFT_BUTTON):
        self._mouse_action_at_cursor_position(QTest.mouseRelease, button)

    def double_click_mouse(self, button=LEFT_BUTTON):
        self._mouse_action_at_cursor_position(QTest.mouseDClick, button)

    def delay(self, ms):
        MainEventLoop.process_events_for(ms)

    def _mouse_action_at_cursor_position(self, action, button):
        target = self._widget_under_cursor()
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        click_location = self._cursor_relative_position_to(target)
        action(target, button, self._active_modifiers, click_location)

    def _widget_under_cursor(self):
        return self._widget_at(QCursor.pos().x(), QCursor.pos().y())

    def _widget_at(self, x, y):
        return QApplication.widgetAt(x, y)

    def _cursor_relative_position_to(self, target):
        return self._relative_position_to(target, QCursor.pos())

    def _relative_position_to(self, target, point):
        return target.mapFromGlobal(point)

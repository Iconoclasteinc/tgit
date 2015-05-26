# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from .events import MainEventLoop


def _widget_at(x, y):
    widget = QApplication.widgetAt(x, y)
    if not widget:
        raise AssertionError('No widget at screen position (%d, %d)!'
                             ' Have you moved the mouse while running the tests?' % (x, y))
    return widget


def _compute_relative_position(widget, x, y):
    return widget.mapFromGlobal(QPoint(x, y))


class Robot(object):
    def __init__(self):
        self._active_modifiers = Qt.NoModifier

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    @property
    def position(self):
        current_position = QCursor.pos()
        return current_position.x(), current_position.y()

    def activate_modifiers(self, mask):
        self._active_modifiers = self._active_modifiers | mask

    def deactivate_modifiers(self, mask):
        self._active_modifiers = self._active_modifiers & ~mask

    def press_key(self, key):
        QTest.keyPress(self._target(), key, self._active_modifiers)

    def release_key(self, key):
        QTest.keyRelease(self._target(), key, self._active_modifiers)

    def type(self, key):
        QTest.keyClick(self._target(), key, self._active_modifiers)

    @staticmethod
    def move_mouse(x, y):
        QCursor.setPos(x, y)

    def press_mouse(self, button):
        self._at_cursor_position(QTest.mousePress, button)

    def release_mouse(self, button):
        self._at_cursor_position(QTest.mouseRelease, button)

    def double_click_mouse(self, button):
        self._at_cursor_position(QTest.mouseDClick, button)

    @staticmethod
    def delay(ms):
        MainEventLoop.process_events_for(ms)

    def _at_cursor_position(self, mouse_action, button):
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        mouse_action(self._target(), button, self._active_modifiers, self._position_relative_to_target())

    def _target(self):
        return _widget_at(*self.position)

    def _position_relative_to_target(self):
        return _compute_relative_position(self._target(), *self.position)

# -*- coding: utf-8 -*-

from PyQt4.Qt import (QCursor, QTest, QApplication, QPoint, Qt)

from events import MainEventLoop


class Robot(object):
    NO_MODIFIER = 0

    LEFT_BUTTON = 0
    RIGHT_BUTTON = 1

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    def type(self, char):
        QTest.keyClick(self._widget_under_cursor(), char)

    def move_mouse(self, x, y):
        target = self._widget_at(x, y)
        # By default QTest will move mouse at the center of the widget,
        # but we want a very specific position
        QTest.mouseMove(target, self._relative_position_to(target, QPoint(x, y)))

    def press_mouse(self, button=LEFT_BUTTON, modifier=NO_MODIFIER):
        self._mouse_action_at_cursor_position(QTest.mousePress, button, modifier)

    def release_mouse(self, button=LEFT_BUTTON, modifier=NO_MODIFIER):
        self._mouse_action_at_cursor_position(QTest.mouseRelease, button, modifier)

    def double_click_mouse(self, button=LEFT_BUTTON, modifier=NO_MODIFIER):
        self._mouse_action_at_cursor_position(QTest.mouseDClick, button, modifier)

    def delay(self, ms):
        MainEventLoop.process_events_for(ms)

    def _mouse_action_at_cursor_position(self, action, button, modifier):
        target = self._widget_under_cursor()
        # By default QTest will operate mouse at the center of the widget,
        # but we want the action to occur at the current cursor position
        click_location = self._cursor_relative_position_to(target)
        action(target, self._buttons(button), self._modifiers(modifier), click_location)

    _MOUSE_BUTTONS = (Qt.LeftButton, Qt.RightButton)

    def _buttons(self, button):
        return self._MOUSE_BUTTONS[button]

    def _modifiers(self, modifier):
        return Qt.NoModifier

    def _widget_under_cursor(self):
        return self._widget_at(QCursor.pos().x(), QCursor.pos().y())

    def _widget_at(self, x, y):
        return QApplication.widgetAt(x, y)

    def _cursor_relative_position_to(self, target):
        return self._relative_position_to(target, QCursor.pos())

    def _relative_position_to(self, target, point):
        return target.mapFromGlobal(point)

# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt, QTest


class Robot(object):
    LEFT_MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, pause_in_ms=50):
        super(Robot, self).__init__()
        self._pause = pause_in_ms

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    def move_mouse_to(self, widget):
        QTest.mouseMove(widget)

    def click_mouse_on(self, widget, button=LEFT_MOUSE_BUTTON):
        self.press_mouse_on(widget, button)
        self.release_mouse_on(widget, button)

    def press_mouse_on(self, widget, button=LEFT_MOUSE_BUTTON):
        QTest.mousePress(widget, button, delay=self._pause)

    def release_mouse_on(self, widget, button=LEFT_MOUSE_BUTTON):
        QTest.mouseRelease(widget, button, delay=self._pause)

    def wait_for(self, ms):
        QTest.qWait(ms)

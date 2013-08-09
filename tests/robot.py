# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt, QTest


class Robot(object):
    LEFT_BUTTON = Qt.LeftButton

    def __init__(self, delay_in_ms=100):
        super(Robot, self).__init__()
        self._delay = delay_in_ms

    def click_on(self, widget, button=LEFT_BUTTON):
        self.move_mouse_to(widget)
        self.wait(self._delay)
        self.mouse_click(widget, button)

    def move_mouse_to(self, widget):
        QTest.mouseMove(widget)

    def mouse_click(self, widget, button):
        self.mouse_press(widget, button)
        self.wait(self._delay)
        self.mouse_release(widget, button)

    def mouse_press(self, widget, button):
        QTest.mousePress(widget, button)

    def mouse_release(self, widget, button):
        QTest.mouseRelease(widget, button)

    def wait(self, ms):
        QTest.qWait(ms)

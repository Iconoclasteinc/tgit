# -*- coding: utf-8 -*-

from PyQt4.Qt import QTest
from autopy import mouse


class Robot(object):
    LEFT_MOUSE_BUTTON = mouse.LEFT_BUTTON

    def __init__(self):
        super(Robot, self).__init__()

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

    def move_mouse(self, point):
        mouse.smooth_move(point.x(), point.y())

    def press_mouse(self, button=LEFT_MOUSE_BUTTON):
        mouse.toggle(True, button)

    def release_mouse(self, button=LEFT_MOUSE_BUTTON):
        mouse.toggle(False, button)

    def delay(self, ms):
        # Process Qt evens while waiting
        QTest.qWait(ms)

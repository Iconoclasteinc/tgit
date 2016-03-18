# -*- coding: utf-8 -*-
import pyautogui

from . import event_loop, platforms
from .gestures import Automaton


# We need to make a little pause on OS X otherwise keys and clicks might not
# be detected
MINIMUM_PAUSE = 0.01 if platforms.mac else 0


class Animatron(Automaton):
    """
    A robotic automaton that emulates a human using the keyboard and mouse.

    It is more realistic although slower than the Robot.
    """
    def __init__(self, pause=MINIMUM_PAUSE):
        pyautogui.PAUSE = pause

    @property
    def mouse_position(self):
        return pyautogui.position()

    def press_key(self, key):
        pyautogui.keyDown(key)
        event_loop.process_pending_events()

    def release_key(self, key):
        pyautogui.keyUp(key)
        event_loop.process_pending_events()

    def type(self, key):
        pyautogui.press(key)
        event_loop.process_pending_events()

    def move_mouse(self, x, y):
        # OS X requires a special drag event, but it seems Qt does not need it.
        # Maybe it recognizes the drag event by itself, so there's no need to do anything special to trigger drag.
        pyautogui.moveTo(x, y)
        event_loop.process_pending_events()

    def press_mouse(self, button):
        pyautogui.mouseDown(button=button)
        event_loop.process_pending_events()

    def release_mouse(self, button):
        pyautogui.mouseUp(button=button)
        event_loop.process_pending_events()

    def delay(self, ms):
        event_loop.process_events_for(ms)

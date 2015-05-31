# -*- coding: utf-8 -*-
import pyautogui

from . import event_loop
from .gestures import Automaton


class Animatron(Automaton):
    """
    A robotic automaton that emulates a human using the keyboard and mouse.

    It is more realistic although slower than the Robot.
    """
    def __init__(self, pause=0):
        pyautogui.PAUSE = pause

    def perform(self, *gestures):
        for gesture in gestures:
            gesture(self)

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

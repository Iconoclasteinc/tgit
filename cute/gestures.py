# -*- coding: utf-8 -*-
import sys
from .keys import *

mac = sys.platform == "darwin"
windows = sys.platform == "win32"

ONE_SECOND_IN_MS = 60000
AVERAGE_WORD_LENGTH = 5  # precisely 5.1 in english
MEDIUM_TYPING_SPEED = 240  # in wpm
FAST_TYPING_SPEED = 480  # in wpm
SUPER_FAST_TYPING_SPEED = 960  # in wpm

MOUSE_CLICK_DELAY = 10  # in ms
MOUSE_DOUBLE_CLICK_DELAY = 50  # in ms
MIN_TIME_TO_AVOID_DOUBLE_CLICK = 500  # in ms

LEFT_BUTTON = 'left'
RIGHT_BUTTON = 'right'


class GesturePerformer:
    """A mixin for performing human gestures"""
    def perform(self, *gestures):
        pass


class Automaton(GesturePerformer):
    """An automaton performs human gestures by manipulating keyboard and mouse"""
    def mouse_position(self):
        pass

    def press_key(self, key):
        pass

    def release_key(self, key):
        pass

    def type(self, key):
        pass

    def move_mouse(self, x, y):
        pass

    def press_mouse(self, button):
        pass

    def release_mouse(self, button):
        pass

    def delay(self, ms):
        pass


def sequence(*gestures):
    return lambda automaton: [gesture(automaton) for gesture in gestures]


def key_press(key):
    return lambda automaton: automaton.press_key(key)


def key_release(key):
    return lambda automaton: automaton.release_key(key)


def holding_modifier_key(key, gesture):
    return sequence(key_press(key), gesture, key_release(key))


def holding_control(gesture):
    return holding_modifier_key(COMMAND if mac else CONTROL, gesture)


def type_key(key):
    return lambda automaton: automaton.type(key)


def type_text(text, typing_speed=SUPER_FAST_TYPING_SPEED):
    return sequence(*[_at_speed(typing_speed, type_key(c)) for c in text])


def mouse_move(pos):
    return lambda automaton: automaton.move_mouse(pos.x(), pos.y())


def mouse_press(button=LEFT_BUTTON):
    return lambda automaton: automaton.press_mouse(button)


def mouse_release(button=LEFT_BUTTON):
    return lambda automaton: automaton.release_mouse(button)


def mouse_click(button=LEFT_BUTTON):
    return sequence(mouse_press(button), pause(MOUSE_CLICK_DELAY), mouse_release(button))


def mouse_click_at(pos, button=LEFT_BUTTON):
    return sequence(mouse_move(pos), mouse_click(button))


def mouse_double_click(button=LEFT_BUTTON):
    return sequence(mouse_click(button), pause(MOUSE_DOUBLE_CLICK_DELAY), mouse_click(button))


def avoid_double_click():
    return pause(MIN_TIME_TO_AVOID_DOUBLE_CLICK)


def mouse_multi_click(button=LEFT_BUTTON):
    return holding_modifier_key(COMMAND if mac else CONTROL, mouse_click(button))


def mouse_multi_click_at(pos, button=LEFT_BUTTON):
    return holding_control(mouse_click_at(pos, button))


def select_all():
    return holding_modifier_key(COMMAND if mac else CONTROL, type_key('a'))


def enter():
    return type_key(RETURN)


def delete_previous():
    return type_key(BACKSPACE)


def unselect():
    return type_key(ESCAPE)


def close():
    return holding_modifier_key(CONTROL, type_key(F4 if windows else 'w'))


def pause(ms):
    return lambda automaton: automaton.delay(ms)


def _at_speed(wpm, typing_gesture):
    return sequence(typing_gesture, pause(_keystroke_delay(wpm)))


def _keystroke_delay(wpm):
    return ONE_SECOND_IN_MS / _keystrokes_per_minute(wpm)


def _keystrokes_per_minute(wpm):
    return wpm * AVERAGE_WORD_LENGTH

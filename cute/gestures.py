# -*- coding: utf-8 -*-
import sys
from cute.keys import *

mac = sys.platform == "darwin"
windows = sys.platform == "win32"

ONE_SECOND_IN_MS = 60000
AVERAGE_WORD_LENGTH = 5  # precisely 5.1 in english
MEDIUM_TYPING_SPEED = 240  # in wpm
FAST_TYPING_SPEED = 480  # in wpm
SUPER_FAST_TYPING_SPEED = 960  # in wpm

MOUSE_CLICK_DELAY = 10  # in ms

LEFT_BUTTON = 'left'
RIGHT_BUTTON = 'right'


def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


def key_press(key):
    return lambda robot: robot.press_key(key)


def key_release(key):
    return lambda robot: robot.release_key(key)


def holding_modifier_key(key, gesture):
    return sequence(key_press(key), gesture, key_release(key))


def holding_control(gesture):
    return holding_modifier_key(COMMAND if mac else CONTROL, gesture)


def type_key(key):
    return lambda robot: robot.type(key)


def type_text(text, typing_speed=SUPER_FAST_TYPING_SPEED):
    return sequence(*[_at_speed(typing_speed, type_key(c)) for c in text])


def mouse_move(pos):
    return lambda robot: robot.move_mouse(pos.x(), pos.y())


def mouse_press(button=LEFT_BUTTON):
    return lambda robot: robot.press_mouse(button)


def mouse_release(button=LEFT_BUTTON):
    return lambda robot: robot.release_mouse(button)


def mouse_click(button=LEFT_BUTTON):
    return sequence(mouse_press(button), pause(MOUSE_CLICK_DELAY), mouse_release(button))


def mouse_click_at(pos, button=LEFT_BUTTON):
    return sequence(mouse_move(pos), mouse_click(button))


def mouse_double_click(button=LEFT_BUTTON):
    # Apparently Qt uses a special DClickEvent which is not the same as 2 clicks,
    # so the following fails:
    # return sequence(mouse_click(), pause(MOUSE_DOUBLE_CLICK_DELAY), mouse_click())
    # We need a double click action from the robot itself
    return lambda robot: robot.double_click_mouse(button)


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
    return lambda robot: robot.delay(ms)


def _at_speed(wpm, typing_gesture):
    return sequence(typing_gesture, pause(_keystroke_delay(wpm)))


def _keystroke_delay(wpm):
    return ONE_SECOND_IN_MS / _keystrokes_per_minute(wpm)


def _keystrokes_per_minute(wpm):
    return wpm * AVERAGE_WORD_LENGTH



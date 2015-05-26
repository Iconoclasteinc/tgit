# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt

ONE_SECOND_IN_MS = 60000
AVERAGE_WORD_LENGTH = 5  # precisely 5.1 in english
MEDIUM_TYPING_SPEED = 240  # in wpm
FAST_TYPING_SPEED = 480  # in wpm
SUPER_FAST_TYPING_SPEED = 960  # in wpm
MOUSE_MOVE_DELAY = 10 # in ms
MOUSE_CLICK_DELAY = 20  # in ms

LEFT_BUTTON = Qt.LeftButton
RIGHT_BUTTON = Qt.RightButton

def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


def set_modifiers(modifiers):
    return lambda robot: robot.activate_modifiers(modifiers)


def unset_modifiers(modifiers):
    return lambda robot: robot.deactivate_modifiers(modifiers)


def with_modifiers(modifiers, gesture):
    return sequence(set_modifiers(modifiers), gesture, unset_modifiers(modifiers))


def type_text(text):
    return sequence(*[at_speed(SUPER_FAST_TYPING_SPEED, type_key(c)) for c in text])


def type_key(key):
    return lambda robot: robot.type(key)


def press_key(key):
    return lambda robot: robot.press_key(key)


def release_key(key):
    return lambda robot: robot.release_key(key)


def at_speed(wpm, typing_gesture):
    return sequence(typing_gesture, pause(_keystroke_delay(wpm)))


def _keystroke_delay(typing_speed_in_wpm):
    return ONE_SECOND_IN_MS / _keystrokes_per_minute(typing_speed_in_wpm)


def _keystrokes_per_minute(wpm):
    return wpm * AVERAGE_WORD_LENGTH


def click_at(point):
    return sequence(mouse_move(point), mouse_click())


def mouse_move(point):
    return sequence(lambda robot: robot.move_mouse(point.x(), point.y()), pause(MOUSE_MOVE_DELAY))


def mouse_click(button=LEFT_BUTTON):
    return sequence(mouse_press(button), pause(MOUSE_CLICK_DELAY), mouse_release(button))


def mouse_press(button=LEFT_BUTTON):
    return lambda robot: robot.press_mouse(button)


def mouse_release(button=LEFT_BUTTON):
    return lambda robot: robot.release_mouse(button)


def mouse_double_click(button=LEFT_BUTTON):
    # Apparently Qt uses a special DClickEvent which is not the same as 2 clicks,
    # so the following fails:
    # return sequence(mouse_click(), pause(MOUSE_DOUBLE_CLICK_DELAY), mouse_click())
    # We need a double click action from the robot itself
    return lambda robot: robot.double_click_mouse(button)


def pause(ms):
    return lambda robot: robot.delay(ms)

# -*- coding: utf-8 -*-

from .robot import Robot

ONE_SECOND_IN_MS = 60000
AVERAGE_WORD_LENGTH = 5         # precisely 5.1 in english
MEDIUM_TYPING_SPEED = 240       # in wpm
FAST_TYPING_SPEED = 480         # in wpm
MOUSE_CLICK_DELAY = 50          # in ms


def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


def type_text(text):
    return sequence(*[at_speed(FAST_TYPING_SPEED, type_key(c)) for c in text])


def type_key(key):
    return lambda robot: robot.type(key)


def at_speed(wpm, typing_gesture):
    return sequence(typing_gesture, pause(_keystroke_delay(wpm)))


def _keystroke_delay(typing_speed_in_wpm):
    return ONE_SECOND_IN_MS / _keystrokes_per_minute(typing_speed_in_wpm)


def _keystrokes_per_minute(wpm):
    return wpm * AVERAGE_WORD_LENGTH


def click_on(point):
    return sequence(mouse_move(point), mouse_click())


def mouse_move(point):
    return lambda robot: robot.move_mouse(point.x(), point.y())


def mouse_click():
    return sequence(mouse_press(), pause(MOUSE_CLICK_DELAY), mouse_release())


def mouse_press():
    return lambda robot: robot.press_mouse(Robot.LEFT_BUTTON)


def mouse_release():
    return lambda robot: robot.release_mouse(Robot.LEFT_BUTTON)


def mouse_double_click():
    # Apparently Qt uses a special DClickEvent which is not the same as 2 clicks,
    # so the following fails:
    # return sequence(mouse_click(), pause(MOUSE_DOUBLE_CLICK_DELAY), mouse_click())
    # We need a double click action from the robot itself
    return lambda robot: robot.double_click_mouse()


def pause(ms):
    return lambda robot: robot.delay(ms)

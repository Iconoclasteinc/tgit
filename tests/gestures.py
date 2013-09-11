# -*- coding: utf-8 -*-

from robot import Robot

ONE_SECOND_IN_MS = 60000
AVERAGE_WORD_LENGTH = 5         # precisely 5.1 in english
MEDIUM_TYPING_SPEED = 240       # in wpm
FAST_TYPING_SPEED = 480         # in wpm
MID_MOUSE_CLICK_DELAY = 50


def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


def type_text(text):
    return sequence(*[at_speed(FAST_TYPING_SPEED, type_char(c)) for c in text])


def type_char(char):
    return lambda robot: robot.type(char)


def at_speed(wpm, typing_gesture):
    return sequence(typing_gesture, pause(_keystroke_delay(wpm)))


def _keystroke_delay(typing_speed_in_wpm):
    return ONE_SECOND_IN_MS / _keystrokes_per_minute(typing_speed_in_wpm)


def _keystrokes_per_minute(wpm):
    return wpm * AVERAGE_WORD_LENGTH


def click_on(point):
    return sequence(mouse_move(point), mouse_click())


def mouse_move(point):
    return lambda robot: robot.move_mouse(point)


def mouse_click():
    return sequence(mouse_press(), pause(MID_MOUSE_CLICK_DELAY), mouse_release())


def mouse_press():
    return lambda robot: robot.press_mouse(Robot.LEFT_MOUSE_BUTTON)


def mouse_release():
    return lambda robot: robot.release_mouse(Robot.LEFT_MOUSE_BUTTON)


def pause(ms):
    return lambda robot: robot.delay(ms)

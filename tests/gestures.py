# -*- coding: utf-8 -*-

from robot import Robot


MID_MOUSE_CLICK_DELAY = 50


def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


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

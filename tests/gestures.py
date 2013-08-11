# -*- coding: utf-8 -*-

from robot import Robot


def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


def click_on(widget):
    return sequence(mouse_move(widget), mouse_click(widget))


def mouse_move(widget):
    return lambda robot: robot.move_mouse_to(widget)


def mouse_click(widget):
    return lambda robot: robot.click_mouse_on(widget, Robot.LEFT_MOUSE_BUTTON)


def delay(ms):
    return lambda robot: robot.wait_for(ms)

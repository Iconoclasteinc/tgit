# -*- coding: utf-8 -*-

from test.cute4.robot import Robot

ONE_SECOND_IN_MS = 60000
AVERAGE_WORD_LENGTH = 5         # precisely 5.1 in english
MEDIUM_TYPING_SPEED = 240       # in wpm
FAST_TYPING_SPEED = 480         # in wpm
SUPER_FAST_TYPING_SPEED = 960   # in wpm
MOUSE_CLICK_DELAY = 20          # in ms


def sequence(*gestures):
    return lambda robot: [gesture(robot) for gesture in gestures]


def setModifiers(modifiers):
    return lambda robot: robot.activateModifiers(modifiers)


def unsetModifiers(modifiers):
    return lambda robot: robot.deactivateModifiers(modifiers)


def withModifiers(modifiers, gesture):
    return sequence(setModifiers(modifiers), gesture, unsetModifiers(modifiers))


def typeText(text):
    return sequence(*[atSpeed(SUPER_FAST_TYPING_SPEED, typeKey(c)) for c in text])


def typeKey(key):
    return lambda robot: robot.type(key)


def pressKey(key):
    return lambda robot: robot.pressKey(key)


def releaseKey(key):
    return lambda robot: robot.releaseKey(key)


def atSpeed(wpm, typing_gesture):
    return sequence(typing_gesture, pause(_keystrokeDelay(wpm)))


def _keystrokeDelay(typing_speed_in_wpm):
    return ONE_SECOND_IN_MS / _keystrokesPerMinute(typing_speed_in_wpm)


def _keystrokesPerMinute(wpm):
    return wpm * AVERAGE_WORD_LENGTH


def clickAt(point):
    return sequence(mouseMove(point), mouseClick())


def mouseMove(point):
    return lambda robot: robot.moveMouse(point.x(), point.y())


def mouseClick():
    return sequence(mousePress(), pause(MOUSE_CLICK_DELAY), mouseRelease())


def mousePress():
    return lambda robot: robot.pressMouse(Robot.LEFT_BUTTON)


def mouseRelease():
    return lambda robot: robot.releaseMouse(Robot.LEFT_BUTTON)


def mouseDoubleClick():
    # Apparently Qt uses a special DClickEvent which is not the same as 2 clicks,
    # so the following fails:
    # return sequence(mouse_click(), pause(MOUSE_DOUBLE_CLICK_DELAY), mouse_click())
    # We need a double click action from the robot itself
    return lambda robot: robot.doubleClickMouse()


def pause(ms):
    return lambda robot: robot.delay(ms)

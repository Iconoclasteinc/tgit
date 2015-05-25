# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt

from . import gestures
import sys

windows = sys.platform == "win32"

SELECT_ALL = gestures.with_modifiers(Qt.ControlModifier, gestures.type_key(Qt.Key_A))
DELETE_PREVIOUS = gestures.type_key(Qt.Key_Backspace)
UNSELECT = gestures.type_key(Qt.Key_Escape)
ENTER = gestures.type_key(Qt.Key_Enter)
CLOSE = gestures.with_modifiers(Qt.ControlModifier, gestures.type_key(Qt.Key_F4 if windows else Qt.Key_W))
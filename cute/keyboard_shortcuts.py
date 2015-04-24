# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt

from . import gestures


SELECT_ALL = gestures.with_modifiers(Qt.ControlModifier, gestures.type_key(Qt.Key_A))
DELETE_PREVIOUS = gestures.type_key(Qt.Key_Backspace)
UNSELECT = gestures.type_key(Qt.Key_Escape)
ENTER = gestures.type_key(Qt.Key_Enter)
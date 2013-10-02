# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt

from tests.cute import gestures


SelectAll = gestures.withModifiers(Qt.ControlModifier, gestures.typeKey(Qt.Key_A))
DeletePrevious = gestures.typeKey(Qt.Key_Backspace)
Unselect = gestures.typeKey(Qt.Key_Escape)

# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt

from . import gestures


SelectAll = gestures.withModifiers(Qt.ControlModifier, gestures.typeKey(Qt.Key_A))
DeletePrevious = gestures.typeKey(Qt.Key_Backspace)
Unselect = gestures.typeKey(Qt.Key_Escape)
Enter = gestures.typeKey(Qt.Key_Enter)
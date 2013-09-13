# -*- coding: utf-8 -*-

from PyQt4.Qt import Qt

from . import gestures


Select_All = gestures.with_modifiers(Qt.ControlModifier, gestures.type_key(Qt.Key_A))
Delete_Previous = gestures.type_key(Qt.Key_Backspace)
Unselect = gestures.type_key(Qt.Key_Escape)

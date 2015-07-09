# -*- coding: utf-8 -*-
#
# TGiT, Music Tagger for Professionals
# Copyright (C) 2013 Iconoclaste Musique Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
from PyQt5.QtCore import QObject, Qt, QEvent


class MovableSectionsCursor(QObject):
    REGULAR_CURSOR = Qt.ArrowCursor
    DRAGGABLE_CURSOR = Qt.OpenHandCursor
    DRAGGING_CURSOR = Qt.ClosedHandCursor

    _mouse_pressed = False

    @classmethod
    def install(cls, header):
        cursor = cls(header)
        header.setMouseTracking(True)
        header.viewport().installEventFilter(cursor)
        return cursor

    def __init__(self, header):
        super().__init__()
        self._header = header

    def _within_bounds(self, pos):
        return 0 < pos.y() <= self._header.length()

    def eventFilter(self, target, event):
        item_view = self._header.parent()

        if event.type() == QEvent.Leave:
            item_view.setCursor(self.REGULAR_CURSOR)
        if event.type() == QEvent.MouseButtonPress:
            self._mouse_pressed = True
            item_view.setCursor(self.DRAGGING_CURSOR)
        if event.type() == QEvent.MouseButtonRelease:
            self._mouse_pressed = False
            item_view.setCursor(self.DRAGGABLE_CURSOR if self._within_bounds(event.pos()) else
                             self.REGULAR_CURSOR)
        if event.type() == QEvent.MouseMove:
            item_view.setCursor(self.DRAGGING_CURSOR if self._mouse_pressed else
                             self.DRAGGABLE_CURSOR if self._within_bounds(event.pos()) else
                             self.REGULAR_CURSOR)

        return super().eventFilter(target, event)

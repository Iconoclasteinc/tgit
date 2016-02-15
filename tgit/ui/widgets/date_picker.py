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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QIcon

from PyQt5.QtWidgets import QDateEdit, QWidget


class DatePicker(QDateEdit):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCalendarPopup(True)
        self._style()

    def _style(self):
        calendar = self.calendarWidget()
        navbar = calendar.findChild(QWidget, "qt_calendar_navigationbar")
        palette = calendar.palette()
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Highlight, Qt.white)
        navbar.setPalette(palette)
        left_arrow = calendar.findChild(QWidget, "qt_calendar_prevmonth")
        left_arrow.setIcon(QIcon(":/calendar-previous"))
        right_arrow = calendar.findChild(QWidget, "qt_calendar_nextmonth")
        right_arrow.setIcon(QIcon(":/calendar-next"))
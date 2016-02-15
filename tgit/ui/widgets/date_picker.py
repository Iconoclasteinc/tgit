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
        self._style_navigation_bar(self.calendarWidget())
        self._style_month_menu(self.calendarWidget())
        self._style_year_edit(self.calendarWidget())
        self._style_navigation_buttons(self.calendarWidget())

    def _style_navigation_bar(self, calendar):
        navbar = calendar.findChild(QWidget, "qt_calendar_navigationbar")
        palette = calendar.palette()
        palette.setColor(QPalette.Highlight, Qt.white)
        navbar.setPalette(palette)

    def _style_month_menu(self, calendar):
        month_menu = calendar.findChild(QWidget, "qt_calendar_monthbutton")
        palette = calendar.palette()
        palette.setColor(QPalette.HighlightedText, palette.color(QPalette.ButtonText))
        month_menu.setPalette(palette)

    def _style_year_edit(self, calendar):
        year_edit = calendar.findChild(QWidget, "qt_calendar_yearbutton")
        palette = calendar.palette()
        palette.setColor(QPalette.HighlightedText, palette.color(QPalette.ButtonText))
        year_edit.setPalette(palette)

    def _style_navigation_buttons(self, calendar):
        left_arrow = calendar.findChild(QWidget, "qt_calendar_prevmonth")
        left_arrow.setIcon(QIcon(":/calendar-previous"))
        right_arrow = calendar.findChild(QWidget, "qt_calendar_nextmonth")
        right_arrow.setIcon(QIcon(":/calendar-next"))

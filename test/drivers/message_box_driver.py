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

from PyQt5.QtWidgets import QMessageBox
from hamcrest import contains_string

from cute.matchers import named, with_text
from test.drivers import ScreenDriver


def message_box(parent):
    return MessageBoxDriver.find_single(parent, QMessageBox, named("message_box"))


class MessageBoxDriver(ScreenDriver):
    def is_showing_message(self, message):
        self.label(named("qt_msgbox_label")).has_text(message)

    def is_showing_details(self, message):
        self.rich_text_edit().has_plain_text(message)

    def acknowledge(self):
        self.button(with_text("OK")).click()

    def confirm(self):
        self.button(with_text(contains_string("Yes"))).click()
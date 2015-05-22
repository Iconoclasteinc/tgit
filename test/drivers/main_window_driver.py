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

from cute import keyboard_shortcuts
from cute.widgets import WidgetDriver
from test.drivers.menu_bar_driver import menu_bar

class MainWindowDriver(WidgetDriver):
    def has_disabled_album_actions(self):
        menu_bar(self).has_disabled_album_actions()

    def close_album(self, using_shortcut=False):
        if using_shortcut:
            self.click()
            self.perform(keyboard_shortcuts.CLOSE)
        else:
            menu_bar(self).close_album()

    def add_files(self):
        menu_bar(self).add_files()

    def add_folder(self):
        menu_bar(self).add_folder()

    def export(self):
        menu_bar(self).export()

    def settings(self):
        menu_bar(self).settings()

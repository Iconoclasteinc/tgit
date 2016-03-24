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

from PyQt5.QtWidgets import QFileDialog

from cute.matchers import named
from cute.widgets import window
from test.drivers.file_dialog_driver import FileDialogDriver


def select_project_destination_dialog(parent):
    return SelectProjectDestinationDialogDriver(window(QFileDialog, named("select_project_destination_dialog")),
                                                parent.prober, parent.gesture_performer)


class SelectProjectDestinationDialogDriver(FileDialogDriver):
    def select_destination(self, destination):
        self.navigate_to_dir(destination)
        self.has_accept_button_text("&Choose")
        self.accept()

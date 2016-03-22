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
from PyQt5.QtWidgets import QFileDialog

from tgit.ui import locations


def make_select_project_destination_dialog(on_select, parent=None, native=True, delete_on_close=True):
    dialog = SelectProjectDestinationDialog(parent, native, delete_on_close)
    dialog.on_select(on_select)
    return dialog


class SelectProjectDestinationDialog(QFileDialog):
    def __init__(self, parent=None, native=None, delete_on_close=True):
        super().__init__(parent)
        self.setObjectName("select_project_destination_dialog")
        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self.setDirectory(locations.Home)
        self.setFileMode(QFileDialog.Directory)
        self.setOption(QFileDialog.DontUseNativeDialog, not native)

    def on_select(self, on_select):
        self.fileSelected.connect(on_select)

    def done(self, result):
        self.fileSelected.disconnect()
        super().done(result)

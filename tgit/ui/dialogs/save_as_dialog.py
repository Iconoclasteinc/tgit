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

from tgit.ui import locations, timing


def make_save_as_excel_dialog(on_select, default_file_name="", parent=None, native=True, delete_on_close=True):
    dialog = SaveAsDialog(default_file_name, "Save As", "xlsx",
                        ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"], parent, native,
                        delete_on_close)
    dialog.on_select(on_select)
    return dialog


def make_save_as_csv_dialog(on_select, default_file_name="", parent=None, native=True, delete_on_close=True):
    dialog = SaveAsDialog(default_file_name, "Export As", "csv", ["text/csv"], parent, native, delete_on_close)
    dialog.on_select(on_select)
    return dialog


class SaveAsDialog(QFileDialog):
    def __init__(self, default_file_name, title, default_suffix, mime_type_filters, parent, native, delete_on_close):
        super().__init__(parent)
        self.setObjectName("save_as_dialog")
        self.setAttribute(Qt.WA_DeleteOnClose, delete_on_close)
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setDirectory(locations.Home)
        self.setFileMode(QFileDialog.AnyFile)
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.setMimeTypeFilters(mime_type_filters)
        self.setDefaultSuffix(default_suffix)
        self.setWindowTitle(self.tr(title))
        self.selectFile(default_file_name)

    def on_select(self, on_select):
        self.fileSelected.connect(timing.after_delay(on_select))

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

import os

from PyQt5.QtCore import QDir, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog


class ExportAsDialog(QFileDialog):
    export_as = pyqtSignal(str)

    def __init__(self, parent, native):
        super().__init__(parent)
        self._build(native)

    def _build(self, native):
        self.setObjectName('export-as-dialog')
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setDirectory(QDir.homePath())
        self.setFileMode(QFileDialog.AnyFile)
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.fileSelected.connect(self._signal_export_as)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def _signal_export_as(self, path):
        self.export_as.emit(os.path.abspath(path))

    def display(self):
        self.open()

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

from PyQt4.QtCore import QDir, Qt, QObject, pyqtSignal
from PyQt4.QtGui import QFileDialog


class ExportAsDialog(QObject):
    exportAs = pyqtSignal(unicode)

    def __init__(self, parent, native):
        QObject.__init__(self)
        self.parent = parent
        self.native = native

    def display(self):
        dialog = QFileDialog(self.parent)
        dialog.setObjectName('export-as-dialog')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setDirectory(QDir.homePath())
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self.native)
        dialog.fileSelected.connect(lambda f: self.exportAs.emit(f))
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.open()
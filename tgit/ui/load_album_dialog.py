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
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtWidgets import QFileDialog

DOCUMENTS_FOLDER = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)


class LoadAlbumDialog(QFileDialog):
    def __init__(self, parent=None, native=True):
        super().__init__(parent)
        self.setObjectName("load_album_dialog")
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.setDirectory(DOCUMENTS_FOLDER)
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter("{0} (*.tgit)".format(self.tr("TGiT Album files")))

    def select(self, on_select):
        self.fileSelected.connect(on_select)
        self.open()

    def done(self, result):
        self.fileSelected.disconnect()
        super().done(result)

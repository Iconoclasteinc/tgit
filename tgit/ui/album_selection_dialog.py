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

from PyQt5.QtCore import QDir, pyqtSignal
from PyQt5.QtWidgets import QFileDialog


def make_album_selection_dialog(parent_window, native=True, *, on_select_album):
    dialog = AlbumSelectionDialog(parent_window, native)
    dialog.track_selected.connect(on_select_album)
    return dialog


class AlbumSelectionDialog(QFileDialog):
    track_selected = pyqtSignal(str)

    def __init__(self, parent, native):
        super().__init__(parent)
        self.setObjectName("import_album_from_track_dialog")
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilters(
            ["{0} ({1})".format(self.tr("MP3 files"), "*.mp3"), "{0} ({1})".format(self.tr("FLAC files"), "*.flac")])
        self.setDirectory(QDir.homePath())
        self.fileSelected.connect(lambda selected: self.track_selected.emit(os.path.abspath(selected)))
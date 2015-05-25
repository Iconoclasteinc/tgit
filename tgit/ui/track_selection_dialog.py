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


def make_track_selection_dialog(parent, native=True, *, on_select_tracks):
    dialog = TrackSelectionDialog(parent, native)
    dialog.tracks_selected.connect(on_select_tracks)
    return dialog


class TrackSelectionDialog(QFileDialog):
    tracks_selected = pyqtSignal(list)

    file_types = {'mp3': "MP3 Files", 'flac': "FLAC files"}

    def __init__(self, parent, native):
        super().__init__(parent)
        self.setObjectName("track-selection-dialog")
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.setDirectory(QDir.homePath())
        self.filesSelected.connect(lambda selected: self.tracks_selected.emit(list(map(os.path.abspath, selected))))
        self.select_files()
        self.filter_tracks('mp3')

    def select_folders(self):
        self.setFileMode(QFileDialog.Directory)

    def select_files(self):
        self.setFileMode(QFileDialog.ExistingFiles)

    def filter_tracks(self, type_):
        self.setNameFilter("{0} {1}".format(self.tr(self.file_types[type_]), "*.{}".format(type_)))
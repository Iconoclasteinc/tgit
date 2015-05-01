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

from PyQt5.QtCore import QDir, Qt, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from tgit.album import Album


class TrackSelectionDialog(QFileDialog):
    tracks_selected = pyqtSignal(list)

    def __init__(self, parent, native):
        super().__init__(parent)
        self._build(native)

    def _build(self, native):
        self.setObjectName("track-selection-dialog")
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.setDirectory(QDir.homePath())
        self.filesSelected.connect(self._signal_tracks_selected)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def _signal_tracks_selected(self, selection):
        return self.tracks_selected.emit([os.path.abspath(entry) for entry in selection])

    def display(self, album, folders=False):
        name_filters = []
        if album.type == Album.Type.MP3:
            name_filters.append("{0} {1}".format(self.tr("MP3 files"), "*.mp3"))

        if album.type == Album.Type.FLAC:
            name_filters.append("{0} {1}".format(self.tr("FLAC files"), "*.flac"))

        self.setNameFilters(name_filters)

        if folders:
            self.setFileMode(QFileDialog.Directory)
        else:
            self.setFileMode(QFileDialog.ExistingFiles)

        self.open()
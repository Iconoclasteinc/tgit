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

from tgit.ui import locations
from tgit import fs


class TrackSelectionDialog(QFileDialog):
    _FILTERS = {'mp3': "MP3 Files", 'flac': "FLAC files"}

    def __init__(self, parent=None, native=True):
        super().__init__(parent)
        self.setObjectName("track-selection-dialog")
        self.setOption(QFileDialog.DontUseNativeDialog, not native)
        self.finished.connect(self.filesSelected.disconnect)
        self.setDirectory(locations.Music)

    def select_files_in_folder(self, file_type, on_select):
        self.setFileMode(QFileDialog.Directory)
        self.setNameFilter(self._filter_for(file_type))
        self.filesSelected.connect(lambda files: on_select(*self._list_files(folder=files[0], file_type=file_type)))
        self.open()

    def select_files(self, file_type, on_select):
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setNameFilter(self._filter_for(file_type))
        self.filesSelected.connect(lambda files: on_select(*files))
        self.open()

    def select_file(self, file_type, on_select):
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter(self._filter_for(file_type))
        self.filesSelected.connect(lambda files: on_select(files[0]))
        self.open()

    def _filter_for(self, type_):
        return "{0} {1}".format(self.tr(self._FILTERS[type_]), "*.{}".format(type_))

    def _list_files(self, folder, file_type):
        return [filename for filename in fs.list_dir(folder) if filename.endswith("." + file_type)]

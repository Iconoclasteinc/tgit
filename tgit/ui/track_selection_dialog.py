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

from PyQt4.QtCore import QDir, QFileInfo, Qt
from PyQt4.QtGui import QFileDialog

from tgit.ui.file_chooser import FileChooser
from tgit.ui.views import mainWindow


class TrackSelectionDialog(FileChooser):
    NAME = 'track-selection-dialog'
    MP3_FILTER = '*.mp3'

    #todo Introduce Preferences
    native = True

    def __init__(self):
        FileChooser.__init__(self)

    def _createDialog(self):
        dialog = QFileDialog(mainWindow())
        dialog.setObjectName(TrackSelectionDialog.NAME)
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self.native)
        dialog.setDirectory(QDir.homePath())
        dialog.setNameFilter('%s (%s)' % (dialog.tr('Audio files'), self.MP3_FILTER))
        dialog.filesSelected.connect(self._selectAudioFiles)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        return dialog

    def _selectAudioFiles(self, selection):
        self.signalFilesChosen(self._audioFilesFrom(selection))

    def _audioFilesFrom(self, selection):
        audioFiles = []
        for filename in selection:
            if self._isDir(filename):
                audioFiles.extend(self._listAudioFilesIn(QDir(filename)))
            else:
                audioFiles.append(filename)
        return audioFiles

    def _listAudioFilesIn(self, folder):
        return [f.canonicalFilePath() for f in folder.entryInfoList([self.MP3_FILTER])]

    def _isDir(self, filename):
        return QFileInfo(filename).isDir()

    def chooseFiles(self):
        dialog = self._createDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.open()

    def chooseDirectory(self):
        dialog = self._createDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.open()
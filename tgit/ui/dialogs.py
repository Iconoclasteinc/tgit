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

from PyQt4.QtCore import QDir, QFileInfo
from PyQt4.QtGui import QFileDialog

from tgit.ui.file_chooser import FileChooser
from tgit.ui import constants as ui

class AudioFileChooserDialog(FileChooser):
    MP3_FILTER = '*.mp3'

    def __init__(self, native=True, parent=None):
        FileChooser.__init__(self)
        self._dialog = None
        self._native = native
        self._parent = parent

    def setParent(self, parent):
        self._parent = parent

    def _makeDialog(self, parent):
        dialog = QFileDialog(parent)
        dialog.setObjectName(ui.CHOOSE_AUDIO_FILES_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setNameFilter('%s (%s)' % (dialog.tr('Audio files'), self.MP3_FILTER))
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self._native)
        dialog.filesSelected.connect(self._selectAudioFiles)
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

    def _createDialogOnFirstUse(self):
        if not self._dialog:
            self._dialog = self._makeDialog(self._parent)

    def chooseFiles(self):
        self._createDialogOnFirstUse()
        self._dialog.setFileMode(QFileDialog.ExistingFiles)
        self._dialog.open()

    def chooseDirectory(self):
        self._createDialogOnFirstUse()
        self._dialog.setFileMode(QFileDialog.Directory)
        self._dialog.open()
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

from PyQt4.QtCore import QDir
from PyQt4.QtGui import QFileDialog

from tgit.ui.file_chooser import FileChooser
from tgit.ui import constants as ui


class AudioFileChooserDialog(FileChooser):
    def __init__(self, native=True, parent=None):
        FileChooser.__init__(self)
        self._dialog = None
        self._native = native
        self._parent = parent

    def setParent(self, parent):
        self._parent = parent

    def _makeDialog(self, parent):
        dialog = QFileDialog(parent)
        dialog.setObjectName(ui.CHOOSE_AUDIO_FILE_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter('%s (*.mp3)' % dialog.tr('Audio files'))
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self._native)
        dialog.fileSelected.connect(self._signalFileChosen)
        return dialog

    def chooseFile(self):
        if not self._dialog:
            self._dialog = self._makeDialog(self._parent)
        self._dialog.open()


class ImageFileChooserDialog(FileChooser):
    def __init__(self, native=True, parent=None):
        FileChooser.__init__(self)
        self._dialog = None
        self._native = native
        self._parent = parent

    def setParent(self, parent):
        self._parent = parent

    def _makeDialog(self, parent):
        dialog = QFileDialog(parent)
        dialog.setObjectName(ui.CHOOSE_IMAGE_FILE_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter('%s (*.png *.jpeg *.jpg)' % dialog.tr('Image files'))
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self._native)
        dialog.fileSelected.connect(self._signalFileChosen)
        return dialog

    def chooseFile(self):
        if not self._dialog:
            self._dialog = self._makeDialog(self._parent)
        self._dialog.open()
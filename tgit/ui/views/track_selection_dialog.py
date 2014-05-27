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
from tgit.ui.views import mainWindow


class TrackSelectionDialog(object):
    MP3_FILES = '*.mp3'

    #todo Introduce Preferences
    native = True

    def __init__(self):
        self.render()

    def render(self):
        self.dialog = QFileDialog(mainWindow())
        self.dialog.setObjectName('track-selection-dialog')
        self.dialog.setOption(QFileDialog.DontUseNativeDialog, not self.native)
        self.dialog.setNameFilter('%s (%s)' % (self.dialog.tr('Audio files'), self.MP3_FILES))
        self.dialog.setDirectory(QDir.homePath())

    def bind(self, **handlers):
        if 'tracksSelected' in handlers:
            self.dialog.filesSelected.connect(handlers['tracksSelected'])

    def show(self, folders=False):
        if folders:
            self.dialog.setFileMode(QFileDialog.Directory)
        else:
            self.dialog.setFileMode(QFileDialog.ExistingFiles)
        self.dialog.open()

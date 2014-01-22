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

from PyQt4.QtCore import QDir, Qt
from PyQt4.QtGui import QFileDialog
from tgit.announcer import Announcer
from tgit.ui.views import mainWindow


def trackSelectionDialog(listener):
    dialog = TrackSelectionDialog()
    dialog.announceTo(listener)
    return dialog


class TrackSelectionDialog(object):
    NAME = 'track-selection-dialog'

    ALL_FILES = '*.*'

    #todo Introduce Preferences
    native = True

    def __init__(self):
        self._announce = Announcer()
        self.filter = TrackSelectionDialog.ALL_FILES

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def render(self):
        self._dialog = QFileDialog(mainWindow())
        self._dialog.setObjectName(TrackSelectionDialog.NAME)
        self._dialog.setOption(QFileDialog.DontUseNativeDialog, not self.native)
        self._dialog.setDirectory(QDir.homePath())
        self._dialog.setNameFilter('%s (%s)' % (self._dialog.tr('Audio files'), self.filter))
        self._dialog.filesSelected.connect(self._announce.tracksSelected)
        self._dialog.setAttribute(Qt.WA_DeleteOnClose)

    def show(self, folders=False):
        if folders:
            self._dialog.setFileMode(QFileDialog.Directory)
        else:
            self._dialog.setFileMode(QFileDialog.ExistingFiles)
        self._dialog.open()
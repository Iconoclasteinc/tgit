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

    def render(self, folderMode=False):
        dialog = QFileDialog(mainWindow())
        dialog.setObjectName(TrackSelectionDialog.NAME)
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self.native)
        dialog.setDirectory(QDir.homePath())
        dialog.setNameFilter('%s (%s)' % (dialog.tr('Audio files'), self.filter))
        dialog.filesSelected.connect(self._announce.tracksSelected)
        dialog.setAttribute(Qt.WA_DeleteOnClose)

        if folderMode:
            dialog.setFileMode(QFileDialog.Directory)
        else:
            dialog.setFileMode(QFileDialog.ExistingFiles)

        dialog.open()
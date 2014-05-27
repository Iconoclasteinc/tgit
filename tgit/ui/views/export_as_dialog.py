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


class ExportAsDialog(object):
    #todo Introduce Preferences
    native = True

    def __init__(self):
        self.build()

    def build(self):
        self.dialog = QFileDialog(mainWindow())
        self.dialog.setObjectName('export-as-dialog')
        self.dialog.setAcceptMode(QFileDialog.AcceptSave)
        self.dialog.setDirectory(QDir.homePath())
        self.dialog.setFileMode(QFileDialog.AnyFile)
        self.dialog.setOption(QFileDialog.DontUseNativeDialog, not self.native)

    def bind(self, **handlers):
        if 'exportAs' in handlers:
            self.dialog.fileSelected.connect(handlers['exportAs'])

    def show(self):
        self.dialog.open()

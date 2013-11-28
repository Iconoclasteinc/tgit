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

from tgit.announcer import Announcer
from tgit.ui import constants as ui


class ExportAsDialog(object):
    def __init__(self, native=True, parent=None):
        self._native = native
        self._parent = parent
        self._announce = Announcer()

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def show(self, album):
        dialog = QFileDialog(self._parent)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setObjectName(ui.EXPORT_AS_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setOption(QFileDialog.DontUseNativeDialog, not self._native)
        dialog.fileSelected.connect(lambda filename: self._announce.export(album, filename))
        dialog.open()
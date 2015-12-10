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

import sys

from PyQt5.QtWidgets import QDialog
import mutagen
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR, Qt

import tgit
from tgit.ui.helpers.ui_file import UIFile


def _python_version():
    return "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])


class AboutDialog(QDialog, UIFile):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        self._setup_ui()

    def _setup_ui(self):
        self._load(":/ui/about_dialog.ui")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._version.setText("v{0}".format(tgit.__version__))
        self._mutagen_version.setText(mutagen.version_string)
        self._python_version.setText(_python_version())
        self._qt_version.setText(QT_VERSION_STR)
        self._pyqt_version.setText(PYQT_VERSION_STR)
        self._actions.accepted.connect(self.close)
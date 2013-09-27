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

from PyQt4.QtGui import QWidget, QGridLayout, QLabel, QLineEdit

ALBUM_PANEL_NAME = 'Album Panel'
RELEASE_NAME_NAME = 'Release Name'


class AlbumPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_PANEL_NAME)
        layout = QGridLayout()
        self.setLayout(layout)
        self._fill(layout)
        self.translateUi()

    def _fill(self, layout):
        self._releaseNameLabel = QLabel()
        layout.addWidget(self._releaseNameLabel, 0, 0)
        self._releaseNameEdit = QLineEdit()
        self._releaseNameEdit.setObjectName(RELEASE_NAME_NAME)
        layout.addWidget(self._releaseNameEdit, 0, 1)
        self._releaseNameLabel.setBuddy(self._releaseNameEdit)

    def translateUi(self):
        self._releaseNameLabel.setText(self.tr("Release Name: "))

    def trackSelected(self, track):
        self._releaseNameEdit.setText(track.releaseName)

    def getReleaseName(self):
        return self._releaseNameEdit.text()




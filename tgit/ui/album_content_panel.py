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

from PyQt4.QtGui import QWidget, QGridLayout, QLabel

ALBUM_CONTENT_PANEL_NAME = 'Album Content Panel'
TRACK_TITLE_HEADER_NAME = 'Track Title Column Header'


class AlbumContentPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_CONTENT_PANEL_NAME)
        self._layout = QGridLayout()
        self.setLayout(self._layout)
        self._fill(self._layout)

    def _fill(self, layout):
        self._addColumnHeadings(layout)

    def _addColumnHeadings(self, layout):
        trackTitleHeading = QLabel()
        trackTitleHeading.setText('<strong>%s</strong>' % self.tr('Track Title<strong>'))
        trackTitleHeading.setObjectName(TRACK_TITLE_HEADER_NAME)
        layout.addWidget(trackTitleHeading, 0, 0)

    def setTrack(self, track):
        label = QLabel(track.trackTitle)
        self._layout.addWidget(label, 1, 0)

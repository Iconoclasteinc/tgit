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
ALBUM_TRACK_TITLE_NAME = 'Album Track Title'


class AlbumContentPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_CONTENT_PANEL_NAME)
        layout = QGridLayout()
        self.setLayout(layout)
        self._fill(layout)

        self._track = None

    def _fill(self, layout):
        self._addTrackTitle(layout, 0)

    def _addTrackTitle(self, layout, row):
        self._trackTitleLabel = QLabel()
        self._trackTitleLabel.setObjectName(ALBUM_TRACK_TITLE_NAME)
        layout.addWidget(self._trackTitleLabel, row, 0)

    def setTrack(self, track):
        self._track = track
        self._trackTitleLabel.setText(self._track.trackTitle)

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

import functools
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

from tgit import audio_player as audio

ALBUM_CONTENT_PANEL_NAME = 'Album Content Panel'
TRACK_TABLE_HEADER_NAME = 'Track Table Heading'
TRACK_TABLE_ROW_NAME = 'Track Table Row'
TRACK_TITLE_HEADER_NAME = 'Track Title Column Header'
TRACK_DURATION_HEADER_NAME = 'Track Duration Column Header'


# todo Duplicates same function in TrackPanel. Where should it go?
# (back to MP3File?, in a shared ui module? in the ui module itself?)
def asDuration(seconds):
    return "%02d:%02d" % divmod(round(seconds), 60)


class AlbumContentPanel(QWidget):
    def __init__(self, player=audio.null(), parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_CONTENT_PANEL_NAME)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._fill(self._layout)
        self._player = player

    def _fill(self, layout):
        self._addColumnHeadings(layout)

    # todo use a table, we cannot rely on widgets order of addition
    def _addColumnHeadings(self, layout):
        header = QWidget()
        header.setObjectName(TRACK_TABLE_HEADER_NAME)
        headings = QHBoxLayout()
        header.setLayout(headings)
        titleHeading = QLabel()
        titleHeading.setText('<strong>%s</strong>' % self.tr('Track Title'))
        headings.addWidget(titleHeading)
        durationHeading = QLabel()
        durationHeading.setText('<strong>%s</strong>' % self.tr('Duration'))
        headings.addWidget(durationHeading)
        headings.addWidget(QLabel())
        layout.addWidget(header)

    def addTrack(self, track):
        row = QWidget()
        row.setObjectName(TRACK_TABLE_ROW_NAME)
        cells = QHBoxLayout()
        row.setLayout(cells)
        title = QLabel(track.trackTitle)
        cells.addWidget(title)
        duration = QLabel(asDuration(track.duration))
        cells.addWidget(duration)
        button = QPushButton()
        button.setText(self.tr('Play'))
        button.setCheckable(True)
        button.setAutoExclusive(True)
        button.clicked.connect(functools.partial(self._playOrStopTrack, track.filename))
        cells.addWidget(button)
        self._layout.addWidget(row)

    def _playOrStopTrack(self, filename):
        if not self._player.hasSource(filename):
            self._player.setSource(filename)
        if self._player.isPlaying():
            self._player.stop()
        else:
            self._player.play()

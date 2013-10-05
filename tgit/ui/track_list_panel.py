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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                         QHeaderView)

from tgit import audio

ALBUM_CONTENT_PANEL_NAME = 'Album Content Panel'
TRACK_TABLE_NAME = 'Track Table'
PLAY_BUTTON_NAME = 'Play Button'

TITLE = 0
DURATION = 1
LISTEN = 2


# todo Put back in MP3File
def asDuration(seconds):
    return "%02d:%02d" % divmod(round(seconds), 60)


class TrackListPanel(QWidget, audio.MediaListener):
    def __init__(self, player=audio.noSound(), parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_CONTENT_PANEL_NAME)
        self._player = player
        self._player.addMediaListener(self)
        self._fill()
        self._tracks = []

    def mediaStopped(self, media):
        self._listenButtonFor(media).setChecked(False)

    def mediaPaused(self, media):
        self.mediaStopped(media)

    def _fill(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._addTrackTable(self._layout)

    def _addTrackTable(self, layout):
        self._table = QTableWidget()
        self._table.setObjectName(TRACK_TABLE_NAME)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.NoSelection)
        self._table.setShowGrid(False)
        headers = [self.tr('Track Title'), self.tr('Duration'), '']
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.horizontalHeader().setResizeMode(TITLE, QHeaderView.Stretch)
        layout.addWidget(self._table)

    def addTrack(self, track):
        newRow = self._table.rowCount()
        self._table.insertRow(newRow)
        title = QTableWidgetItem(track.trackTitle)
        self._table.setItem(newRow, TITLE, title)
        duration = QTableWidgetItem(asDuration(track.duration))
        duration.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._table.setItem(newRow, DURATION, duration)
        playButton = QPushButton()
        playButton.setObjectName(PLAY_BUTTON_NAME)
        playButton.setText(self.tr('Play'))
        playButton.setCheckable(True)
        playButton.clicked.connect(functools.partial(self._listenTo, track))
        self._table.setCellWidget(newRow, LISTEN, playButton)
        self._tracks.append(track)

    def _listenButtonFor(self, media):
        for index, track in enumerate(self._tracks):
            if track == media:
                return self._listenButton(index)

    def _listenButton(self, index):
        return self._listenButtons()[index]

    def _listenButtons(self):
        return [self._table.cellWidget(row, LISTEN) for row in xrange(self._table.rowCount())]

    def _listenTo(self, track):
        if self.sender().isChecked():
            self._player.play(track)
        else:
            self._player.stop()
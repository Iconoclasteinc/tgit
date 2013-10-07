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
                         QHeaderView, QHBoxLayout)

from tgit import audio
from tgit.ui import display
from tgit.null import Null

ALBUM_CONTENT_PANEL_NAME = 'Album Content Panel'
TRACK_TABLE_NAME = 'Track Table'
PLAY_BUTTON_NAME = 'Play Button'
ADD_BUTTON_NAME = 'Add Button'

TRACK_TITLE = 0
LEAD_PERFORMER = 1
RELEASE_NAME = 2
BITRATE = 3
DURATION = 4
LISTEN = 5


class TrackListPanel(QWidget, audio.MediaListener):
    def __init__(self, player=Null(), handler=Null(), parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_CONTENT_PANEL_NAME)
        self._player = player
        self._player.addMediaListener(self)
        self._requestHandler = handler
        self._fill()
        self.localize()
        self._tracks = []

    def mediaStopped(self, media):
        self._listenButtonFor(media).setChecked(False)

    def mediaPaused(self, media):
        self.mediaStopped(media)

    def setRequestHandler(self, handler):
        self._requestHandler = handler

    def _fill(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._addTrackTable(self._layout)
        self._addButtons(self._layout)

    def _addTrackTable(self, layout):
        self._table = QTableWidget()
        self._table.setObjectName(TRACK_TABLE_NAME)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.NoSelection)
        self._table.setShowGrid(False)
        headers = [self.tr('Track Title'), self.tr('Lead Performer'), self.tr('Release Name'),
                   self.tr('Bitrate'), self.tr('Duration'), self.tr('')]
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.horizontalHeader().setResizeMode(TRACK_TITLE, QHeaderView.Stretch)
        layout.addWidget(self._table)

    def addTrack(self, track):
        newRow = self._table.rowCount()
        self._table.insertRow(newRow)
        self._table.setItem(newRow, TRACK_TITLE, QTableWidgetItem(track.trackTitle))
        self._table.setItem(newRow, LEAD_PERFORMER, QTableWidgetItem(track.leadPerformer))
        self._table.setItem(newRow, RELEASE_NAME, QTableWidgetItem(track.releaseName))
        self._table.setItem(newRow, BITRATE,
                            QTableWidgetItem("%d kbps" % display.toKbps(track.bitrate)))
        duration = QTableWidgetItem(display.asDuration(track.duration))
        duration.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._table.setItem(newRow, DURATION, duration)
        playButton = QPushButton()
        playButton.setObjectName(PLAY_BUTTON_NAME)
        playButton.setText(self.tr('Play'))
        playButton.setCheckable(True)
        playButton.clicked.connect(functools.partial(self._listenTo, track))
        self._table.setCellWidget(newRow, LISTEN, playButton)
        self._tracks.append(track)

    def _addButtons(self, layout):
        buttonLayout = QHBoxLayout()
        self._addButton = QPushButton()
        self._addButton.setObjectName(ADD_BUTTON_NAME)
        self._addButton.clicked.connect(self._fireSelectTrack)
        buttonLayout.addWidget(self._addButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def _fireSelectTrack(self):
        self._requestHandler.selectTrack()

    def localize(self):
        self._addButton.setText(self.tr('Add Track...'))

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
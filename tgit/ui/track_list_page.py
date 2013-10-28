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

import functools as func

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                         QHBoxLayout)

from tgit.announcer import Announcer
from tgit.album import AlbumListener
from tgit.player import PlayerListener
from tgit.ui import constants as ui, display

TRACK_TITLE_COLUMN = 0
LEAD_PERFORMER_COLUMN = 1
RELEASE_NAME_COLUMN = 2
BITRATE_COLUMN = 3
DURATION_COLUMN = 4
PLAY_COLUMN = 5
REMOVE_COLUMN = 6


class TrackListPage(QWidget, PlayerListener, AlbumListener):
    def __init__(self, album, player, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._player = player
        self._player.addPlayerListener(self)
        self._requestListeners = Announcer()

        self.setObjectName(ui.TRACK_LIST_PAGE_NAME)
        self._build()
        self.localize()
        self._populateTableWithTracksFrom(album)

    def addRequestListener(self, listener):
        self._requestListeners.addListener(listener)

    def trackStopped(self, track):
        try:
            self._listenButton(self._rowFor(track)).setChecked(False)
        except StopIteration:
            #Track has been removed
            pass

    def trackPaused(self, track):
        self.trackStopped(track)

    def _build(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._addTrackTable(self._layout)
        self._addButtons(self._layout)

    def _addTrackTable(self, layout):
        self._table = QTableWidget()
        self._table.setObjectName(ui.TRACK_TABLE_NAME)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.NoSelection)
        self._table.setShowGrid(False)
        headers = [self.tr('Track Title'), self.tr('Lead Performer'), self.tr('Release Name'),
                   self.tr('Bitrate'), self.tr('Duration'), self.tr(''), self.tr('')]
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.verticalHeader().setMovable(True)
        self._table.verticalHeader().sectionMoved.connect(self._moveTrack)
        layout.addWidget(self._table)

    def _populateTableWithTracksFrom(self, album):
        for row, track in enumerate(album.tracks):
            self._removeTrackFromTable(row, track)
            self._addTrackToTable(row, track)

    def _moveTrack(self, index, from_, to):
        track = self._trackInRow(from_)
        self._album.removeTrack(track)
        self._album.addTrack(track, to)

    def _trackInRow(self, row):
        return self._table.item(row, TRACK_TITLE_COLUMN).data(Qt.UserRole)

    def trackRemoved(self, track, position):
        self._removeTrackFromTable(position, track)

    def _removeTrackFromTable(self, position, track):
        track.removeTrackListener(self)
        self._table.removeRow(position)

    def trackAdded(self, track, position):
        self._addTrackToTable(position, track)

    def _addTrackToTable(self, position, track):
        self._table.insertRow(position)
        self._setTrackInRow(position, track)
        track.addTrackListener(self)

    def _setTrackInRow(self, row, track):
        item = QTableWidgetItem(track.trackTitle)
        item.setData(Qt.UserRole, track)
        self._table.setItem(row, TRACK_TITLE_COLUMN, item)
        self._table.setItem(row, LEAD_PERFORMER_COLUMN, QTableWidgetItem(self._album.leadPerformer))
        self._table.setItem(row, RELEASE_NAME_COLUMN, QTableWidgetItem(self._album.releaseName))
        self._table.setItem(row, BITRATE_COLUMN,
                            QTableWidgetItem('%d kbps' % display.inKbps(track.bitrate)))
        duration = QTableWidgetItem(display.asDuration(track.duration))
        duration.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._table.setItem(row, DURATION_COLUMN, duration)
        playButton = QPushButton()
        playButton.setObjectName(ui.PLAY_BUTTON_NAME)
        playButton.setText(self.tr('Play'))
        playButton.setCheckable(True)
        playButton.setChecked(self._isPlaying(track))
        playButton.clicked.connect(func.partial(self._listenToTrack, track))
        self._table.setCellWidget(row, PLAY_COLUMN, playButton)
        removeButton = QPushButton()
        removeButton.setObjectName(ui.REMOVE_BUTTON_NAME)
        removeButton.setText(self.tr('Remove'))
        removeButton.clicked.connect(func.partial(self._removeTrack, track))
        self._table.setCellWidget(row, REMOVE_COLUMN, removeButton)

    def trackStateChanged(self, track):
        row = self._rowFor(track)
        self._setTrackInRow(row, track)

    def albumStateChanged(self, album):
        for row in xrange(self._table.rowCount()):
            track = self._trackInRow(row)
            self._setTrackInRow(row, track)

    def _addButtons(self, layout):
        buttonLayout = QHBoxLayout()
        self._addButton = QPushButton()
        self._addButton.setObjectName(ui.ADD_TRACK_BUTTON_NAME)
        self._addButton.clicked.connect(self._selectTrack)
        buttonLayout.addWidget(self._addButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def _selectTrack(self):
        self._requestListeners.selectTrack()

    def localize(self):
        self._addButton.setText(self.tr('Add Track...'))

    def _rowFor(self, track):
        return next(row for row in xrange(self._table.rowCount())
                    if self._trackInRow(row) == track)

    def _listenButton(self, index):
        return self._listenButtons()[index]

    def _listenButtons(self):
        return [self._table.cellWidget(row, PLAY_COLUMN) for row in
                xrange(self._table.rowCount())]

    def _listenToTrack(self, track):
        if self.sender().isChecked():
            self._player.play(track)
        else:
            self._player.stop()

    def _removeTrack(self, track):
        if self._isPlaying(track):
            self._player.stop()

        self._album.removeTrack(track)

    def _isPlaying(self, track):
        return self._player.isPlaying() and track == self._player.currentTrack()
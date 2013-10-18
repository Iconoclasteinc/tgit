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
from tgit import player
from tgit.ui import display

ALBUM_CONTENT_PANEL_NAME = 'Album Content Panel'
TRACK_TABLE_NAME = 'Track Table'
PLAY_BUTTON_NAME = 'Play Button'
REMOVE_BUTTON_NAME = 'Remove Button'
ADD_BUTTON_NAME = 'Add Button'

TRACK_TITLE = 0
LEAD_PERFORMER = 1
RELEASE_NAME = 2
BITRATE = 3
DURATION = 4
LISTEN = 5
REMOVE = 6


class TrackListPanel(QWidget, player.MediaListener, AlbumListener):
    def __init__(self, album, player, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_CONTENT_PANEL_NAME)
        self._player = player
        self._player.addMediaListener(self)
        self._build()
        self.localize()

        self._album = album
        self._album.addAlbumListener(self)
        self._requestListeners = Announcer()
        self.albumStateChanged(album)

    # todo when we disallow adding the same track multiple times,
    # track filename should be its unique, do we want to pass
    # a filename to the player and get a filename back on notifications?
    def mediaStopped(self, media):
        try:
            self._listenButton(self._rowFor(media)).setChecked(False)
        except StopIteration:
            #Track has been removed
            pass

    def mediaPaused(self, media):
        self.mediaStopped(media)

    def addRequestListener(self, handler):
        self._requestHandler = handler

    def _build(self):
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
                   self.tr('Bitrate'), self.tr('Duration'), self.tr(''), self.tr('')]
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.verticalHeader().setMovable(True)
        self._table.verticalHeader().sectionMoved.connect(self._moveTrack)
        layout.addWidget(self._table)

    def _trackInRow(self, row):
        return self._table.item(row, TRACK_TITLE).data(Qt.UserRole)

    def _moveTrack(self, index, from_, to):
        track = self._trackInRow(from_)
        self._album.removeTrack(track)
        self._album.addTrack(track, to)

    def trackRemoved(self, track, position):
        self._table.removeRow(position)

    def trackAdded(self, track, position):
        self._table.insertRow(position)
        item = QTableWidgetItem(track.trackTitle)
        item.setData(Qt.UserRole, track)
        self._table.setItem(position, TRACK_TITLE, item)
        self._table.setItem(position, LEAD_PERFORMER, QTableWidgetItem(self._album.leadPerformer))
        self._table.setItem(position, RELEASE_NAME, QTableWidgetItem(self._album.releaseName))
        self._table.setItem(position, BITRATE,
                            QTableWidgetItem("%d kbps" % display.inKbps(track.bitrate)))
        duration = QTableWidgetItem(display.asDuration(track.duration))
        duration.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._table.setItem(position, DURATION, duration)
        playButton = QPushButton()
        playButton.setObjectName(PLAY_BUTTON_NAME)
        playButton.setText(self.tr('Play'))
        playButton.setCheckable(True)
        playButton.clicked.connect(func.partial(self._listenToTrack, track))
        self._table.setCellWidget(position, LISTEN, playButton)
        removeButton = QPushButton()
        removeButton.setObjectName(REMOVE_BUTTON_NAME)
        removeButton.setText(self.tr('Remove'))
        removeButton.clicked.connect(func.partial(self._removeTrack, track))
        self._table.setCellWidget(position, REMOVE, removeButton)

    def albumStateChanged(self, album):
        # todo this should iterate album tracks, not rows
        for row in xrange(self._table.rowCount()):
            track = self._trackInRow(row)
            self._table.item(row, TRACK_TITLE).setText(track.trackTitle)
            self._table.item(row, LEAD_PERFORMER).setText(album.leadPerformer)
            self._table.item(row, RELEASE_NAME).setText(album.releaseName)

    def _addButtons(self, layout):
        buttonLayout = QHBoxLayout()
        self._addButton = QPushButton()
        self._addButton.setObjectName(ADD_BUTTON_NAME)
        self._addButton.clicked.connect(self._selectTrack)
        buttonLayout.addWidget(self._addButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

    def _selectTrack(self):
        self._requestHandler.selectTrack()

    def localize(self):
        self._addButton.setText(self.tr('Add Track...'))

    def _rowFor(self, track):
        return next(row for row in xrange(self._table.rowCount())
                    if self._trackInRow(row) == track)

    def _listenButton(self, index):
        return self._listenButtons()[index]

    def _listenButtons(self):
        return [self._table.cellWidget(row, LISTEN) for row in xrange(self._table.rowCount())]

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
        return self._listenButton(self._rowFor(track)).isChecked()
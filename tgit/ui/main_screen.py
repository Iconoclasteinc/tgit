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

from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton

from tgit.announcer import Announcer
from tgit.album import AlbumListener

from tgit.ui.album_panel import AlbumPanel
from tgit.ui.track_list_panel import TrackListPanel
from tgit.ui.track_panel import TrackPanel

TRACK_LIST_PANEL = 0
ALBUM_PANEL = 1
TRACK_PANEL = 2

NEXT_STEP_BUTTON_NAME = "Next Step"
PREVIOUS_STEP_BUTTON_NAME = "Previous Step"
SAVE_BUTTON_NAME = "Save"


class MainScreen(QWidget, AlbumListener):
    def __init__(self, album, player, trackSelector, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._player = player
        self._trackSelector = trackSelector
        self._requestListeners = Announcer()

        self._build()
        self.localize()

    def addRequestListener(self, listener):
        self._requestListeners.addListener(listener)

    def selectTrack(self):
        self._trackListPanel().selectTrack()

    def recordAlbum(self):
        self._requestListeners.recordAlbum()

    def _build(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self._pages = QStackedWidget()
        trackListPanel = TrackListPanel(self._album, self._player, self._trackSelector)
        trackListPanel.addRequestListener(self._requestListeners)
        self._pages.addWidget(trackListPanel)
        self._pages.addWidget(AlbumPanel(self._album))
        self._pages.setCurrentIndex(TRACK_LIST_PANEL)
        layout.addWidget(self._pages)

        layout.addWidget(self._makeButtonBar())

    def _makeButtonBar(self):
        self._buttonBar = QWidget()
        layout = QHBoxLayout()
        self._buttonBar.setLayout(layout)
        self._previousPageButton = QPushButton()
        self._previousPageButton.setObjectName(PREVIOUS_STEP_BUTTON_NAME)
        self._previousPageButton.clicked.connect(self._showPreviousPage)
        self._previousPageButton.setDisabled(True)
        layout.addWidget(self._previousPageButton)
        layout.addStretch()
        self._saveButton = QPushButton()
        self._saveButton.setObjectName(SAVE_BUTTON_NAME)
        self._saveButton.clicked.connect(self.recordAlbum)
        self._saveButton.setDisabled(True)
        layout.addWidget(self._saveButton)
        layout.addStretch()
        self._nextStepButton = QPushButton()
        self._nextStepButton.setObjectName(NEXT_STEP_BUTTON_NAME)
        self._nextStepButton.clicked.connect(self._showNextPage)
        self._nextStepButton.setEnabled(True)
        layout.addWidget(self._nextStepButton)

        return self._buttonBar

    def trackAdded(self, track, position):
        self._addTrackPage(track, position)
        self._nextStepButton.setEnabled(True)

    def trackRemoved(self, track, position):
        self._removeTrackPage(track, position)
        if self._album.empty():
            self._nextStepButton.setDisabled(True)

    def _addTrackPage(self, track, position):
        self._pages.insertWidget(TRACK_PANEL + position, TrackPanel(track))

    def _removeTrackPage(self, track, position):
        self._pages.removeWidget(self._trackPage(position))

    def _currentPage(self):
        return self._pages.currentIndex()

    def _onPage(self, index):
        return self._currentPage() == index

    def _previousPage(self):
        return self._currentPage() - 1

    def _nextPage(self):
        return self._currentPage() + 1

    def _lastPage(self):
        return self._pages.count() - 1

    def showTrackList(self):
        self._showPage(TRACK_LIST_PANEL)

    def _showPage(self, page):
        self._pages.setCurrentIndex(page)

    def _showPreviousPage(self):
        self._showPage(self._previousPage())
        if self._onPage(TRACK_LIST_PANEL):
            self._saveButton.setDisabled(True)
            self._previousPageButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)

    def _showNextPage(self):
        self._showPage(self._nextPage())
        if self._onPage(self._lastPage()):
            self._nextStepButton.setDisabled(True)
        self._previousPageButton.setEnabled(True)
        self._saveButton.setEnabled(True)

    def _trackListPanel(self):
        return self._pages.widget(TRACK_LIST_PANEL)

    def _albumPanel(self):
        return self._pages.widget(ALBUM_PANEL)

    def _trackPage(self, position):
        return self._pages.widget(TRACK_PANEL + position)

    def localize(self):
        self._previousPageButton.setText(self.tr("Previous"))
        self._saveButton.setText(self.tr("Save"))
        self._nextStepButton.setText(self.tr("Next"))
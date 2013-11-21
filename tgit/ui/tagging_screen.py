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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton

from tgit.announcer import Announcer
from tgit.album import AlbumListener
from tgit.ui.file_chooser import FileChoiceListener
from tgit.ui import constants as ui
from tgit.ui.album_page import AlbumPage
from tgit.ui.track_list_page import TrackListPage
from tgit.ui.track_page import TrackPage

TRACK_LIST_PAGE = 0
ALBUM_PAGE = 1
TRACK_PAGE = 2


class TaggingScreen(QWidget, AlbumListener, FileChoiceListener):
    def __init__(self, album, player, audioFileChooser, imageFileChooser, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._player = player
        self._audioFileChooser = audioFileChooser
        self._audioFileChooser.addChoiceListener(self)
        self._imageFileChooser = imageFileChooser
        self._requestListeners = Announcer()

        self._build()
        self.localize()

    def addRequestListener(self, listener):
        self._requestListeners.addListener(listener)

    def filesChosen(self, *filenames):
        for filename in filenames:
            self._requestListeners.addTrackToAlbum(self._album, filename)

    def selectFiles(self):
        self._audioFileChooser.chooseFiles()

    def selectFolder(self):
        self._audioFileChooser.chooseDirectory()

    def recordAlbum(self):
        self._requestListeners.recordAlbum(self._album)

    def _build(self):
        self.setObjectName(ui.TAGGING_SCREEN_NAME)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self._pages = QStackedWidget()
        page = TrackListPage(self._album, self._player)
        page.addRequestListener(self)
        self._pages.addWidget(page)
        self._pages.addWidget(AlbumPage(self._album, self._imageFileChooser))
        self._pages.setCurrentIndex(TRACK_LIST_PAGE)
        layout.addWidget(self._pages)

        layout.addWidget(self._makeButtonBar())

    def _makeButtonBar(self):
        self._buttonBar = QWidget()
        layout = QHBoxLayout()
        self._buttonBar.setLayout(layout)
        self._previousPageButton = QPushButton()
        self._previousPageButton.setObjectName(ui.PREVIOUS_PAGE_BUTTON_NAME)
        self._previousPageButton.clicked.connect(self._showPreviousPage)
        self._previousPageButton.setDisabled(True)
        layout.addWidget(self._previousPageButton)
        layout.addStretch()
        self._saveButton = QPushButton()
        self._saveButton.setObjectName(ui.SAVE_BUTTON_NAME)
        self._saveButton.setFocusPolicy(Qt.ClickFocus)
        self._saveButton.clicked.connect(self.recordAlbum)
        self._saveButton.setDisabled(True)
        layout.addWidget(self._saveButton)
        layout.addStretch()
        self._nextStepButton = QPushButton()
        self._nextStepButton.setObjectName(ui.NEXT_PAGE_BUTTON_NAME)
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
        self._pages.insertWidget(TRACK_PAGE + position, TrackPage(self._album, track))

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
        self._showPage(TRACK_LIST_PAGE)

    def _showPage(self, page):
        self._pages.setCurrentIndex(page)

    def _showPreviousPage(self):
        self._showPage(self._previousPage())
        if self._onPage(TRACK_LIST_PAGE):
            self._saveButton.setDisabled(True)
            self._previousPageButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)

    def _showNextPage(self):
        self._showPage(self._nextPage())
        if self._onPage(self._lastPage()):
            self._nextStepButton.setDisabled(True)
        self._previousPageButton.setEnabled(True)
        self._saveButton.setEnabled(True)

    def _trackListPage(self):
        return self._pages.widget(TRACK_LIST_PAGE)

    def _albumPage(self):
        return self._pages.widget(ALBUM_PAGE)

    def _trackPage(self, position):
        return self._pages.widget(TRACK_PAGE + position)

    def localize(self):
        self._previousPageButton.setText(self.tr('Previous'))
        self._saveButton.setText(self.tr('Save'))
        self._nextStepButton.setText(self.tr('Next'))
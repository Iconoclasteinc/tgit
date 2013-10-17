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

from PyQt4.QtCore import (QDir, QRect)
from PyQt4.QtGui import (QWidget, QMainWindow, QMenu, QAction, QStatusBar, QVBoxLayout,
                         QHBoxLayout, QPushButton, QFileDialog, QStackedWidget)

from tgit.announcer import Announcer
from tgit.album import AlbumListener
from tgit.ui.track_list_panel import TrackListPanel
from tgit.ui.album_panel import AlbumPanel
from tgit.ui.track_panel import TrackPanel


MAIN_WINDOW_NAME = "TGiT"
FILE_MENU_NAME = 'File Menu'
IMPORT_TRACK_ACTION_NAME = 'Import Track Action'
ADD_FILE_BUTTON_NAME = "Add File"
IMPORT_TRACK_DIALOG_NAME = "Select Track File"
NEXT_STEP_BUTTON_NAME = "Next Step"
PREVIOUS_STEP_BUTTON_NAME = "Previous Step"
SAVE_BUTTON_NAME = "Save"

TRACK_LIST_PANEL = 0
ALBUM_PANEL = 1
TRACK_PANEL = 2


class MainWindow(QMainWindow, AlbumListener):
    def __init__(self, album, player, parent=None):
        QMainWindow.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._player = player
        self._musicProducers = Announcer()

        self._build()
        self.show()
        self.raise_()
        self.activateWindow()

    def addMusicProducer(self, producer):
        self._musicProducers.add(producer)

    def trackAdded(self, track, position):
        self._albumPanel().albumStateChanged(self._album)

        self._addTrackPage(track, position)
        self._updateAlbumAndTracks()

        if self._onWelcomePage():
            self._showPage(TRACK_LIST_PANEL)
            self.setCentralWidget(self._mainPanel)

        self._nextStepButton.setEnabled(True)

    def trackRemoved(self, track, position):
        self._removeTrackPage(track, position)
        if self._noMoreTrackPages():
            self._nextStepButton.setDisabled(True)

    def _onWelcomePage(self):
        return self.centralWidget() == self._welcomePanel

    def _makeAddFileDialog(self):
        dialog = QFileDialog(self)
        dialog.setObjectName(IMPORT_TRACK_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")
        dialog.setModal(True)
        dialog.fileSelected.connect(self._musicProducers.announce().importTrack)
        return dialog

    def selectTrack(self):
        if not hasattr(self, '_addFileDialog'):
            self._addFileDialog = self._makeAddFileDialog()
        self._addFileDialog.open()

    def _build(self):
        self.setObjectName(MAIN_WINDOW_NAME)
        self.resize(640, 480)
        self._fillMenu()
        self._makeStatusBar()
        self._makeButtonBar()
        self._makeMainPanel()
        self.setCentralWidget(self._makeWelcomePanel())
        self.localize()

    def _fillMenu(self):
        menuBar = self.menuBar()
        menuBar.setGeometry(QRect(0, 0, 469, 21))
        self._fileMenu = QMenu(menuBar)
        self._fileMenu.setObjectName(FILE_MENU_NAME)
        self._importAction = QAction(self._fileMenu)
        self._importAction.setObjectName(IMPORT_TRACK_ACTION_NAME)
        self._importAction.triggered.connect(self.selectTrack)
        self._fileMenu.addAction(self._importAction)
        menuBar.addMenu(self._fileMenu)

    def _makeStatusBar(self):
        self.setStatusBar(QStatusBar())

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
        self._saveButton.clicked.connect(self._saveAlbum)
        self._saveButton.setDisabled(True)
        layout.addWidget(self._saveButton)
        layout.addStretch()
        self._nextStepButton = QPushButton()
        self._nextStepButton.setObjectName(NEXT_STEP_BUTTON_NAME)
        self._nextStepButton.clicked.connect(self._showNextPage)
        layout.addWidget(self._nextStepButton)

    def _trackListPanel(self):
        return self._pages.widget(TRACK_LIST_PANEL)

    def _albumPanel(self):
        return self._pages.widget(ALBUM_PANEL)

    def _trackPageAt(self, index):
        return self._allTrackPages()[index]

    def _allTrackPages(self):
        return [self._pages.widget(index) for index in xrange(TRACK_PANEL, self._pages.count())]

    def _addTrackPage(self, track, position):
        self._pages.insertWidget(TRACK_PANEL + position, TrackPanel(track))

    def _removeTrackPage(self, track, position):
        self._pages.removeWidget(self._trackPage(position))

    def _trackPage(self, position):
        return self._pages.widget(TRACK_PANEL + position)

    def _noMoreTrackPages(self):
        return len(self._allTrackPages()) == 0

    def _makeMainPanel(self):
        self._mainPanel = QWidget()
        layout = QVBoxLayout()
        self._pages = QStackedWidget()
        trackListPanel = TrackListPanel(self._album, self._player)
        trackListPanel.addRequestListener(self)

        self._pages.addWidget(trackListPanel)
        albumPanel = AlbumPanel(self._album)
        self._pages.addWidget(albumPanel)
        layout.addWidget(self._pages)
        self._previousPageButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)
        layout.addWidget(self._buttonBar)
        self._mainPanel.setLayout(layout)

    def _currentPage(self):
        return self._pages.currentIndex()

    def _onTrackListPage(self):
        return self._currentPage() == TRACK_LIST_PANEL

    def _onLastPage(self):
        return self._currentPage() == self._pages.count() - 1

    def _previousPage(self):
        return self._currentPage() - 1

    def _nextPage(self):
        return self._currentPage() + 1

    def _showPage(self, page):
        self._updateAlbumAndTracks()
        self._pages.setCurrentIndex(page)

    def _showPreviousPage(self):
        self._showPage(self._previousPage())
        if self._onTrackListPage():
            self._saveButton.setDisabled(True)
            self._previousPageButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)

    def _showNextPage(self):
        self._showPage(self._nextPage())
        if self._onLastPage():
            self._nextStepButton.setDisabled(True)
        self._previousPageButton.setEnabled(True)
        self._saveButton.setEnabled(True)

    def _updateAlbumAndTracks(self):
        self._albumPanel().updateAlbum()
        for page in self._allTrackPages():
            page.updateTrack()
        self._trackListPanel().albumStateChanged(self._album)

    def _saveAlbum(self):
        self._updateAlbumAndTracks()
        self._musicProducers.announce().record()

    # todo Extract a WelcomePanel
    def _makeWelcomePanel(self):
        self._welcomePanel = QWidget()
        layout = QHBoxLayout()
        layout.addStretch()
        self._addFileButton = QPushButton()
        self._addFileButton.setObjectName(ADD_FILE_BUTTON_NAME)
        self._addFileButton.clicked.connect(self.selectTrack)
        layout.addWidget(self._addFileButton)
        layout.addStretch()
        self._welcomePanel.setLayout(layout)
        return self._welcomePanel

    def localize(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._fileMenu.setTitle(self.tr('File'))
        self._importAction.setText(self.tr("Import File..."))
        self._addFileButton.setText(self.tr("Add File..."))
        self._saveButton.setText(self.tr("Save"))
        self._previousPageButton.setText(self.tr("Previous"))
        self._nextStepButton.setText(self.tr("Next"))
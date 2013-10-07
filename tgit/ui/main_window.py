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

from tgit.null import Null
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


class MainWindow(QMainWindow):
    def __init__(self, player=Null(), musicDirector=Null()):
        QMainWindow.__init__(self)
        self._player = player
        self._musicDirector = musicDirector
        # We still don't have an album concept
        self._tracks = []
        self._setupUi()
        self.show()
        self.raise_()
        self.activateWindow()

    def setMusicDirector(self, director):
        self._musicDirector = director

    def _setupUi(self):
        self.setObjectName(MAIN_WINDOW_NAME)
        self.resize(640, 480)
        self._makeImportFileDialog()
        self._fillMenu()
        self._makeStatusBar()
        # todo create dialog on the fly to speed up startup time
        self._makeButtonBar()
        self._makeMainPanel()
        self.setCentralWidget(self._makeWelcomePanel())
        self.localizeUi()

    def _fillMenu(self):
        menuBar = self.menuBar()
        menuBar.setGeometry(QRect(0, 0, 469, 21))
        self._fileMenu = QMenu(menuBar)
        self._fileMenu.setObjectName(FILE_MENU_NAME)
        self._importAction = QAction(self._fileMenu)
        self._importAction.setObjectName(IMPORT_TRACK_ACTION_NAME)
        self._importAction.triggered.connect(self._addFileDialog.open)
        self._fileMenu.addAction(self._importAction)
        menuBar.addMenu(self._fileMenu)

    def _makeStatusBar(self):
        self.setStatusBar(QStatusBar())

    def _makeImportFileDialog(self):
        self._addFileDialog = QFileDialog(self)
        self._addFileDialog.setObjectName(IMPORT_TRACK_DIALOG_NAME)
        self._addFileDialog.setDirectory(QDir.homePath())
        self._addFileDialog.setOption(QFileDialog.DontUseNativeDialog)
        self._addFileDialog.setModal(True)
        self._addFileDialog.fileSelected.connect(self._importTrackFile)

    def _importTrackFile(self, filename):
        self._musicDirector.importTrack(filename)

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

    def _trackPanel(self, index):
        return self._pages.widget(TRACK_PANEL + index)

    def _addTrackPage(self, track):
        trackPanel = TrackPanel()
        trackPanel.setTrack(track)
        self._pages.addWidget(trackPanel)

    def trackImported(self, track):
        self._trackListPanel().addTrack(track)

        if self._albumEmpty():
            self._showPage(TRACK_LIST_PANEL)
            self._albumPanel().setTrack(track)
            self.setCentralWidget(self._mainPanel)

        if self._onLastPage():
            self._nextStepButton.setEnabled(True)

        self._addTrackPage(track)
        self._tracks.append(track)

    def _albumEmpty(self):
        return not self._tracks

    def _makeMainPanel(self):
        self._mainPanel = QWidget()
        layout = QVBoxLayout()
        self._pages = QStackedWidget()
        trackListPanel = TrackListPanel(self._player)
        self._pages.addWidget(trackListPanel)
        albumPanel = AlbumPanel()
        self._pages.addWidget(albumPanel)
        layout.addWidget(self._pages)
        self._previousPageButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)
        layout.addWidget(self._buttonBar)
        self._mainPanel.setLayout(layout)

    def _currentPage(self):
        return self._pages.currentIndex()

    def _onFirstPage(self):
        return self._currentPage() == 0

    def _onLastPage(self):
        return self._currentPage() == self._pages.count() - 1

    def _previousPage(self):
        return self._currentPage() - 1

    def _nextPage(self):
        return self._currentPage() + 1

    def _showPage(self, page):
        self._pages.setCurrentIndex(page)

    def _showPreviousPage(self):
        self._showPage(self._previousPage())
        if self._onFirstPage():
            self._saveButton.setDisabled(True)
            self._previousPageButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)

    def _showNextPage(self):
        self._showPage(self._nextPage())
        if self._onLastPage():
            self._nextStepButton.setDisabled(True)
        self._previousPageButton.setEnabled(True)
        self._saveButton.setEnabled(True)

    def _updateAlbumWithMetadata(self):
        for index, track in enumerate(self._tracks):
            self._albumPanel().updateTrack(track)
            self._trackPanel(index).updateTrack(track)

    def _saveAlbum(self):
        self._updateAlbumWithMetadata()
        self._musicDirector.saveAlbum(self._tracks)

    # todo Extract a WelcomePanel
    def _makeWelcomePanel(self):
        self._welcomePanel = QWidget()
        layout = QHBoxLayout()
        layout.addStretch()
        self._addFileButton = QPushButton()
        self._addFileButton.setObjectName(ADD_FILE_BUTTON_NAME)
        self._addFileButton.clicked.connect(self._addFileDialog.open)
        layout.addWidget(self._addFileButton)
        layout.addStretch()
        self._welcomePanel.setLayout(layout)
        return self._welcomePanel

    def localizeUi(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._fileMenu.setTitle(self.tr('File'))
        self._importAction.setText(self.tr("Import File..."))
        self._addFileButton.setText(self.tr("Add File..."))
        self._saveButton.setText(self.tr("Save"))
        self._previousPageButton.setText(self.tr("Previous"))
        self._nextStepButton.setText(self.tr("Next"))
        self._addFileDialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")

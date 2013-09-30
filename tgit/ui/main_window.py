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
from PyQt4.QtGui import (QWidget, QMainWindow, QMenuBar, QMenu, QAction, QStatusBar, QGridLayout,
                         QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog)

from tgit.ui.album_panel import AlbumPanel
from tgit.ui.track_panel import TrackPanel

MAIN_WINDOW_NAME = "TGiT"
ADD_FILE_BUTTON_NAME = "Add File"
IMPORT_TRACK_DIALOG_NAME = "Select Track File"
NEXT_STEP_BUTTON_NAME = "Next Step"
PREVIOUS_STEP_BUTTON_NAME = "Previous Step"
SAVE_BUTTON_NAME = "Save"


class MainWindow(QMainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self._musicDirector = None
        self._setupUi()
        self.show()
        self.raise_()
        self.activateWindow()

    def _setupUi(self):
        self.setObjectName(MAIN_WINDOW_NAME)
        self.resize(640, 480)
        self._fillMenu()
        self._makeStatusBar()
        # todo create dialog on the fly to speed up startup time
        self._makeImportFileDialog()
        self._makeWelcomePanel()
        self._albumPanel = AlbumPanel()
        self._trackPanel = TrackPanel()
        self.setCentralWidget(self._welcomePanel)
        self._makeButtonBar()
        self.localizeUi()

    def _fillMenu(self):
        menuBar = QMenuBar()
        menuBar.setGeometry(QRect(0, 0, 469, 21))
        self._quitMenu = QMenu(menuBar)
        self._quitMenuItem = QAction(self._quitMenu)
        self._quitMenuItem.triggered.connect(self.close)
        self._quitMenu.addAction(self._quitMenuItem)
        self.setMenuBar(menuBar)
        menuBar.addAction(self._quitMenu.menuAction())

    def _makeStatusBar(self):
        self.setStatusBar(QStatusBar())

    # todo Extract a WelcomePanel
    def _makeWelcomePanel(self):
        self._welcomePanel = QWidget()
        layout = QGridLayout(self._welcomePanel)
        self._welcomePanel.setLayout(layout)
        self._addFileButton = QPushButton()
        self._addFileButton.setObjectName(ADD_FILE_BUTTON_NAME)
        self._addFileButton.clicked.connect(self._addFileDialog.open)
        layout.addWidget(self._addFileButton, 0, 0)

    def _makeImportFileDialog(self):
        self._addFileDialog = QFileDialog(self)
        self._addFileDialog.setObjectName(IMPORT_TRACK_DIALOG_NAME)
        self._addFileDialog.setDirectory(QDir.homePath())
        self._addFileDialog.setOption(QFileDialog.DontUseNativeDialog)
        self._addFileDialog.setModal(True)
        self._addFileDialog.fileSelected.connect(self._importTrackFile)

    def _importTrackFile(self, filename):
        if self._musicDirector:
            self._musicDirector.importTrack(filename)

    def _makeButtonBar(self):
        self._buttonBar = QWidget()
        layout = QHBoxLayout()
        self._buttonBar.setLayout(layout)
        self._previousStepButton = QPushButton()
        self._previousStepButton.setObjectName(PREVIOUS_STEP_BUTTON_NAME)
        self._previousStepButton.clicked.connect(self._showAlbumPanel)
        layout.addWidget(self._previousStepButton)
        self._saveButton = QPushButton()
        self._saveButton.setObjectName(SAVE_BUTTON_NAME)
        self._saveButton.clicked.connect(self._saveTrackFile)
        layout.addWidget(self._saveButton)
        self._nextStepButton = QPushButton()
        self._nextStepButton.setObjectName(NEXT_STEP_BUTTON_NAME)
        self._nextStepButton.clicked.connect(self._showTrackPanel)
        layout.addWidget(self._nextStepButton)

    def _saveTrackFile(self):
        if self._albumPanel:
            self._albumPanel.updateTrack(self._track)
        if self._trackPanel:
            self._trackPanel.updateTrack(self._track)
        if self._musicDirector:
            self._musicDirector.saveTrack(self._track)

    def addMusicDirector(self, director):
        self._musicDirector = director

    def trackSelected(self, track):
        self._track = track
        # todo should panels really be responsible for maintaining edition state?
        self._albumPanel.setTrack(self._track)
        self._trackPanel.setTrack(self._track)
        self._showAlbumPanel()

    # todo is there any better way to do this?
    def _notToBeDestroyed(self, widget):
        # transfer ownership to PyQt to avoid Qt to destroy QObject that is not in any layout
        widget.setParent(None)

    def _showAlbumPanel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self._albumPanel)
        layout.addStretch()
        self._previousStepButton.setDisabled(True)
        self._nextStepButton.setEnabled(True)
        layout.addWidget(self._buttonBar)
        panel.setLayout(layout)
        self.setCentralWidget(panel)
        self._notToBeDestroyed(self._trackPanel)

    def _showTrackPanel(self):
        self._albumPanel.updateTrack(self._track)
        panel = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self._trackPanel)
        layout.addStretch()
        self._previousStepButton.setEnabled(True)
        self._nextStepButton.setDisabled(True)
        layout.addWidget(self._buttonBar)
        panel.setLayout(layout)
        self.setCentralWidget(panel)
        self._notToBeDestroyed(self._albumPanel)

    def localizeUi(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._addFileButton.setText(self.tr("Add File..."))
        self._quitMenu.setTitle(self.tr("Quit"))
        self._quitMenuItem.setText(self.tr("Hit me to quit"))
        self._saveButton.setText(self.tr("Save"))
        self._previousStepButton.setText(self.tr("Previous"))
        self._nextStepButton.setText(self.tr("Next"))
        self._addFileDialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")

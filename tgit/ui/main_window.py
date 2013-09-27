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

from PyQt4.QtCore import (Qt, QDir, QRect)
from PyQt4.QtGui import (QWidget, QMainWindow, QMenuBar, QMenu, QAction, QStatusBar, QGridLayout,
                         QLabel, QPushButton, QLineEdit, QFileDialog, QPixmap, QImage)

from tgit.ui.album_panel import AlbumPanel

MAIN_WINDOW_NAME = "TGiT"
ADD_FILE_BUTTON_NAME = "Add File"
NEXT_STEP_BUTTON_NAME = "Next Step"
SAVE_BUTTON_NAME = "Save"

IMPORT_TRACK_DIALOG_NAME = "Select Track File"

RELEASE_DATE_NAME = "Release Date"
UPC_NAME = "UPC"
TRACK_TITLE_NAME = "Track Title"
VERSION_INFO_NAME = "Version Info"
FEATURED_GUEST_NAME = "Featured Guest"
ISRC_NAME = "ISRC"
BITRATE_NAME = "Bitrate"
DURATION_NAME = "Duration"


def toKbps(bitrate):
    return int(round(bitrate, -3) / 1000)


def secondsAsText(seconds):
    return "%02d:%02d" % divmod(round(seconds), 60)


# todo start teasing apart the main window to get birth to the domain concepts
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
        self._makeImportFileDialog()
        self.setCentralWidget(self._makeWelcomePanel())
        self._makeTagAlbumPanel()
        self._fillMenu()
        self._makeStatusBar()
        self.localizeUi()

    def _makeStatusBar(self):
        self.setStatusBar(QStatusBar(self))

    def _makeWelcomePanel(self):
        self._welcomePanel = QWidget()
        welcomePanelLayout = QGridLayout(self._welcomePanel)
        self._addFileButton = QPushButton(self._welcomePanel)
        self._addFileButton.setObjectName(ADD_FILE_BUTTON_NAME)
        self._addFileButton.clicked.connect(self._addFileDialog.open)
        welcomePanelLayout.addWidget(self._addFileButton, 0, 0, 1, 1)
        return self._welcomePanel

    def _makeTagAlbumPanel(self):
        self._tagAlbumPanel = QWidget()
        tagAlbumLayout = QGridLayout(self._tagAlbumPanel)
        self._albumPanel = AlbumPanel(self)
        tagAlbumLayout.addWidget(self._albumPanel, 0, 0, 3, 3)
        self._addReleaseDate(tagAlbumLayout, 3)
        self._addUpc(tagAlbumLayout, 4)
        self._addTrackTitle(tagAlbumLayout, 5)
        self._addVersionInfo(tagAlbumLayout, 6)
        self._addFeaturedGuest(tagAlbumLayout, 7)
        self._addIsrc(tagAlbumLayout, 8)
        self._addBitrate(tagAlbumLayout, 9)
        self._addDuration(tagAlbumLayout, 10)
        self._addButtons(tagAlbumLayout, 11)
        return self._tagAlbumPanel

    def _addReleaseDate(self, layout, row):
        self._releaseDateLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._releaseDateLabel, row, 0, 1, 1)
        self._releaseDateEdit = QLineEdit(self._tagAlbumPanel)
        self._releaseDateEdit.setObjectName(RELEASE_DATE_NAME)
        layout.addWidget(self._releaseDateEdit, row, 1, 1, 1)
        self._releaseDateLabel.setBuddy(self._releaseDateEdit)

    def _addUpc(self, layout, row):
        self._upcLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._upcLabel, row, 0, 1, 1)
        self._upcEdit = QLineEdit(self._tagAlbumPanel)
        self._upcEdit.setObjectName(UPC_NAME)
        layout.addWidget(self._upcEdit, row, 1, 1, 1)
        self._upcLabel.setBuddy(self._upcEdit)

    def _addTrackTitle(self, layout, row):
        self._trackTitleLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._trackTitleLabel, row, 0, 1, 1)
        self._trackTitleEdit = QLineEdit(self._tagAlbumPanel)
        self._trackTitleEdit.setObjectName(TRACK_TITLE_NAME)
        layout.addWidget(self._trackTitleEdit, row, 1, 1, 1)
        self._trackTitleLabel.setBuddy(self._trackTitleEdit)

    def _addVersionInfo(self, layout, row):
        self._versionInfoLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._versionInfoLabel, row, 0, 1, 1)
        self._versionInfoEdit = QLineEdit(self._tagAlbumPanel)
        self._versionInfoEdit.setObjectName(VERSION_INFO_NAME)
        layout.addWidget(self._versionInfoEdit, row, 1, 1, 1)
        self._versionInfoLabel.setBuddy(self._versionInfoEdit)

    def _addFeaturedGuest(self, layout, row):
        self._featuredGuestLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._featuredGuestLabel, row, 0, 1, 1)
        self._featuredGuestEdit = QLineEdit(self._tagAlbumPanel)
        self._featuredGuestEdit.setObjectName(FEATURED_GUEST_NAME)
        layout.addWidget(self._featuredGuestEdit, row, 1, 1, 1)
        self._featuredGuestLabel.setBuddy(self._featuredGuestEdit)

    def _addIsrc(self, layout, row):
        self._isrcLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._isrcLabel, row, 0, 1, 1)
        self._isrcEdit = QLineEdit(self._tagAlbumPanel)
        self._isrcEdit.setObjectName(ISRC_NAME)
        layout.addWidget(self._isrcEdit, row, 1, 1, 1)
        self._isrcLabel.setBuddy(self._isrcEdit)

    def _addBitrate(self, layout, row):
        self._bitrateLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._bitrateLabel, row, 0, 1, 1)
        self._bitrateInfoLabel = QLabel(self._tagAlbumPanel)
        self._bitrateInfoLabel.setObjectName(BITRATE_NAME)
        layout.addWidget(self._bitrateInfoLabel, row, 1, 1, 1)
        self._bitrateLabel.setBuddy(self._bitrateInfoLabel)

    def _addDuration(self, layout, row):
        self._durationLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._durationLabel, row, 0, 1, 1)
        self._durationInfoLabel = QLabel(self._tagAlbumPanel)
        self._durationInfoLabel.setObjectName(DURATION_NAME)
        layout.addWidget(self._durationInfoLabel, row, 1, 1, 1)
        self._durationLabel.setBuddy(self._durationInfoLabel)

    def _addButtons(self, layout, row):
        self._saveButton = QPushButton(self._tagAlbumPanel)
        self._saveButton.setObjectName(SAVE_BUTTON_NAME)
        self._saveButton.clicked.connect(self._saveTrackFile)
        layout.addWidget(self._saveButton, row, 1)
        self._nextStepButton = QPushButton(self._tagAlbumPanel)
        self._nextStepButton.setObjectName(NEXT_STEP_BUTTON_NAME)
        layout.addWidget(self._nextStepButton, row, 2)

    def _fillMenu(self):
        menuBar = QMenuBar(self)
        menuBar.setGeometry(QRect(0, 0, 469, 21))
        self._quitMenu = QMenu(menuBar)
        self._quitMenuItem = QAction(self)
        self._quitMenuItem.triggered.connect(self.close)
        self._quitMenu.addAction(self._quitMenuItem)
        self.setMenuBar(menuBar)
        menuBar.addAction(self._quitMenu.menuAction())

    # todo integration test dialog file name filtering by making sure the Accept button stay
    # disabled when we select a non supported file type
    def _makeImportFileDialog(self):
        self._addFileDialog = QFileDialog(self)
        self._addFileDialog.setObjectName(IMPORT_TRACK_DIALOG_NAME)
        self._addFileDialog.setDirectory(QDir.homePath())
        self._addFileDialog.setOption(QFileDialog.DontUseNativeDialog)
        self._addFileDialog.setModal(True)
        self._addFileDialog.fileSelected.connect(self._importTrackFile)

    def _showTagAlbumPanel(self):
        self.setCentralWidget(self._tagAlbumPanel)

    def _importTrackFile(self, filename):
        if self._musicDirector:
            self._musicDirector.importTrack(filename)

    def _saveTrackFile(self):
        self._albumPanel.updateTrack(self._track)
        self._track.releaseDate = self._releaseDateEdit.text()
        self._track.upc = self._upcEdit.text()
        self._track.trackTitle = self._trackTitleEdit.text()
        self._track.versionInfo = self._versionInfoEdit.text()
        self._track.featuredGuest = self._featuredGuestEdit.text()
        self._track.isrc = self._isrcEdit.text()
        if self._musicDirector:
            self._musicDirector.saveTrack(self._track)

    def addMusicDirector(self, director):
        self._musicDirector = director

    def trackSelected(self, track):
        self._track = track
        self._albumPanel.trackSelected(track)
        self._releaseDateEdit.setText(track.releaseDate)
        self._upcEdit.setText(track.upc)
        self._trackTitleEdit.setText(track.trackTitle)
        self._versionInfoEdit.setText(track.versionInfo)
        self._featuredGuestEdit.setText(track.featuredGuest)
        self._isrcEdit.setText(track.isrc)
        self._bitrateInfoLabel.setText("%s kbps" % toKbps(track.bitrate))
        self._durationInfoLabel.setText(secondsAsText(track.duration))
        self._showTagAlbumPanel()

    def localizeUi(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._addFileButton.setText(self.tr("Add File..."))
        self._quitMenu.setTitle(self.tr("Quit"))
        self._quitMenuItem.setText(self.tr("Hit me to quit"))
        self._releaseDateLabel.setText(self.tr("Release Date: "))
        self._upcLabel.setText(self.tr("UPC/EAN: "))
        self._trackTitleLabel.setText(self.tr("Track Title: "))
        self._versionInfoLabel.setText(self.tr("Version Information: "))
        self._featuredGuestLabel.setText(self.tr("Featured Guest: "))
        self._isrcLabel.setText(self.tr("ISRC: "))
        self._bitrateLabel.setText(self.tr("Bitrate: "))
        self._durationLabel.setText(self.tr("Duration: "))
        self._saveButton.setText(self.tr("Save"))
        self._nextStepButton.setText(self.tr("Next"))
        self._addFileDialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")

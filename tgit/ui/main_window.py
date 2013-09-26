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

import mimetypes
from PyQt4.QtCore import (Qt, QDir, QRect)
from PyQt4.QtGui import (QWidget, QMainWindow, QMenuBar, QMenu, QAction, QStatusBar, QGridLayout,
                         QLabel, QPushButton, QLineEdit, QFileDialog, QPixmap, QImage)

from tgit.mp3 import MP3File

MAIN_WINDOW_NAME = "TGiT"
ADD_FILE_BUTTON_NAME = "Add File"
IMPORT_TRACK_DIALOG_NAME = "Select Track File"
SELECT_PICTURE_BUTTON_NAME = "Select Picture"
SELECT_PICTURE_DIALOG_NAME = "Select Picture File"
FRONT_COVER_PICTURE_NAME = "Front Cover Picture"
FRONT_COVER_EMBEDDED_TEXT_NAME = "Front Cover Embedded Text"
RELEASE_NAME_NAME = "Release Name"
LEAD_PERFORMER_NAME = "Lead Performer"
RELEASE_DATE_NAME = "Release Date"
UPC_NAME = "UPC"
TRACK_TITLE_NAME = "Track Title"
VERSION_INFO_NAME = "Version Info"
FEATURED_GUEST_NAME = "Featured Guest"
ISRC_NAME = "ISRC"
BITRATE_NAME = "Bitrate"
DURATION_NAME = "Duration"
SAVE_BUTTON_NAME = "Save"


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
        self._makeSelectPictureDialog()
        self.setCentralWidget(self._makeWelcomePanel())
        self._makeTagAlbumPanel()
        self._fillMenu()
        self._makeStatusBar()
        self.localizeUi()

    def addMusicDirector(self, director):
        self._musicDirector = director

    def trackSelected(self, track):
        self._releaseNameEdit.setText(track.releaseName)
        self._displayFrontCover(track.frontCoverPicture)
        self._leadPerformerEdit.setText(track.leadPerformer)
        self._releaseDateEdit.setText(track.releaseDate)
        self._upcEdit.setText(track.upc)
        self._showTagAlbumPanel()

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
        self._addFrontCoverPicture(tagAlbumLayout, 0)
        self._addReleaseName(tagAlbumLayout, 2)
        self._addLeadPerformer(tagAlbumLayout, 3)
        self._addReleaseDate(tagAlbumLayout, 4)
        self._addUpc(tagAlbumLayout, 5)
        self._addTrackTitle(tagAlbumLayout, 6)
        self._addVersionInfo(tagAlbumLayout, 7)
        self._addFeaturedGuest(tagAlbumLayout, 8)
        self._addIsrc(tagAlbumLayout, 9)
        self._addBitrate(tagAlbumLayout, 10)
        self._addDuration(tagAlbumLayout, 11)
        self._addButtons(tagAlbumLayout, 12)
        return self._tagAlbumPanel

    def _addFrontCoverPicture(self, layout, row):
        self._frontCoverImage = QLabel(self._tagAlbumPanel)
        self._frontCoverImage.setObjectName(FRONT_COVER_PICTURE_NAME)
        layout.addWidget(self._frontCoverImage, row, 0, 1, 1)
        self._selectPictureButton = QPushButton(self._tagAlbumPanel)
        self._selectPictureButton.setObjectName(SELECT_PICTURE_BUTTON_NAME)
        self._selectPictureButton.clicked.connect(self._selectPictureDialog.open)
        layout.addWidget(self._selectPictureButton, row, 1, 1, 1)
        self._frontCoverTextLabel = QLabel(self._tagAlbumPanel)
        self._frontCoverTextLabel.setObjectName(FRONT_COVER_EMBEDDED_TEXT_NAME)
        layout.addWidget(self._frontCoverTextLabel, row + 1, 0, 1, 1)

    def _addReleaseName(self, layout, row):
        self._releaseNameLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._releaseNameLabel, row, 0, 1, 1)
        self._releaseNameEdit = QLineEdit(self._tagAlbumPanel)
        self._releaseNameEdit.setObjectName(RELEASE_NAME_NAME)
        layout.addWidget(self._releaseNameEdit, row, 1, 1, 1)
        self._releaseNameLabel.setBuddy(self._releaseNameEdit)

    def _addLeadPerformer(self, layout, row):
        self._leadPerformerLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._leadPerformerLabel, row, 0, 1, 1)
        self._leadPerformerEdit = QLineEdit(self._tagAlbumPanel)
        self._leadPerformerEdit.setObjectName(LEAD_PERFORMER_NAME)
        layout.addWidget(self._leadPerformerEdit, row, 1, 1, 1)
        self._leadPerformerLabel.setBuddy(self._leadPerformerEdit)

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

    def _addVersionInfo(self, layout, row):
        self._versionInfoLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._versionInfoLabel, row, 0, 1, 1)
        self._versionInfoEdit = QLineEdit(self._tagAlbumPanel)
        self._versionInfoEdit.setObjectName(VERSION_INFO_NAME)
        layout.addWidget(self._versionInfoEdit, row, 1, 1, 1)

    def _addFeaturedGuest(self, layout, row):
        self._featuredGuestLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._featuredGuestLabel, row, 0, 1, 1)
        self._featuredGuestEdit = QLineEdit(self._tagAlbumPanel)
        self._featuredGuestEdit.setObjectName(FEATURED_GUEST_NAME)
        layout.addWidget(self._featuredGuestEdit, row, 1, 1, 1)

    def _addIsrc(self, layout, row):
        self._isrcLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._isrcLabel, row, 0, 1, 1)
        self._isrcEdit = QLineEdit(self._tagAlbumPanel)
        self._isrcEdit.setObjectName(ISRC_NAME)
        layout.addWidget(self._isrcEdit, row, 1, 1, 1)

    def _addBitrate(self, layout, row):
        self._bitrateLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._bitrateLabel, row, 0, 1, 1)
        self._bitrateInfoLabel = QLabel(self._tagAlbumPanel)
        self._bitrateInfoLabel.setObjectName(BITRATE_NAME)
        layout.addWidget(self._bitrateInfoLabel, row, 1, 1, 1)

    def _addDuration(self, layout, row):
        self._durationLabel = QLabel(self._tagAlbumPanel)
        layout.addWidget(self._durationLabel, row, 0, 1, 1)
        self._durationInfoLabel = QLabel(self._tagAlbumPanel)
        self._durationInfoLabel.setObjectName(DURATION_NAME)
        layout.addWidget(self._durationInfoLabel, row, 1, 1, 1)

    def _addButtons(self, layout, row):
        self._saveButton = QPushButton(self._tagAlbumPanel)
        self._saveButton.setObjectName(SAVE_BUTTON_NAME)
        self._saveButton.clicked.connect(self._saveTrackFile)
        layout.addWidget(self._saveButton, row, 0, 1, 1)

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

    # todo integration test dialog file name filtering by making sure the Accept button stay
    # disabled when we select a non supported file type
    def _makeSelectPictureDialog(self):
        self._selectPictureDialog = QFileDialog(self)
        self._selectPictureDialog.setObjectName(SELECT_PICTURE_DIALOG_NAME)
        self._selectPictureDialog.setDirectory(QDir.homePath())
        self._selectPictureDialog.setOption(QFileDialog.DontUseNativeDialog)
        self._selectPictureDialog.setModal(True)
        self._selectPictureDialog.fileSelected.connect(self._loadFrontCoverPicture)

    def _loadFrontCoverPicture(self, filename):
        self._displayFrontCover(self._loadPicture(filename))

    def _displayFrontCover(self, picture):
        self._frontCover = picture
        _, imageData = self._frontCover
        self._frontCoverImage.setPixmap(self._scaledPixmapFrom(imageData))
        self._frontCoverTextLabel.setText(self._getEmbeddedText(imageData))

    def _showTagAlbumPanel(self):
        self.setCentralWidget(self._tagAlbumPanel)

    def _importTrackFile(self, filename):
        if self._musicDirector:
            self._musicDirector.importTrack(filename)
        self._audio = MP3File(filename)
        self._trackTitleEdit.setText(self._audio.trackTitle)
        self._versionInfoEdit.setText(self._audio.versionInfo)
        self._featuredGuestEdit.setText(self._audio.featuredGuest)
        self._isrcEdit.setText(self._audio.isrc)
        self._bitrateInfoLabel.setText("%d kbps" % self._audio.bitrateInKbps)
        self._durationInfoLabel.setText(self._audio.durationAsText)
        self.trackSelected(self._audio)

    def _getEmbeddedText(self, imageData):
        return QImage.fromData(imageData).text()

    def _scaledPixmapFrom(self, imageData):
        if imageData is None:
            return QPixmap()
        originalImage = QImage.fromData(imageData)
        scaledImage = originalImage.scaled(125, 125, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return QPixmap.fromImage(scaledImage)

    def _saveTrackFile(self):
        self._audio.releaseName = self._releaseNameEdit.text()
        self._audio.frontCoverPicture = self._frontCover
        self._audio.leadPerformer = self._leadPerformerEdit.text()
        self._audio.releaseDate = self._releaseDateEdit.text()
        self._audio.upc = self._upcEdit.text()
        self._audio.trackTitle = self._trackTitleEdit.text()
        self._audio.versionInfo = self._versionInfoEdit.text()
        self._audio.featuredGuest = self._featuredGuestEdit.text()
        self._audio.isrc = self._isrcEdit.text()
        self._audio.save()

    def _loadPicture(self, filename):
        if filename is None:
            return None, None
        mimeType = mimetypes.guess_type(filename)
        imageData = open(filename, "rb").read()
        return mimeType[0], imageData

    def localizeUi(self):
        self.setWindowTitle(self.tr("TGiT"))
        self._addFileButton.setText(self.tr("Add File..."))
        self._quitMenu.setTitle(self.tr("Quit"))
        self._quitMenuItem.setText(self.tr("Hit me to quit"))
        self._releaseNameLabel.setText(self.tr("Release Name: "))
        self._leadPerformerLabel.setText(self.tr("Lead Performer: "))
        self._releaseDateLabel.setText(self.tr("Release Date: "))
        self._upcLabel.setText(self.tr("UPC/EAN: "))
        self._trackTitleLabel.setText(self.tr("Track Title: "))
        self._versionInfoLabel.setText(self.tr("Version Information: "))
        self._featuredGuestLabel.setText(self.tr("Featured Guest: "))
        self._isrcLabel.setText(self.tr("ISRC: "))
        self._bitrateLabel.setText(self.tr("Bitrate: "))
        self._durationLabel.setText(self.tr("Duration: "))
        self._saveButton.setText(self.tr("Save"))
        self._addFileDialog.setNameFilter(self.tr("MP3 files") + " (*.mp3)")
        self._selectPictureButton.setText(self.tr("Select Picture..."))
        self._selectPictureDialog.setNameFilter(self.tr("Image files") + " (*.png *.jpeg *.jpg)")
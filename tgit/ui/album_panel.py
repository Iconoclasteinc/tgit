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
from PyQt4.QtCore import Qt, QDir
from PyQt4.QtGui import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QPixmap, QImage,
                         QFileDialog, QHBoxLayout, QVBoxLayout)

ALBUM_PANEL_NAME = 'Album Panel'
FRONT_COVER_PICTURE_NAME = "Front Cover Picture"
FRONT_COVER_DISPLAY_SIZE = (125, 125)
SELECT_PICTURE_BUTTON_NAME = "Select Picture"
SELECT_PICTURE_DIALOG_NAME = "Select Picture File"
RELEASE_NAME_NAME = 'Release Name'
LEAD_PERFORMER_NAME = "Lead Performer"
GUEST_PERFORMERS_NAME = "Guest Performers"
LABEL_NAME_NAME = "Label Name"
RECORDING_TIME_NAME = "Recording Time"
RELEASE_TIME_NAME = "Release Time"
ORIGINAL_RELEASE_TIME_NAME = "Original Release Time"
UPC_NAME = "UPC"


class AlbumPanel(QWidget):
    def __init__(self, album, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_PANEL_NAME)
        grid = QGridLayout()
        self._fill(grid)
        self.translateUi()
        self._layout(grid)
        self._album = album
        self.albumStateChanged(album)

    def _layout(self, grid):
        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def _loadFrontCoverPicture(self, filename):
        self._changeFrontCover(self._loadPicture(filename))

    def _loadPicture(self, filename):
        if filename is None:
            return None, None
        mimeType = mimetypes.guess_type(filename)
        imageData = open(filename, "rb").read()
        return mimeType[0], imageData

    def _changeFrontCover(self, picture):
        self._frontCover = picture
        _, imageData = self._frontCover
        self._frontCoverImage.setPixmap(self._scaleToDisplayArea(imageData))
        self.updateAlbum()

    def _scaleToDisplayArea(self, imageData):
        if imageData is None:
            return QPixmap()
        image = self._scaleImage(QImage.fromData(imageData), *FRONT_COVER_DISPLAY_SIZE)
        return QPixmap.fromImage(image)

    def _scaleImage(self, image, width, height):
        return image.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def _fill(self, layout):
        self._addFrontCoverPictureTo(layout, 0)
        self._addReleaseNameTo(layout, 1)
        self._addLeadPerformerTo(layout, 2)
        self._addGuestPerformersTo(layout, 3)
        self._addLabelNameTo(layout, 4)
        self._addRecordingTimeTo(layout, 5)
        self._addReleaseTimeTo(layout, 6)
        self._addOriginalReleaseTimeTo(layout, 7)
        self._addUpc(layout, 8)

    def _addFrontCoverPictureTo(self, layout, row):
        self._frontCoverImage = QLabel()
        self._frontCoverImage.setFixedSize(*FRONT_COVER_DISPLAY_SIZE)
        self._frontCoverImage.setObjectName(FRONT_COVER_PICTURE_NAME)
        layout.addWidget(self._frontCoverImage, row, 0)
        self._selectPictureButton = QPushButton()
        self._selectPictureButton.setObjectName(SELECT_PICTURE_BUTTON_NAME)
        self._selectPictureButton.clicked.connect(self._selectPicture)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._selectPictureButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout, row, 1)

    def _makeSelectPictureDialog(self):
        dialog = QFileDialog(self)
        dialog.setObjectName(SELECT_PICTURE_DIALOG_NAME)
        dialog.setDirectory(QDir.homePath())
        dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setNameFilter(self.tr("Image files") + " (*.png *.jpeg *.jpg)")
        dialog.setModal(True)
        dialog.fileSelected.connect(self._loadFrontCoverPicture)
        return dialog

    def _selectPicture(self):
        if not hasattr(self, '_selectPictureDialog'):
            self._selectPictureDialog = self._makeSelectPictureDialog()
        self._selectPictureDialog.open()

    def _addReleaseNameTo(self, layout, row):
        self._releaseNameLabel = QLabel()
        layout.addWidget(self._releaseNameLabel, row, 0)
        self._releaseNameEdit = QLineEdit()
        self._releaseNameEdit.setObjectName(RELEASE_NAME_NAME)
        self._releaseNameEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._releaseNameEdit, row, 1)
        self._releaseNameLabel.setBuddy(self._releaseNameEdit)

    def _addLeadPerformerTo(self, layout, row):
        self._leadPerformerLabel = QLabel()
        layout.addWidget(self._leadPerformerLabel, row, 0)
        self._leadPerformerEdit = QLineEdit()
        self._leadPerformerEdit.setObjectName(LEAD_PERFORMER_NAME)
        self._leadPerformerEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._leadPerformerEdit, row, 1)
        self._leadPerformerLabel.setBuddy(self._leadPerformerEdit)

    def _addGuestPerformersTo(self, layout, row):
        self._guestPerformersLabel = QLabel()
        layout.addWidget(self._guestPerformersLabel, row, 0)
        self._guestPerformersEdit = QLineEdit()
        self._guestPerformersEdit.setObjectName(GUEST_PERFORMERS_NAME)
        self._guestPerformersEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._guestPerformersEdit, row, 1)
        self._guestPerformersLabel.setBuddy(self._guestPerformersEdit)

    def _addLabelNameTo(self, layout, row):
        self._labelNameLabel = QLabel()
        layout.addWidget(self._labelNameLabel, row, 0)
        self._labelNameEdit = QLineEdit()
        self._labelNameEdit.setObjectName(LABEL_NAME_NAME)
        self._labelNameEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._labelNameEdit, row, 1)
        self._labelNameLabel.setBuddy(self._labelNameEdit)

    def _addRecordingTimeTo(self, layout, row):
        self._recordingTimeLabel = QLabel()
        layout.addWidget(self._recordingTimeLabel, row, 0)
        self._recordingTimeEdit = QLineEdit()
        self._recordingTimeEdit.setObjectName(RECORDING_TIME_NAME)
        self._recordingTimeEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._recordingTimeEdit, row, 1)
        self._recordingTimeLabel.setBuddy(self._recordingTimeEdit)

    def _addReleaseTimeTo(self, layout, row):
        self._releaseTimeLabel = QLabel()
        layout.addWidget(self._releaseTimeLabel, row, 0)
        self._releaseTimeEdit = QLineEdit()
        self._releaseTimeEdit.setObjectName(RELEASE_TIME_NAME)
        self._releaseTimeEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._releaseTimeEdit, row, 1)
        self._releaseTimeLabel.setBuddy(self._releaseTimeEdit)

    def _addOriginalReleaseTimeTo(self, layout, row):
        self._originalReleaseTimeLabel = QLabel()
        layout.addWidget(self._originalReleaseTimeLabel, row, 0)
        self._originalReleaseTimeEdit = QLineEdit()
        self._originalReleaseTimeEdit.setObjectName(ORIGINAL_RELEASE_TIME_NAME)
        self._originalReleaseTimeEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._originalReleaseTimeEdit, row, 1)
        self._originalReleaseTimeLabel.setBuddy(self._originalReleaseTimeEdit)

    def _addUpc(self, layout, row):
        self._upcLabel = QLabel()
        layout.addWidget(self._upcLabel, row, 0)
        self._upcEdit = QLineEdit()
        self._upcEdit.setObjectName(UPC_NAME)
        self._upcEdit.textEdited.connect(self.updateAlbum)
        layout.addWidget(self._upcEdit, row, 1)
        self._upcLabel.setBuddy(self._upcEdit)

    def translateUi(self):
        self._selectPictureButton.setText(self.tr("Select Picture..."))
        self._releaseNameLabel.setText(self.tr("Release Name: "))
        self._leadPerformerLabel.setText(self.tr("Lead Performer: "))
        self._guestPerformersLabel.setText(self.tr("Guest Performers: "))
        self._labelNameLabel.setText(self.tr("Label Name: "))
        self._recordingTimeLabel.setText(self.tr("Recording Time: "))
        self._releaseTimeLabel.setText(self.tr("Release Time: "))
        self._originalReleaseTimeLabel.setText(self.tr("Original Release Time: "))
        self._upcLabel.setText(self.tr("UPC/EAN: "))

    def albumStateChanged(self, album):
        self._changeFrontCover(album.frontCoverPicture)
        self._releaseNameEdit.setText(album.releaseName)
        self._leadPerformerEdit.setText(album.leadPerformer)
        self._guestPerformersEdit.setText(album.guestPerformers)
        self._labelNameEdit.setText(album.labelName)
        self._recordingTimeEdit.setText(album.recordingTime)
        self._releaseTimeEdit.setText(album.releaseTime)
        self._originalReleaseTimeEdit.setText(album.originalReleaseTime)
        self._upcEdit.setText(album.upc)

    def updateAlbum(self):
        self._album.frontCoverPicture = self._frontCover
        self._album.releaseName = self._releaseNameEdit.text()
        self._album.leadPerformer = self._leadPerformerEdit.text()
        self._album.guestPerformers = self._guestPerformersEdit.text()
        self._album.labelName = self._labelNameEdit.text()
        self._album.recordingTime = self._recordingTimeEdit.text()
        self._album.releaseTime = self._releaseTimeEdit.text()
        self._album.originalReleaseTime = self._originalReleaseTimeEdit.text()
        self._album.upc = self._upcEdit.text()
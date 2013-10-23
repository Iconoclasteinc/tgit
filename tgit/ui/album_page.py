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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QPixmap, QImage,
                         QHBoxLayout, QVBoxLayout)

from tgit.file_chooser import FileChoiceListener
from tgit.ui import constants as ui


class AlbumPage(QWidget, FileChoiceListener):
    def __init__(self, album, pictureChooser, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._pictureChooser = pictureChooser
        self._pictureChooser.addChoiceListener(self)

        self.setObjectName(ui.ALBUM_PAGE_NAME)
        grid = QGridLayout()
        self._fill(grid)
        self.translateUi()
        self._layout(grid)
        self.albumStateChanged(album)

    def _layout(self, grid):
        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def fileChosen(self, filename):
        self._frontCover = self._loadImage(filename)
        self._displayFrontCover(self._frontCover)
        self._updateAlbumCover()

    def _loadImage(self, filename):
        if filename is None:
            return None

        mimeType = mimetypes.guess_type(filename)
        imageData = open(filename, "rb").read()
        return mimeType[0], imageData

    def _displayFrontCover(self, image):
        self._frontCoverPixmap.setPixmap(self._scaleToDisplayArea(image))

    def _scaleToDisplayArea(self, image):
        if image is None:
            return QPixmap()

        _, imageData = image
        scaledImage = self._scaleImage(QImage.fromData(imageData), *ui.FRONT_COVER_PIXMAP_SIZE)
        return QPixmap.fromImage(scaledImage)

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
        self._frontCoverPixmap = QLabel()
        self._frontCoverPixmap.setFixedSize(*ui.FRONT_COVER_PIXMAP_SIZE)
        self._frontCoverPixmap.setObjectName(ui.FRONT_COVER_PIXMAP_NAME)
        layout.addWidget(self._frontCoverPixmap, row, 0)
        self._selectPictureButton = QPushButton()
        self._selectPictureButton.setObjectName(ui.SELECT_PICTURE_BUTTON_NAME)
        self._selectPictureButton.clicked.connect(self._selectPicture)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._selectPictureButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout, row, 1)

    def _selectPicture(self):
        self._pictureChooser.chooseFile()

    def _addReleaseNameTo(self, layout, row):
        self._releaseNameLabel = QLabel()
        layout.addWidget(self._releaseNameLabel, row, 0)
        self._releaseNameEdit = QLineEdit()
        self._releaseNameEdit.setObjectName(ui.RELEASE_NAME_EDIT_NAME)
        self._releaseNameEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._releaseNameEdit, row, 1)
        self._releaseNameLabel.setBuddy(self._releaseNameEdit)

    def _addLeadPerformerTo(self, layout, row):
        self._leadPerformerLabel = QLabel()
        layout.addWidget(self._leadPerformerLabel, row, 0)
        self._leadPerformerEdit = QLineEdit()
        self._leadPerformerEdit.setObjectName(ui.LEAD_PERFORMER_EDIT_NAME)
        self._leadPerformerEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._leadPerformerEdit, row, 1)
        self._leadPerformerLabel.setBuddy(self._leadPerformerEdit)

    def _addGuestPerformersTo(self, layout, row):
        self._guestPerformersLabel = QLabel()
        layout.addWidget(self._guestPerformersLabel, row, 0)
        self._guestPerformersEdit = QLineEdit()
        self._guestPerformersEdit.setObjectName(ui.GUEST_PERFORMERS_EDIT_NAME)
        self._guestPerformersEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._guestPerformersEdit, row, 1)
        self._guestPerformersLabel.setBuddy(self._guestPerformersEdit)

    def _addLabelNameTo(self, layout, row):
        self._labelNameLabel = QLabel()
        layout.addWidget(self._labelNameLabel, row, 0)
        self._labelNameEdit = QLineEdit()
        self._labelNameEdit.setObjectName(ui.LABEL_NAME_EDIT_NAME)
        self._labelNameEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._labelNameEdit, row, 1)
        self._labelNameLabel.setBuddy(self._labelNameEdit)

    def _addRecordingTimeTo(self, layout, row):
        self._recordingTimeLabel = QLabel()
        layout.addWidget(self._recordingTimeLabel, row, 0)
        self._recordingTimeEdit = QLineEdit()
        self._recordingTimeEdit.setObjectName(ui.RECORDING_TIME_EDIT_NAME)
        self._recordingTimeEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._recordingTimeEdit, row, 1)
        self._recordingTimeLabel.setBuddy(self._recordingTimeEdit)

    def _addReleaseTimeTo(self, layout, row):
        self._releaseTimeLabel = QLabel()
        layout.addWidget(self._releaseTimeLabel, row, 0)
        self._releaseTimeEdit = QLineEdit()
        self._releaseTimeEdit.setObjectName(ui.RELEASE_TIME_EDIT_NAME)
        self._releaseTimeEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._releaseTimeEdit, row, 1)
        self._releaseTimeLabel.setBuddy(self._releaseTimeEdit)

    def _addOriginalReleaseTimeTo(self, layout, row):
        self._originalReleaseTimeLabel = QLabel()
        layout.addWidget(self._originalReleaseTimeLabel, row, 0)
        self._originalReleaseTimeEdit = QLineEdit()
        self._originalReleaseTimeEdit.setObjectName(ui.ORIGINAL_RELEASE_TIME_EDIT_NAME)
        self._originalReleaseTimeEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._originalReleaseTimeEdit, row, 1)
        self._originalReleaseTimeLabel.setBuddy(self._originalReleaseTimeEdit)

    def _addUpc(self, layout, row):
        self._upcLabel = QLabel()
        layout.addWidget(self._upcLabel, row, 0)
        self._upcEdit = QLineEdit()
        self._upcEdit.setObjectName(ui.UPC_EDIT_NAME)
        self._upcEdit.textEdited.connect(self._updateAlbum)
        layout.addWidget(self._upcEdit, row, 1)
        self._upcLabel.setBuddy(self._upcEdit)

    def translateUi(self):
        self._selectPictureButton.setText(self.tr('Select Picture...'))
        self._releaseNameLabel.setText(self.tr('Release Name: '))
        self._leadPerformerLabel.setText(self.tr('Lead Performer: '))
        self._guestPerformersLabel.setText(self.tr('Guest Performers: '))
        self._labelNameLabel.setText(self.tr('Label Name: '))
        self._recordingTimeLabel.setText(self.tr('Recording Time: '))
        self._releaseTimeLabel.setText(self.tr('Release Time: '))
        self._originalReleaseTimeLabel.setText(self.tr('Original Release Time: '))
        self._upcLabel.setText(self.tr('UPC/EAN: '))

    def _frontCoverOf(self, album):
        frontCovers = album.frontCovers()
        if frontCovers:
            return frontCovers[0].mime, frontCovers[0].data
        else:
            return None

    def albumStateChanged(self, album):
        self._displayFrontCover(self._frontCoverOf(album))
        self._releaseNameEdit.setText(album.releaseName)
        self._leadPerformerEdit.setText(album.leadPerformer)
        self._guestPerformersEdit.setText(album.guestPerformers)
        self._labelNameEdit.setText(album.labelName)
        self._recordingTimeEdit.setText(album.recordingTime)
        self._releaseTimeEdit.setText(album.releaseTime)
        self._originalReleaseTimeEdit.setText(album.originalReleaseTime)
        self._upcEdit.setText(album.upc)

    def _updateAlbumCover(self):
        self._album.removeImages()
        if self._frontCover is not None:
            self._album.addFrontCover(self._frontCover[0], self._frontCover[1])

    def _updateAlbum(self):
        self._album.releaseName = self._releaseNameEdit.text()
        self._album.leadPerformer = self._leadPerformerEdit.text()
        self._album.guestPerformers = self._guestPerformersEdit.text()
        self._album.labelName = self._labelNameEdit.text()
        self._album.recordingTime = self._recordingTimeEdit.text()
        self._album.releaseTime = self._releaseTimeEdit.text()
        self._album.originalReleaseTime = self._originalReleaseTimeEdit.text()
        self._album.upc = self._upcEdit.text()
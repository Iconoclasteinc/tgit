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
                         QFileDialog)

ALBUM_PANEL_NAME = 'Album Panel'
FRONT_COVER_PICTURE_NAME = "Front Cover Picture"
FRONT_COVER_DISPLAY_SIZE = (125, 125)
SELECT_PICTURE_BUTTON_NAME = "Select Picture"
SELECT_PICTURE_DIALOG_NAME = "Select Picture File"
RELEASE_NAME_NAME = 'Release Name'
LEAD_PERFORMER_NAME = "Lead Performer"
RELEASE_DATE_NAME = "Release Date"
UPC_NAME = "UPC"


class AlbumPanel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(ALBUM_PANEL_NAME)
        layout = QGridLayout()
        self.setLayout(layout)
        self._makeSelectPictureDialog()
        self._fill(layout)
        self.translateUi()

    # todo integration test dialog file filtering by making sure the Accept button stay
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

    def _loadPicture(self, filename):
        if filename is None:
            return None, None
        mimeType = mimetypes.guess_type(filename)
        imageData = open(filename, "rb").read()
        return mimeType[0], imageData

    def _displayFrontCover(self, picture):
        self._frontCover = picture
        _, imageData = self._frontCover
        self._frontCoverImage.setPixmap(self._scaleToDisplayArea(imageData))

    def _scaleToDisplayArea(self, imageData):
        if imageData is None:
            return QPixmap()
        # todo we can scale the pixmap directly
        originalImage = QImage.fromData(imageData)
        width, height = FRONT_COVER_DISPLAY_SIZE
        scaledImage = originalImage.scaled(width, height, Qt.KeepAspectRatio,
                                           Qt.SmoothTransformation)
        return QPixmap.fromImage(scaledImage)

    def _fill(self, layout):
        self._addFrontCoverPictureTo(layout, 0)
        self._addReleaseNameTo(layout, 1)
        self._addLeadPerformerTo(layout, 2)
        self._addReleaseDateTo(layout, 3)
        self._addUpc(layout, 4)

    def _addFrontCoverPictureTo(self, layout, row):
        self._frontCoverImage = QLabel()
        self._frontCoverImage.setFixedSize(*FRONT_COVER_DISPLAY_SIZE)
        self._frontCoverImage.setObjectName(FRONT_COVER_PICTURE_NAME)
        layout.addWidget(self._frontCoverImage, row, 0)
        self._selectPictureButton = QPushButton()
        self._selectPictureButton.setObjectName(SELECT_PICTURE_BUTTON_NAME)
        self._selectPictureButton.clicked.connect(self._selectPictureDialog.open)
        layout.addWidget(self._selectPictureButton, row, 1)

    def _addReleaseNameTo(self, layout, row):
        self._releaseNameLabel = QLabel()
        layout.addWidget(self._releaseNameLabel, row, 0)
        self._releaseNameEdit = QLineEdit()
        self._releaseNameEdit.setObjectName(RELEASE_NAME_NAME)
        layout.addWidget(self._releaseNameEdit, row, 1)
        self._releaseNameLabel.setBuddy(self._releaseNameEdit)

    def _addLeadPerformerTo(self, layout, row):
        self._leadPerformerLabel = QLabel()
        layout.addWidget(self._leadPerformerLabel, row, 0)
        self._leadPerformerEdit = QLineEdit()
        self._leadPerformerEdit.setObjectName(LEAD_PERFORMER_NAME)
        layout.addWidget(self._leadPerformerEdit, row, 1)
        self._leadPerformerLabel.setBuddy(self._leadPerformerEdit)

    def _addReleaseDateTo(self, layout, row):
        self._releaseDateLabel = QLabel()
        layout.addWidget(self._releaseDateLabel, row, 0)
        self._releaseDateEdit = QLineEdit()
        self._releaseDateEdit.setObjectName(RELEASE_DATE_NAME)
        layout.addWidget(self._releaseDateEdit, row, 1)
        self._releaseDateLabel.setBuddy(self._releaseDateEdit)

    def _addUpc(self, layout, row):
        self._upcLabel = QLabel()
        layout.addWidget(self._upcLabel, row, 0)
        self._upcEdit = QLineEdit()
        self._upcEdit.setObjectName(UPC_NAME)
        layout.addWidget(self._upcEdit, row, 1)
        self._upcLabel.setBuddy(self._upcEdit)

    def translateUi(self):
        self._selectPictureButton.setText(self.tr("Select Picture..."))
        self._selectPictureDialog.setNameFilter(self.tr("Image files") + " (*.png *.jpeg *.jpg)")
        self._releaseNameLabel.setText(self.tr("Release Name: "))
        self._leadPerformerLabel.setText(self.tr("Lead Performer: "))
        self._releaseDateLabel.setText(self.tr("Release Date: "))
        self._upcLabel.setText(self.tr("UPC/EAN: "))

    def trackSelected(self, track):
        self._releaseNameEdit.setText(track.releaseName)
        self._displayFrontCover(track.frontCoverPicture)
        self._leadPerformerEdit.setText(track.leadPerformer)
        self._releaseDateEdit.setText(track.releaseDate)
        self._upcEdit.setText(track.upc)

    def updateTrack(self, track):
        track.releaseName = self._releaseNameEdit.text()
        track.frontCoverPicture = self._frontCover
        track.leadPerformer = self._leadPerformerEdit.text()
        track.releaseDate = self._releaseDateEdit.text()
        track.upc = self._upcEdit.text()



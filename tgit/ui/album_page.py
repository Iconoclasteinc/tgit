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
from PyQt4.QtGui import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QPixmap, QImage,
                         QHBoxLayout, QVBoxLayout)

from tgit.album import AlbumListener
from tgit.ui import constants as ui, display
from tgit.ui.text_area import TextArea
from tgit.ui.file_chooser import FileChoiceListener
from tgit.util import fs


class AlbumPage(QWidget, FileChoiceListener, AlbumListener):
    def __init__(self, album, pictureChooser, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._pictureChooser = pictureChooser
        self._pictureChooser.addChoiceListener(self)

        self._assemble(album)

    def _assemble(self, album):
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

        mimeType = fs.guessMimeType(filename)
        imageData = fs.readContent(filename)
        return mimeType, imageData

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
        self._addTownTo(layout, 5)
        self._addCountryTo(layout, 6)
        self._addCatalogNumberTo(layout, 7)
        self._addUpcTo(layout, 8)
        self._addRecordingTimeTo(layout, 9)
        self._addReleaseTimeTo(layout, 10)
        self._addDigitalReleaseTimeTo(layout, 11)
        self._addOriginalReleaseTimeTo(layout, 12)
        self._addRecordingStudiosTo(layout, 13)
        self._addProducerTo(layout, 14)
        self._addMixerTo(layout, 15)
        self._addCommentsTo(layout, 16)
        self._addPrimaryStyleTo(layout, 17)
        self._addMediaTypeTo(layout, 18)
        self._addReleaseTypeTo(layout, 19)

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
        self._pictureChooser.chooseSingleFile()

    def _addReleaseNameTo(self, layout, row):
        self._releaseNameLabel = QLabel()
        layout.addWidget(self._releaseNameLabel, row, 0)
        self._releaseNameEdit = QLineEdit()
        self._releaseNameEdit.setObjectName(ui.RELEASE_NAME_EDIT_NAME)
        self._releaseNameEdit.editingFinished.connect(self._updateReleaseName)
        layout.addWidget(self._releaseNameEdit, row, 1)
        self._releaseNameLabel.setBuddy(self._releaseNameEdit)

    def _addLeadPerformerTo(self, layout, row):
        self._leadPerformerLabel = QLabel()
        layout.addWidget(self._leadPerformerLabel, row, 0)
        self._leadPerformerEdit = QLineEdit()
        self._leadPerformerEdit.setObjectName(ui.LEAD_PERFORMER_EDIT_NAME)
        self._leadPerformerEdit.editingFinished.connect(self._updateLeadPerformer)
        layout.addWidget(self._leadPerformerEdit, row, 1)
        self._leadPerformerLabel.setBuddy(self._leadPerformerEdit)

    def _addGuestPerformersTo(self, layout, row):
        self._guestPerformersLabel = QLabel()
        layout.addWidget(self._guestPerformersLabel, row, 0)
        self._guestPerformersEdit = QLineEdit()
        self._guestPerformersEdit.setObjectName(ui.GUEST_PERFORMERS_EDIT_NAME)
        self._guestPerformersEdit.editingFinished.connect(self._updateGuestPerformers)
        layout.addWidget(self._guestPerformersEdit, row, 1)
        self._guestPerformersLabel.setBuddy(self._guestPerformersEdit)

    def _addLabelNameTo(self, layout, row):
        self._labelNameLabel = QLabel()
        layout.addWidget(self._labelNameLabel, row, 0)
        self._labelNameEdit = QLineEdit()
        self._labelNameEdit.setObjectName(ui.LABEL_NAME_EDIT_NAME)
        self._labelNameEdit.editingFinished.connect(self._updateLabelName)
        layout.addWidget(self._labelNameEdit, row, 1)
        self._labelNameLabel.setBuddy(self._labelNameEdit)

    def _addTownTo(self, layout, row):
        self._townLabel = QLabel()
        layout.addWidget(self._townLabel, row, 0)
        self._townEdit = QLineEdit()
        self._townEdit.setDisabled(True)
        self._townEdit.setObjectName(ui.TOWN_EDIT_NAME)
        layout.addWidget(self._townEdit, row, 1)
        self._townLabel.setBuddy(self._townEdit)

    def _addCountryTo(self, layout, row):
        self._countryLabel = QLabel()
        layout.addWidget(self._countryLabel, row, 0)
        self._countryEdit = QLineEdit()
        self._countryEdit.setDisabled(True)
        self._countryEdit.setObjectName(ui.COUNTRY_EDIT_NAME)
        layout.addWidget(self._countryEdit, row, 1)
        self._countryLabel.setBuddy(self._countryEdit)

    def _addCatalogNumberTo(self, layout, row):
        self._catalogNumberLabel = QLabel()
        layout.addWidget(self._catalogNumberLabel, row, 0)
        self._catalogNumberEdit = QLineEdit()
        self._catalogNumberEdit.setObjectName(ui.CATALOG_NUMBER_EDIT_NAME)
        self._catalogNumberEdit.editingFinished.connect(self._updateCatalogNumber)
        layout.addWidget(self._catalogNumberEdit, row, 1)
        self._catalogNumberLabel.setBuddy(self._catalogNumberEdit)

    def _addUpcTo(self, layout, row):
        self._upcLabel = QLabel()
        layout.addWidget(self._upcLabel, row, 0)
        self._upcEdit = QLineEdit()
        self._upcEdit.setObjectName(ui.UPC_EDIT_NAME)
        self._upcEdit.editingFinished.connect(self._updateUpc)
        layout.addWidget(self._upcEdit, row, 1)
        self._upcLabel.setBuddy(self._upcEdit)

    def _addRecordingTimeTo(self, layout, row):
        self._recordingTimeLabel = QLabel()
        layout.addWidget(self._recordingTimeLabel, row, 0)
        self._recordingTimeEdit = QLineEdit()
        self._recordingTimeEdit.setObjectName(ui.RECORDING_TIME_EDIT_NAME)
        self._recordingTimeEdit.editingFinished.connect(self._updateRecordingTime)
        layout.addWidget(self._recordingTimeEdit, row, 1)
        self._recordingTimeLabel.setBuddy(self._recordingTimeEdit)

    def _addReleaseTimeTo(self, layout, row):
        self._releaseTimeLabel = QLabel()
        layout.addWidget(self._releaseTimeLabel, row, 0)
        self._releaseTimeEdit = QLineEdit()
        self._releaseTimeEdit.setObjectName(ui.RELEASE_TIME_EDIT_NAME)
        self._releaseTimeEdit.editingFinished.connect(self._updateReleaseTime)
        layout.addWidget(self._releaseTimeEdit, row, 1)
        self._releaseTimeLabel.setBuddy(self._releaseTimeEdit)

    def _addDigitalReleaseTimeTo(self, layout, row):
        self._digitalReleaseTimeLabel = QLabel()
        layout.addWidget(self._digitalReleaseTimeLabel, row, 0)
        self._digitalReleaseTimeEdit = QLineEdit()
        self._digitalReleaseTimeEdit.setDisabled(True)
        self._digitalReleaseTimeEdit.setObjectName(ui.DIGITAL_RELEASE_TIME_EDIT_NAME)
        layout.addWidget(self._digitalReleaseTimeEdit, row, 1)
        self._digitalReleaseTimeLabel.setBuddy(self._digitalReleaseTimeEdit)

    def _addOriginalReleaseTimeTo(self, layout, row):
        self._originalReleaseTimeLabel = QLabel()
        layout.addWidget(self._originalReleaseTimeLabel, row, 0)
        self._originalReleaseTimeEdit = QLineEdit()
        self._originalReleaseTimeEdit.setObjectName(ui.ORIGINAL_RELEASE_TIME_EDIT_NAME)
        # self._originalReleaseTimeEdit.setDisabled(True)
        self._originalReleaseTimeEdit.editingFinished.connect(self._updateOriginalReleaseTime)
        layout.addWidget(self._originalReleaseTimeEdit, row, 1)
        self._originalReleaseTimeLabel.setBuddy(self._originalReleaseTimeEdit)

    def _addRecordingStudiosTo(self, layout, row):
        self._recordingStudiosLabel = QLabel()
        layout.addWidget(self._recordingStudiosLabel, row, 0)
        self._recordingStudiosEdit = QLineEdit()
        self._recordingStudiosEdit.setObjectName(ui.RECORDING_STUDIOS_EDIT_NAME)
        self._recordingStudiosEdit.editingFinished.connect(self._updateRecordingStudios)
        layout.addWidget(self._recordingStudiosEdit, row, 1)
        self._recordingStudiosLabel.setBuddy(self._recordingStudiosEdit)

    def _addProducerTo(self, layout, row):
        self._producerLabel = QLabel()
        layout.addWidget(self._producerLabel, row, 0)
        self._producerEdit = QLineEdit()
        self._producerEdit.setObjectName(ui.PRODUCER_EDIT_NAME)
        self._producerEdit.editingFinished.connect(self._updateProducer)
        layout.addWidget(self._producerEdit, row, 1)
        self._producerLabel.setBuddy(self._producerEdit)

    def _addMixerTo(self, layout, row):
        self._mixerLabel = QLabel()
        layout.addWidget(self._mixerLabel, row, 0)
        self._mixerEdit = QLineEdit()
        self._mixerEdit.setObjectName(ui.MIXER_EDIT_NAME)
        self._mixerEdit.editingFinished.connect(self._updateMixer)
        layout.addWidget(self._mixerEdit, row, 1)
        self._mixerLabel.setBuddy(self._mixerEdit)

    def _addCommentsTo(self, layout, row):
        self._commentsLabel = QLabel()
        layout.addWidget(self._commentsLabel, row, 0)
        self._commentsEdit = TextArea()
        self._commentsEdit.setObjectName(ui.COMMENTS_TEXT_NAME)
        self._commentsEdit.editingFinished.connect(self._updateComments)
        layout.addWidget(self._commentsEdit, row, 1)
        self._commentsLabel.setBuddy(self._commentsEdit)

    def _addPrimaryStyleTo(self, layout, row):
        self._primaryStyleLabel = QLabel()
        layout.addWidget(self._primaryStyleLabel, row, 0)
        self._primaryStyleEdit = QLineEdit()
        self._primaryStyleEdit.setDisabled(True)
        self._primaryStyleEdit.setObjectName(ui.PRIMARY_STYLE_EDIT_NAME)
        layout.addWidget(self._primaryStyleEdit, row, 1)
        self._primaryStyleLabel.setBuddy(self._primaryStyleEdit)

    def _addMediaTypeTo(self, layout, row):
        self._mediaTypeLabel = QLabel()
        layout.addWidget(self._mediaTypeLabel, row, 0)
        self._mediaTypeEdit = QLineEdit()
        self._mediaTypeEdit.setDisabled(True)
        self._mediaTypeEdit.setObjectName(ui.MEDIA_TYPE_EDIT_NAME)
        layout.addWidget(self._mediaTypeEdit, row, 1)
        self._mediaTypeLabel.setBuddy(self._mediaTypeEdit)

    def _addReleaseTypeTo(self, layout, row):
        self._releaseTypeLabel = QLabel()
        layout.addWidget(self._releaseTypeLabel, row, 0)
        self._releaseTypeEdit = QLineEdit()
        self._releaseTypeEdit.setDisabled(True)
        self._releaseTypeEdit.setObjectName(ui.RELEASE_TYPE_EDIT_NAME)
        layout.addWidget(self._releaseTypeEdit, row, 1)
        self._releaseTypeLabel.setBuddy(self._releaseTypeEdit)

    def translateUi(self):
        self._selectPictureButton.setText(self.tr('Select Picture...'))
        self._releaseNameLabel.setText(self.tr('Release Name: '))
        self._leadPerformerLabel.setText(self.tr('Lead Performer: '))
        self._guestPerformersLabel.setText(self.tr('Guest Performers: '))
        self._labelNameLabel.setText(self.tr('Label Name: '))
        self._townLabel.setText(self.tr('Town: '))
        self._countryLabel.setText(self.tr('Country: '))
        self._catalogNumberLabel.setText(self.tr('Catalog Number: '))
        self._upcLabel.setText(self.tr('UPC/EAN: '))
        self._recordingTimeLabel.setText(self.tr('Recording Time: '))
        self._releaseTimeLabel.setText(self.tr('Release Time: '))
        self._digitalReleaseTimeLabel.setText(self.tr('Digital Release Time: '))
        self._originalReleaseTimeLabel.setText(self.tr('Original Release Time: '))
        self._recordingStudiosLabel.setText(self.tr('Recording Studios: '))
        self._producerLabel.setText(self.tr('Producer: '))
        self._mixerLabel.setText(self.tr('Mixer: '))
        self._commentsLabel.setText(self.tr('Comments: '))
        self._primaryStyleLabel.setText(self.tr('Primary Style: '))
        self._mediaTypeLabel.setText(self.tr('Media Type: '))
        self._releaseTypeLabel.setText(self.tr('Release Type: '))

    def _frontCoverOf(self, album):
        frontCovers = album.frontCovers
        if frontCovers:
            return frontCovers[0].mime, frontCovers[0].data
        else:
            return None

    def albumStateChanged(self, album):
        self._displayFrontCover(self._frontCoverOf(album))
        self._releaseNameEdit.setText(album.releaseName)
        self._leadPerformerEdit.setText(album.leadPerformer)
        self._guestPerformersEdit.setText(display.toPeopleList(album.guestPerformers))
        self._labelNameEdit.setText(album.labelName)
        self._catalogNumberEdit.setText(album.catalogNumber)
        self._upcEdit.setText(album.upc)
        self._recordingTimeEdit.setText(album.recordingTime)
        self._releaseTimeEdit.setText(album.releaseTime)
        self._originalReleaseTimeEdit.setText(album.originalReleaseTime)
        self._recordingStudiosEdit.setText(album.recordingStudios)
        self._producerEdit.setText(album.producer)
        self._mixerEdit.setText(album.mixer)
        self._commentsEdit.setPlainText(album.comments)

    def _updateAlbumCover(self):
        self._album.removeImages()
        if self._frontCover is not None:
            self._album.addFrontCover(self._frontCover[0], self._frontCover[1])

    def _updateReleaseName(self):
        self._album.releaseName = self._releaseNameEdit.text()

    def _updateLeadPerformer(self):
        self._album.leadPerformer = self._leadPerformerEdit.text()

    def _updateGuestPerformers(self):
        self._album.guestPerformers = display.fromPeopleList(self._guestPerformersEdit.text())

    def _updateLabelName(self):
        self._album.labelName = self._labelNameEdit.text()

    def _updateCatalogNumber(self):
        self._album.catalogNumber = self._catalogNumberEdit.text()

    def _updateUpc(self):
        self._album.upc = self._upcEdit.text()

    def _updateRecordingTime(self):
        self._album.recordingTime = self._recordingTimeEdit.text()

    def _updateReleaseTime(self):
        self._album.releaseTime = self._releaseTimeEdit.text()

    def _updateOriginalReleaseTime(self):
        self._album.originalReleaseTime = self._originalReleaseTimeEdit.text()

    def _updateRecordingStudios(self):
        self._album.recordingStudios = self._recordingStudiosEdit.text()

    def _updateProducer(self):
        self._album.producer = self._producerEdit.text()

    def _updateMixer(self):
        self._album.mixer = self._mixerEdit.text()

    def _updateComments(self):
        self._album.comments = self._commentsEdit.toPlainText()
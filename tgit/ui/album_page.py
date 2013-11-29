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
from PyQt4.QtGui import *

from tgit.album import AlbumListener
from tgit.ui import constants as ui, display
from tgit.ui.text_area import TextArea
from tgit.ui.file_chooser import FileChoiceListener
from tgit.util import fs


class AlbumPage(QWidget, FileChoiceListener, AlbumListener):
    FRONT_COVER_FIELD_NAME = 'front-cover'
    FRONT_COVER_SIZE = (125, 125)
    SELECT_PICTURE_BUTTON_NAME = 'select-picture'
    CHOOSE_IMAGE_FILE_DIALOG_NAME = 'choose-image-file'

    RELEASE_NAME_FIELD_NAME = 'release-name'
    LEAD_PERFORMER_FIELD_NAME = 'lead-performer'
    AREA_FIELD_NAME = 'area'
    GUEST_PERFORMERS_FIELD_NAME = 'guest performers'

    LABEL_NAME_FIELD_NAME = 'label-name'
    LABEL_TOWN_FIELD_NAME = 'label-town'
    CATALOG_NUMBER_FIELD_NAME = 'catalog-number'
    UPC_FIELD_NAME = 'upc'
    MEDIA_TYPE_FIELD_NAME = 'media-type'
    RELEASE_TYPE_FIELD_NAME = 'release-type'
    COMMENTS_FIELD_NAME = 'comments'

    RELEASE_TIME_FIELD_NAME = 'release-time'
    DIGITAL_RELEASE_FIELD_NAME = 'digital-release-time'
    ORIGINAL_RELEASE_TIME_FIELD_NAME = 'original-release-time'
    RECORDING_TIME_FIELD_NAME = 'recording-time'

    RECORDING_STUDIOS_FIELD_NAME = 'recording-studios'
    PRODUCER_FIELD_NAME = 'producer'
    MIXER_FIELD_NAME = 'mixer'
    PRIMARY_STYLE_FIELD_NAME = 'primary-style'

    def __init__(self, album, pictureChooser, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._pictureChooser = pictureChooser
        self._pictureChooser.addChoiceListener(self)

        self._build()
        self.localize()
        self.albumStateChanged(album)

    def _build(self):
        self.setObjectName(ui.ALBUM_PAGE_NAME)
        self._fillContent()
        self._disableTeaserFields()

    def _fillContent(self):
        layout = QHBoxLayout()
        layout.addWidget(self._makeLeftColumn())
        layout.addWidget(self._makeRightColumn())
        self.setLayout(layout)

    def _makeLeftColumn(self):
        column = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(self._makeFrontCoverPanel())
        layout.addWidget(self._makeDatesFieldSet())
        layout.addStretch()

        column.setLayout(layout)
        return column

    def _makeRightColumn(self):
        column = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(self._makeAlbumFieldSet())
        layout.addWidget(self._makeRecordFieldSet())
        layout.addWidget(self._makeRecordingFieldSet())
        layout.addStretch()

        column.setLayout(layout)
        return column

    def _makeFrontCoverPanel(self):
        panel = QWidget()
        self._frontCoverPictureLabel = self._makeFrontCoverPictureField()
        self._selectPictureButton = self._makeSelectPictureButton()

        layout = QVBoxLayout()
        layout.addWidget(self._frontCoverPictureLabel)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._selectPictureButton)
        buttons.addStretch()
        layout.addLayout(buttons)

        panel.setLayout(layout)
        return panel

    def _makeFrontCoverPictureField(self):
        label = QLabel()
        label.setObjectName(AlbumPage.FRONT_COVER_FIELD_NAME)
        label.setFixedSize(*AlbumPage.FRONT_COVER_SIZE)
        return label

    def _makeSelectPictureButton(self):
        button = QPushButton()
        button.setObjectName(AlbumPage.SELECT_PICTURE_BUTTON_NAME)
        button.clicked.connect(self._selectPicture)
        return button

    def _makeDatesFieldSet(self):
        # todo move to localize()
        fieldSet = QGroupBox(self.tr('DATES'))
        self._releaseTimeLineEdit = self._makeReleaseTimeField()
        self._digitalReleaseTimeLineEdit = self._makeDigitalReleaseTimeField()
        self._originalReleaseTimeLineEdit = self._makeOriginalReleaseTimeField()
        self._recordingTimeLineEdit = self._makeRecordingTimeField()

        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self._addLabelledFields(form, self._releaseTimeLineEdit, self._digitalReleaseTimeLineEdit,
                                self._originalReleaseTimeLineEdit, self._recordingTimeLineEdit)

        fieldSet.setLayout(form)
        return fieldSet

    def _addLabelledFields(self, form, *fields):
        for field in fields:
            # When label have empty text, form layout seems to ignore setting their buddy
            label = QLabel()
            label.setBuddy(field)
            form.addRow(label, field)

    # todo once we connect all editingFinished signals to a single updateAlbum slot,
    # we can probably get away with a single _makeTextField(name)
    def _makeReleaseTimeField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.RELEASE_TIME_FIELD_NAME)
        edit.editingFinished.connect(self._updateReleaseTime)
        return edit

    def _makeDigitalReleaseTimeField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.DIGITAL_RELEASE_FIELD_NAME)
        return edit

    def _makeOriginalReleaseTimeField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.ORIGINAL_RELEASE_TIME_FIELD_NAME)
        return edit

    def _makeRecordingTimeField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.RECORDING_TIME_FIELD_NAME)
        edit.editingFinished.connect(self._updateRecordingTime)
        return edit

    def _makeAlbumFieldSet(self):
        # todo move to localize()
        fieldSet = QGroupBox(self.tr('ALBUM'))
        self._releaseNameLineEdit = self._makeReleaseNameField()
        self._leadPerformerLineEdit = self._makeLeadPerformerField()
        self._areaLineEdit = self._makeAreaField()
        self._guestPerformersLineEdit = self._makeGuestPerformersField()

        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self._addLabelledFields(form, self._releaseNameLineEdit, self._leadPerformerLineEdit,
                                self._areaLineEdit, self._guestPerformersLineEdit)

        fieldSet.setLayout(form)
        return fieldSet

    def _makeReleaseNameField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.RELEASE_NAME_FIELD_NAME)
        edit.editingFinished.connect(self._updateReleaseName)
        return edit

    def _makeLeadPerformerField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.LEAD_PERFORMER_FIELD_NAME)
        edit.editingFinished.connect(self._updateLeadPerformer)
        return edit

    def _makeAreaField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.AREA_FIELD_NAME)
        return edit

    def _makeGuestPerformersField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.GUEST_PERFORMERS_FIELD_NAME)
        edit.editingFinished.connect(self._updateGuestPerformers)
        return edit

    def _makeRecordFieldSet(self):
        # todo move to localize()
        fieldSet = QGroupBox(self.tr('RECORD'))
        self._labelNameLineEdit = self._makeLabelNameField()
        self._labelTownLineEdit = self._makeLabelTownField()
        self._catalogNumberLineEdit = self._makeCatalogNumberField()
        self._upcLineEdit = self._makeUpcField()
        self._mediaTypeLineEdit = self._makeMediaTypeField()
        self._releaseTypeLineEdit = self._makeReleaseTypeField()
        self._commentsTextArea = self._makeCommentsField()

        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self._addLabelledFields(form, self._labelNameLineEdit, self._labelTownLineEdit,
                                self._catalogNumberLineEdit, self._upcLineEdit,
                                self._mediaTypeLineEdit, self._releaseTypeLineEdit,
                                self._commentsTextArea)

        fieldSet.setLayout(form)
        return fieldSet

    def _makeLabelNameField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.LABEL_NAME_FIELD_NAME)
        edit.editingFinished.connect(self._updateLabelName)
        return edit

    def _makeLabelTownField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.LABEL_TOWN_FIELD_NAME)
        return edit

    def _makeCatalogNumberField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.CATALOG_NUMBER_FIELD_NAME)
        edit.editingFinished.connect(self._updateCatalogNumber)
        return edit

    def _makeUpcField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.UPC_FIELD_NAME)
        edit.editingFinished.connect(self._updateUpc)
        return edit

    def _makeMediaTypeField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.MEDIA_TYPE_FIELD_NAME)
        return edit

    def _makeReleaseTypeField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.RELEASE_TYPE_FIELD_NAME)
        return edit

    def _makeCommentsField(self):
        text = TextArea()
        text.setObjectName(AlbumPage.COMMENTS_FIELD_NAME)
        text.editingFinished.connect(self._updateComments)
        return text

    def _makeRecordingFieldSet(self):
        # todo move to localize()
        fieldSet = QGroupBox(self.tr('RECORDING'))
        self._recordingStudiosLineEdit = self._makeRecordingStudiosField()
        self._producerLineEdit = self._makeProducerField()
        self._mixerLineEdit = self._makeMixerField()
        self._primaryStyleLineEdit = self._makePrimaryStyleField()

        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self._addLabelledFields(form, self._recordingStudiosLineEdit, self._producerLineEdit,
                                self._mixerLineEdit, self._primaryStyleLineEdit)

        fieldSet.setLayout(form)
        return fieldSet

    def _makeRecordingStudiosField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.RECORDING_STUDIOS_FIELD_NAME)
        edit.editingFinished.connect(self._updateRecordingStudios)
        return edit

    def _makeProducerField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.PRODUCER_FIELD_NAME)
        edit.editingFinished.connect(self._updateProducer)
        return edit

    def _makeMixerField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.MIXER_FIELD_NAME)
        edit.editingFinished.connect(self._updateMixer)
        return edit

    def _makePrimaryStyleField(self):
        edit = QLineEdit()
        edit.setObjectName(AlbumPage.PRIMARY_STYLE_FIELD_NAME)
        return edit

    def _disableTeaserFields(self):
        self._disableField(self._digitalReleaseTimeLineEdit)
        self._disableField(self._originalReleaseTimeLineEdit)
        self._disableField(self._areaLineEdit)
        self._disableField(self._labelTownLineEdit)
        self._disableField(self._mediaTypeLineEdit)
        self._disableField(self._releaseTypeLineEdit)
        self._disableField(self._primaryStyleLineEdit)

    def _disableField(self, field):
        field.setDisabled(True)
        self._labelFor(field).setDisabled(True)

    def localize(self):
        self._selectPictureButton.setText(self.tr('Select Picture...'))
        self._labelFor(self._releaseNameLineEdit).setText(self.tr('Release Name:'))
        self._labelFor(self._leadPerformerLineEdit).setText(self.tr('Lead Performer:'))
        self._leadPerformerLineEdit.setPlaceholderText(self.tr('Artist, Band or Various Artists'))
        self._labelFor(self._areaLineEdit).setText(self.tr('Area:'))
        self._labelFor(self._guestPerformersLineEdit).setText(self.tr('Guest Performers:'))
        self._guestPerformersLineEdit.setPlaceholderText(
            self.tr('Instrument1: Performer1; Instrument2: Performer2; ...'))
        self._labelFor(self._labelNameLineEdit).setText(self.tr('Label Name:'))
        self._labelFor(self._labelTownLineEdit).setText(self.tr('Label Town:'))
        self._labelFor(self._catalogNumberLineEdit).setText(self.tr('Catalog Number:'))
        self._labelFor(self._upcLineEdit).setText(self.tr('UPC/EAN:'))
        self._labelFor(self._mediaTypeLineEdit).setText(self.tr('Media Type:'))
        self._labelFor(self._releaseTypeLineEdit).setText(self.tr('Release Type:'))
        self._labelFor(self._commentsTextArea).setText(self.tr('Comments:'))
        self._labelFor(self._releaseTimeLineEdit).setText(self.tr('Release Time:'))
        self._releaseTimeLineEdit.setPlaceholderText(self.tr('YYYY-MM-DD'))
        self._labelFor(self._digitalReleaseTimeLineEdit).setText(self.tr('Digital Release Time:'))
        self._labelFor(self._originalReleaseTimeLineEdit).setText(self.tr('Original Release Time:'))
        self._labelFor(self._recordingTimeLineEdit).setText(self.tr('Recording Time: '))
        self._recordingTimeLineEdit.setPlaceholderText(self.tr('YYYY-MM-DD'))
        self._labelFor(self._recordingStudiosLineEdit).setText(self.tr('Recording Studios:'))
        self._labelFor(self._producerLineEdit).setText(self.tr('Producer:'))
        self._labelFor(self._mixerLineEdit).setText(self.tr('Mixer:'))
        self._labelFor(self._primaryStyleLineEdit).setText(self.tr('Primary Style:'))

    def _labelFor(self, widget):
        return next(label for label in self.findChildren(QLabel) if label.buddy() == widget)

    def fileChosen(self, filename):
        self._frontCoverImage = self._loadImage(filename)
        self._displayFrontCover(self._frontCoverImage)
        self._updateAlbumCover()

    def _loadImage(self, filename):
        if filename is None:
            return None

        mimeType = fs.guessMimeType(filename)
        imageData = fs.readContent(filename)
        return mimeType, imageData

    def _displayFrontCover(self, image):
        self._frontCoverPictureLabel.setPixmap(self._scaleToDisplayArea(image))

    def _scaleToDisplayArea(self, image):
        if image is None:
            return QPixmap()

        _, data = image
        scaledImage = self._scaleImage(QImage.fromData(data), *AlbumPage.FRONT_COVER_SIZE)
        return QPixmap.fromImage(scaledImage)

    def _scaleImage(self, image, width, height):
        return image.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def _selectPicture(self):
        self._pictureChooser.chooseSingleFile()

    def _frontCoverOf(self, album):
        frontCovers = album.frontCovers
        if frontCovers:
            return frontCovers[0].mime, frontCovers[0].data
        else:
            return None

    def albumStateChanged(self, album):
        self._displayFrontCover(self._frontCoverOf(album))
        self._releaseNameLineEdit.setText(album.releaseName)
        self._leadPerformerLineEdit.setText(album.leadPerformer)
        self._guestPerformersLineEdit.setText(display.toPeopleList(album.guestPerformers))
        self._labelNameLineEdit.setText(album.labelName)
        self._catalogNumberLineEdit.setText(album.catalogNumber)
        self._upcLineEdit.setText(album.upc)
        self._commentsTextArea.setPlainText(album.comments)
        self._releaseTimeLineEdit.setText(album.releaseTime)
        self._recordingTimeLineEdit.setText(album.recordingTime)
        self._recordingStudiosLineEdit.setText(album.recordingStudios)
        self._producerLineEdit.setText(album.producer)
        self._mixerLineEdit.setText(album.mixer)

    def _updateAlbumCover(self):
        self._album.removeImages()
        if self._frontCoverImage is not None:
            self._album.addFrontCover(self._frontCoverImage[0], self._frontCoverImage[1])

    def _updateReleaseName(self):
        self._album.releaseName = self._releaseNameLineEdit.text()

    def _updateLeadPerformer(self):
        self._album.leadPerformer = self._leadPerformerLineEdit.text()

    def _updateGuestPerformers(self):
        self._album.guestPerformers = display.fromPeopleList(self._guestPerformersLineEdit.text())

    def _updateLabelName(self):
        self._album.labelName = self._labelNameLineEdit.text()

    def _updateCatalogNumber(self):
        self._album.catalogNumber = self._catalogNumberLineEdit.text()

    def _updateUpc(self):
        self._album.upc = self._upcLineEdit.text()

    def _updateRecordingTime(self):
        self._album.recordingTime = self._recordingTimeLineEdit.text()

    def _updateReleaseTime(self):
        self._album.releaseTime = self._releaseTimeLineEdit.text()

    def _updateRecordingStudios(self):
        self._album.recordingStudios = self._recordingStudiosLineEdit.text()

    def _updateProducer(self):
        self._album.producer = self._producerLineEdit.text()

    def _updateMixer(self):
        self._album.mixer = self._mixerLineEdit.text()

    def _updateComments(self):
        self._album.comments = self._commentsTextArea.toPlainText()
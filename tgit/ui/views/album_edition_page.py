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
from PyQt4.QtGui import (QWidget, QSizePolicy, QGroupBox, QLabel, QPushButton, QLineEdit,
                         QPixmap, QImage, QCheckBox, QComboBox, QAbstractButton)

from tgit.genres import GENRES
from tgit.ui import display, style
from tgit.ui.widgets.text_area import TextArea


def scaleTo(image, width, height):
    if image is None:
        return QPixmap()
    scaledImage = QImage.fromData(image.data).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return QPixmap.fromImage(scaledImage)


def addLabelledFields(form, *fields):
    for field in fields:
        label = QLabel()
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setBuddy(field)
        form.addRow(label, field)


class AlbumEditionPage(QWidget):
    NAME = 'album-edition-page'

    PICTURES_FIELD_SET_NAME = 'pictures'
    FRONT_COVER_FIELD_NAME = 'front-cover'
    FRONT_COVER_SIZE = (350, 350)
    SELECT_PICTURE_BUTTON_NAME = 'select-picture'
    REMOVE_PICTURE_BUTTON_NAME = 'remove-picture'

    RELEASE_NAME_FIELD_NAME = 'release-name'
    COMPILATION_FIELD_NAME = 'compilation'
    LEAD_PERFORMER_FIELD_NAME = 'lead-performer'
    AREA_FIELD_NAME = 'area'
    GUEST_PERFORMERS_FIELD_NAME = 'guest-performers'

    LABEL_NAME_FIELD_NAME = 'label-name'
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

    def __init__(self):
        QWidget.__init__(self)
        self._build()
        self._disableMacFocusFrame()
        self._disableTeaserFields()
        self.translate()

    def onMetadataChange(self, callback):
        for edit in (self._leadPerformerLineEdit, self._releaseNameLineEdit, self._guestPerformersLineEdit,
                self._labelNameLineEdit, self._catalogNumberLineEdit, self._upcLineEdit, self._commentsTextArea,
                self._recordingTimeLineEdit, self._releaseTimeLineEdit, self._producerLineEdit,
                self._recordingStudiosLineEdit, self._producerLineEdit, self._mixerLineEdit):
            edit.editingFinished.connect(lambda: callback(self.albumMetadata))

        self._compilationCheckBox.clicked.connect(lambda: callback(self.albumMetadata))
        self._primaryStyleCombo.activated.connect(lambda: callback(self.albumMetadata))
        self._primaryStyleCombo.lineEdit().textEdited.connect(lambda: callback(self.albumMetadata))

    def onSelectPicture(self, callback):
        self._button(self.SELECT_PICTURE_BUTTON_NAME).clicked.connect(lambda: callback())

    def onRemovePicture(self, callback):
        self._button(self.REMOVE_PICTURE_BUTTON_NAME).clicked.connect(lambda: callback())

    def _build(self):
        self.setObjectName(self.NAME)
        layout = style.horizontalLayout()
        layout.setSpacing(0)
        layout.addWidget(self._makeLeftColumn())
        layout.addWidget(self._makeRightColumn())
        self.setLayout(layout)

    def _makeLeftColumn(self):
        column = QWidget()
        column.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self._picturesFieldSet = self._makePicturesFieldSet()
        self._datesFieldSet = self._makeDatesFieldSet()

        layout = style.verticalLayout()
        layout.addWidget(self._picturesFieldSet)
        layout.addWidget(self._datesFieldSet)
        layout.addStretch()

        column.setLayout(layout)
        return column

    def _makeRightColumn(self):
        column = QWidget()
        self._albumFieldSet = self._makeAlbumFieldSet()
        self._recordFieldSet = self._makeRecordFieldSet()
        self._recordingFieldSet = self._makeRecordingFieldSet()

        layout = style.verticalLayout()
        layout.addWidget(self._albumFieldSet)
        layout.addWidget(self._recordFieldSet)
        layout.addWidget(self._recordingFieldSet)
        layout.addStretch()

        column.setLayout(layout)
        return column

    def _makePicturesFieldSet(self):
        fieldSet = QGroupBox()
        fieldSet.setObjectName(self.PICTURES_FIELD_SET_NAME)
        self._attachedPictureLabel = self._makeFrontCoverPictureField()
        self._selectPictureButton = self._makeSelectPictureButton()
        self._removePictureButton = self._makeRemovePictureButton()

        layout = style.verticalLayout()
        layout.addWidget(self._attachedPictureLabel)
        buttons = style.horizontalLayout()
        buttons.addStretch()
        buttons.addWidget(self._selectPictureButton)
        buttons.addWidget(self._removePictureButton)
        buttons.addStretch()
        layout.addLayout(buttons)

        fieldSet.setLayout(layout)
        return fieldSet

    def _makeFrontCoverPictureField(self):
        label = QLabel()
        label.setObjectName(self.FRONT_COVER_FIELD_NAME)
        label.setFixedSize(*self.FRONT_COVER_SIZE)
        self._attachedPicture = None
        return label

    def _makeSelectPictureButton(self):
        button = QPushButton()
        button.setObjectName(self.SELECT_PICTURE_BUTTON_NAME)
        style.enableButton(button)
        return button

    def _makeRemovePictureButton(self):
        button = QPushButton()
        button.setObjectName(self.REMOVE_PICTURE_BUTTON_NAME)
        style.enableButton(button)
        return button

    def _makeDatesFieldSet(self):
        fieldSet = QGroupBox()
        self._releaseTimeLineEdit = self._makeLineEdit(self.RELEASE_TIME_FIELD_NAME)
        self._digitalReleaseTimeLineEdit = self._makeLineEdit(self.DIGITAL_RELEASE_FIELD_NAME)
        self._originalReleaseTimeLineEdit = self._makeLineEdit(self.ORIGINAL_RELEASE_TIME_FIELD_NAME)
        self._recordingTimeLineEdit = self._makeLineEdit(self.RECORDING_TIME_FIELD_NAME)

        form = style.formLayout()
        addLabelledFields(form, self._releaseTimeLineEdit, self._digitalReleaseTimeLineEdit,
                          self._originalReleaseTimeLineEdit, self._recordingTimeLineEdit)

        fieldSet.setLayout(form)
        return fieldSet

    def _makeLineEdit(self, name):
        edit = QLineEdit()
        edit.setObjectName(name)
        return edit

    def _makeCheckBox(self, name):
        checkbox = QCheckBox()
        checkbox.setObjectName(name)
        checkbox.setFocusPolicy(Qt.StrongFocus)
        return checkbox

    def _makeComboBox(self, name):
        combo = QComboBox()
        combo.setObjectName(name)
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.NoInsert)
        combo.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        return combo

    def _makeAlbumFieldSet(self):
        fieldSet = QGroupBox()
        self._releaseNameLineEdit = self._makeLineEdit(self.RELEASE_NAME_FIELD_NAME)
        self._compilationCheckBox = self._makeCheckBox(self.COMPILATION_FIELD_NAME)
        self._leadPerformerLineEdit = self._makeLineEdit(self.LEAD_PERFORMER_FIELD_NAME)
        self._areaLineEdit = self._makeLineEdit(self.AREA_FIELD_NAME)
        self._guestPerformersLineEdit = self._makeLineEdit(self.GUEST_PERFORMERS_FIELD_NAME)

        form = style.formLayout()
        addLabelledFields(form, self._releaseNameLineEdit, self._compilationCheckBox, self._leadPerformerLineEdit,
                          self._areaLineEdit, self._guestPerformersLineEdit)

        fieldSet.setLayout(form)
        return fieldSet

    def _makeRecordFieldSet(self):
        fieldSet = QGroupBox()
        self._labelNameLineEdit = self._makeLineEdit(self.LABEL_NAME_FIELD_NAME)
        self._catalogNumberLineEdit = self._makeLineEdit(self.CATALOG_NUMBER_FIELD_NAME)
        self._upcLineEdit = self._makeLineEdit(self.UPC_FIELD_NAME)
        self._mediaTypeLineEdit = self._makeLineEdit(self.MEDIA_TYPE_FIELD_NAME)
        self._releaseTypeLineEdit = self._makeLineEdit(self.RELEASE_TYPE_FIELD_NAME)
        self._commentsTextArea = self._makeTextArea(self.COMMENTS_FIELD_NAME)

        form = style.formLayout()
        addLabelledFields(form, self._labelNameLineEdit, self._catalogNumberLineEdit, self._upcLineEdit,
                          self._mediaTypeLineEdit, self._releaseTypeLineEdit, self._commentsTextArea)

        fieldSet.setLayout(form)
        return fieldSet

    def _makeTextArea(self, name):
        text = TextArea()
        text.setObjectName(name)
        text.setTabChangesFocus(True)
        return text

    def _makeRecordingFieldSet(self):
        fieldSet = QGroupBox()
        self._recordingStudiosLineEdit = self._makeLineEdit(self.RECORDING_STUDIOS_FIELD_NAME)
        self._producerLineEdit = self._makeLineEdit(self.PRODUCER_FIELD_NAME)
        self._mixerLineEdit = self._makeLineEdit(self.MIXER_FIELD_NAME)
        self._primaryStyleCombo = self._makeComboBox(self.PRIMARY_STYLE_FIELD_NAME)
        self._primaryStyleCombo.addItems(GENRES)

        form = style.formLayout()
        addLabelledFields(form, self._recordingStudiosLineEdit, self._producerLineEdit, self._mixerLineEdit,
                          self._primaryStyleCombo)

        fieldSet.setLayout(form)
        return fieldSet

    def _disableTeaserFields(self):
        self._disableField(self._digitalReleaseTimeLineEdit)
        self._disableField(self._originalReleaseTimeLineEdit)
        self._disableField(self._areaLineEdit)
        self._disableField(self._mediaTypeLineEdit)
        self._disableField(self._releaseTypeLineEdit)

    def _disableField(self, field):
        field.setDisabled(True)
        self._labelFor(field).setDisabled(True)

    def updateAlbum(self, album):
        self._displayAttachedPicture(album.mainCover)
        self._releaseNameLineEdit.setText(album.releaseName)
        # todo we really need typed metadata
        self._compilationCheckBox.setChecked(album.compilation is True)
        self._leadPerformerLineEdit.setDisabled(album.compilation is True)
        if album.compilation:
            self._leadPerformerLineEdit.setText(self.tr('Various Artists'))
        else:
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
        self._primaryStyleCombo.setEditText(album.primaryStyle)

    def _displayAttachedPicture(self, image):
        self._attachedPicture = image
        self._attachedPictureLabel.setPixmap(scaleTo(image, *self.FRONT_COVER_SIZE))

    @property
    def albumMetadata(self):
        class Snapshot(object):
            def __str__(self):
                return str(self.__dict__)

        snapshot = Snapshot()
        snapshot.releaseName = self._releaseNameLineEdit.text()
        snapshot.compilation = self._compilationCheckBox.isChecked()
        snapshot.leadPerformer = self._leadPerformerLineEdit.text()
        snapshot.guestPerformers = display.fromPeopleList(self._guestPerformersLineEdit.text())
        snapshot.labelName = self._labelNameLineEdit.text()
        snapshot.catalogNumber = self._catalogNumberLineEdit.text()
        snapshot.upc = self._upcLineEdit.text()
        snapshot.comments = self._commentsTextArea.toPlainText()
        snapshot.recordingTime = self._recordingTimeLineEdit.text()
        snapshot.releaseTime = self._releaseTimeLineEdit.text()
        snapshot.recordingStudios = self._recordingStudiosLineEdit.text()
        snapshot.producer = self._producerLineEdit.text()
        snapshot.mixer = self._mixerLineEdit.text()
        snapshot.primaryStyle = self._primaryStyleCombo.currentText()

        return snapshot

    def _disableMacFocusFrame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def translate(self):
        self._translatePictureFields()
        self._translateAlbumFields()
        self._translateRecordFields()
        self._translateDateFields()
        self._translateRecordingFields()

    def _translatePictureFields(self):
        self._picturesFieldSet.setTitle(self.tr('PICTURES'))
        self._selectPictureButton.setText(self.tr('SELECT PICTURE...'))
        self._removePictureButton.setText(self.tr('REMOVE'))

    def _translateAlbumFields(self):
        self._albumFieldSet.setTitle(self.tr('ALBUM'))
        self._labelFor(self._releaseNameLineEdit).setText(self.tr('Release Name:'))
        self._labelFor(self._compilationCheckBox).setText(self.tr('Compilation:'))
        self._labelFor(self._leadPerformerLineEdit).setText(self.tr('Lead Performer:'))
        self._leadPerformerLineEdit.setPlaceholderText(self.tr('Artist, Band or Various Artists'))
        self._labelFor(self._areaLineEdit).setText(self.tr('Area:'))
        self._labelFor(self._guestPerformersLineEdit).setText(self.tr('Guest Performers:'))
        self._guestPerformersLineEdit.setPlaceholderText(
            self.tr('Instrument1: Performer1; Instrument2: Performer2; ...'))
        self._labelFor(self._labelNameLineEdit).setText(self.tr('Label Name:'))

    def _translateRecordFields(self):
        self._recordFieldSet.setTitle(self.tr('RECORD'))
        self._labelFor(self._catalogNumberLineEdit).setText(self.tr('Catalog Number:'))
        self._labelFor(self._upcLineEdit).setText(self.tr('UPC/EAN:'))
        self._upcLineEdit.setPlaceholderText('1234567899999')
        self._labelFor(self._mediaTypeLineEdit).setText(self.tr('Media Type:'))

    def _translateDateFields(self):
        self._datesFieldSet.setTitle(self.tr('DATES'))
        self._labelFor(self._releaseTypeLineEdit).setText(self.tr('Release Type:'))
        self._labelFor(self._commentsTextArea).setText(self.tr('Comments:'))
        self._labelFor(self._releaseTimeLineEdit).setText(self.tr('Release Time:'))
        self._releaseTimeLineEdit.setPlaceholderText(self.tr('YYYY-MM-DD'))
        self._labelFor(self._digitalReleaseTimeLineEdit).setText(self.tr('Digital Release Time:'))
        self._labelFor(self._originalReleaseTimeLineEdit).setText(self.tr('Original Release Time:'))
        self._labelFor(self._recordingTimeLineEdit).setText(self.tr('Recording Time: '))
        self._recordingTimeLineEdit.setPlaceholderText(self.tr('YYYY-MM-DD'))

    def _translateRecordingFields(self):
        self._recordingFieldSet.setTitle(self.tr('RECORDING'))
        self._labelFor(self._recordingStudiosLineEdit).setText(self.tr('Recording Studios:'))
        self._labelFor(self._producerLineEdit).setText(self.tr('Producer:'))
        self._labelFor(self._mixerLineEdit).setText(self.tr('Mixer:'))
        self._labelFor(self._primaryStyleCombo).setText(self.tr('Primary Style:'))

    def _labelFor(self, widget):
        return self._child(QLabel, withBuddy(widget))

    def _button(self, name):
        return self._child(QAbstractButton, named(name))

    def _child(self, ofType, matching):
        return next(child for child in self.findChildren(ofType) if matching(child))


def named(name):
    return lambda w: w.objectName() == name


def withBuddy(buddy):
    return lambda w: w.buddy() == buddy
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

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QWidget, QSizePolicy, QGroupBox, QLabel

from tgit4.album import AlbumListener
from tgit4.genres import GENRES
from tgit4.ui.helpers import form, image, formatting


class AlbumEditionPage(QWidget, AlbumListener):
    selectPicture = pyqtSignal()
    removePicture = pyqtSignal()
    lookupISNI = pyqtSignal()
    clearISNI = pyqtSignal()
    assignISNI = pyqtSignal()
    addPerformer = pyqtSignal()
    metadataChanged = pyqtSignal(dict)

    FRONT_COVER_SIZE = 350, 350

    def __init__(self, album):
        QWidget.__init__(self)
        self.album = album
        self.picture = None
        self.build()

    def build(self):
        self.setObjectName('album-edition-page')
        layout = form.row()
        layout.setSpacing(0)
        layout.addWidget(self.makeLeftColumn())
        layout.addWidget(self.makeRightColumn())
        self.setLayout(layout)
        self.disableMacFocusFrame()
        self.disableTeaserFields()

    def albumStateChanged(self, album):
        self.refresh()

    def makeLeftColumn(self):
        column = QWidget()
        column.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        layout = form.column()
        layout.addWidget(self.makePicturesFields())
        layout.addWidget(self.makeDatesFields())
        layout.addStretch()
        column.setLayout(layout)
        return column

    def makeRightColumn(self):
        column = QWidget()
        layout = form.column()
        layout.addWidget(self.makeAlbumFields())
        layout.addWidget(self.makeRecordFields())
        layout.addWidget(self.makeRecordingFields())
        layout.addStretch()
        column.setLayout(layout)
        return column

    def makePicturesFields(self):
        pictures = QGroupBox()
        pictures.setObjectName('pictures')
        pictures.setTitle(self.tr('PICTURES'))
        layout = form.column()
        self.mainCover = form.label('front-cover')
        self.mainCover.setFixedSize(*self.FRONT_COVER_SIZE)
        layout.addWidget(self.mainCover)
        buttons = form.row()
        buttons.addStretch()
        selectPicture = form.button('select-picture', self.tr('SELECT PICTURE...'))
        selectPicture.clicked.connect(lambda pressed: self.selectPicture.emit())
        buttons.addWidget(selectPicture)
        removePicture = form.button('remove-picture', self.tr('REMOVE'))
        removePicture.clicked.connect(lambda pressed: self.removePicture.emit())
        buttons.addWidget(removePicture)
        buttons.addStretch()
        layout.addLayout(buttons)
        pictures.setLayout(layout)
        return pictures

    def makeDatesFields(self):
        dates = QGroupBox()
        dates.setTitle(self.tr('DATES'))
        layout = form.layout()
        self.releaseTime = form.lineEdit('release-time')
        self.releaseTime.setPlaceholderText(self.tr('YYYY-MM-DD'))
        self.releaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('releaseTime')))
        layout.addRow(form.labelFor(self.releaseTime, self.tr('Release Time:')), self.releaseTime)
        self.digitalReleaseTime = form.lineEdit('digital-release-time')
        self.digitalReleaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('digitalReleaseTime')))
        layout.addRow(form.labelFor(self.digitalReleaseTime, self.tr('Digital Release Time:')), self.digitalReleaseTime)
        self.originalReleaseTime = form.lineEdit('original-release-time')
        self.originalReleaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('originalReleaseTime')))
        layout.addRow(form.labelFor(self.originalReleaseTime, self.tr('Original Release Time:')),
                      self.originalReleaseTime)
        self.recordingTime = form.lineEdit('recording-time')
        self.recordingTime.setPlaceholderText(self.tr('YYYY-MM-DD'))
        self.recordingTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('recordingTime')))
        layout.addRow(form.labelFor(self.recordingTime, self.tr('Recording Time:')), self.recordingTime)
        dates.setLayout(layout)
        return dates

    def makeAlbumFields(self):
        albums = QGroupBox()
        albums.setObjectName('album-box')
        albums.setTitle(self.tr('ALBUM'))
        layout = form.layout()

        self.releaseName = form.lineEdit('release-name')
        self.releaseName.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('releaseName')))
        layout.addRow(form.labelFor(self.releaseName, self.tr('Release Name:')), self.releaseName)

        lookupISNI = form.button('lookup-isni', self.tr('LOOKUP ISNI'), disabled=True)
        lookupISNI.clicked.connect(lambda pressed: self.lookupISNI.emit())
        lookupISNI.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        lookupISNI.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        assignISNI = form.button('assign-isni', self.tr('ASSIGN ISNI'), disabled=True)
        assignISNI.clicked.connect(lambda: self.assignISNI.emit())
        assignISNI.setToolTip(self.tr('This feature will be available soon'))
        assignISNI.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        assignISNI.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.compilation = form.checkBox('compilation')
        self.compilation.clicked.connect(lambda: self.metadataChanged.emit(self.metadata('compilation')))
        self.compilation.stateChanged.connect(lambda newState: self.enableOrDisableISNIButton(newState is Qt.Checked, self.album.leadPerformer, lookupISNI))
        layout.addRow(form.labelFor(self.compilation, self.tr('Compilation:')), self.compilation)

        self.leadPerformer = form.lineEdit('lead-performer')
        self.leadPerformer.setPlaceholderText(self.tr('Artist, Band or Various Artists'))
        self.leadPerformer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('leadPerformer')))
        self.leadPerformer.textChanged.connect(lambda value: self.enableOrDisableISNIButton(self.album.compilation, value, lookupISNI))
        leadPerformerRow = form.row()
        leadPerformerRow.addWidget(self.leadPerformer)
        leadPerformerRow.addWidget(lookupISNI)
        leadPerformerRow.addWidget(assignISNI)
        layout.addRow(form.labelFor(self.leadPerformer, self.tr('Lead Performer:')), leadPerformerRow)

        clearISNI = form.button('clear-isni', self.tr('CLEAR ISNI'))
        clearISNI.clicked.connect(lambda: self.clearISNI.emit())
        clearISNI.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        clearISNI.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.isni = form.lineEdit('isni', disabled=True)
        ISNIRow = form.row()
        ISNIRow.addWidget(self.isni)
        ISNIRow.addWidget(clearISNI)
        layout.addRow(form.labelFor(self.isni, self.tr('ISNI:'), disabled=True), ISNIRow)

        self.area = form.lineEdit('area')
        layout.addRow(form.labelFor(self.area, self.tr('Area:')), self.area)

        addPerformer = form.button('add-performer', self.tr('+'))
        addPerformer.clicked.connect(lambda: self.addPerformer.emit())
        addPerformer.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        addPerformer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.guestPerformers = form.lineEdit('guest-performers')
        self.guestPerformers.setPlaceholderText(self.tr('Instrument1: Performer1; Instrument2: Performer2; ...'))
        self.guestPerformers.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('guestPerformers')))
        performersRow = form.row()
        performersRow.addWidget(self.guestPerformers)
        performersRow.addWidget(addPerformer)
        layout.addRow(form.labelFor(self.guestPerformers, self.tr('Guest Performers:')), performersRow)

        albums.setLayout(layout)
        return albums

    def makeRecordFields(self):
        record = QGroupBox()
        record.setTitle(self.tr('RECORD'))
        layout = form.layout()
        self.labelName = form.lineEdit('label-name')
        self.labelName.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('labelName')))
        layout.addRow(form.labelFor(self.labelName, self.tr('Label Name:')), self.labelName)
        self.catalogNumber = form.lineEdit('catalog-number')
        self.catalogNumber.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('catalogNumber')))
        layout.addRow(form.labelFor(self.catalogNumber, self.tr('Catalog Number:')), self.catalogNumber)
        self.upc = form.lineEdit('upc')
        self.upc.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('upc')))
        self.upc.setPlaceholderText('1234567899999')
        layout.addRow(form.labelFor(self.upc, self.tr('UPC/EAN:')), self.upc)
        self.mediaType = form.lineEdit('media-type')
        self.mediaType.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('mediaType')))
        layout.addRow(form.labelFor(self.mediaType, self.tr('Media Type:')), self.mediaType)
        self.releaseType = form.lineEdit('release-type')
        self.releaseType.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('releaseType')))
        layout.addRow(form.labelFor(self.releaseType, self.tr('Release Type:')), self.releaseType)
        self.comments = form.textArea('comments')
        self.comments.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('comments')))
        layout.addRow(form.labelFor(self.comments, self.tr('Comments:')), self.comments)
        record.setLayout(layout)
        return record

    def makeRecordingFields(self):
        recording = QGroupBox()
        recording.setTitle(self.tr('RECORDING'))
        layout = form.layout()
        self.recordingStudios = form.lineEdit('recording-studios')
        self.recordingStudios.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('recordingStudios')))
        layout.addRow(form.labelFor(self.recordingStudios, self.tr('Recording Studios:')), self.recordingStudios)
        self.producer = form.lineEdit('producer')
        self.producer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('producer')))
        layout.addRow(form.labelFor(self.producer, self.tr('Producer:')), self.producer)
        self.mixer = form.lineEdit('mixer')
        self.mixer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata('mixer')))
        layout.addRow(form.labelFor(self.mixer, self.tr('Mixer:')), self.mixer)
        self.primaryStyle = form.comboBox('primary-style')
        self.primaryStyle.addItems(sorted(GENRES))
        self.primaryStyle.activated.connect(lambda: self.metadataChanged.emit(self.metadata('primaryStyle')))
        self.primaryStyle.lineEdit().textEdited.connect(lambda: self.metadataChanged.emit(self.metadata('primaryStyle')))
        layout.addRow(form.labelFor(self.primaryStyle, self.tr('Primary Style:')), self.primaryStyle)
        recording.setLayout(layout)
        return recording

    def disableTeaserFields(self):
        for field in (self.digitalReleaseTime, self.originalReleaseTime, self.area, self.mediaType, self.releaseType):
            field.setDisabled(True)
            self.labelFor(field).setDisabled(True)

    def refresh(self):
        if self.album.mainCover is not self.picture or self.album.mainCover is None:
            self.mainCover.setPixmap(image.scale(self.album.mainCover, *self.FRONT_COVER_SIZE))
            self.picture = self.album.mainCover
        self.releaseName.setText(self.album.releaseName)
        self.compilation.setChecked(self.album.compilation is True)
        self.displayLeadPerformer(self.album)
        self.isni.setText(self.album.isni)
        self.guestPerformers.setText(formatting.toPeopleList(self.album.guestPerformers))
        self.labelName.setText(self.album.labelName)
        self.catalogNumber.setText(self.album.catalogNumber)
        self.upc.setText(self.album.upc)
        self.comments.setPlainText(self.album.comments)
        self.releaseTime.setText(self.album.releaseTime)
        self.recordingTime.setText(self.album.recordingTime)
        self.recordingStudios.setText(self.album.recordingStudios)
        self.producer.setText(self.album.producer)
        self.mixer.setText(self.album.mixer)
        self.primaryStyle.setEditText(self.album.primaryStyle)

    def displayLeadPerformer(self, album):
        # todo this should be set in the embedded metadata adapter and we should have a checkbox for various artists
        self.leadPerformer.setText(album.compilation and self.tr('Various Artists') or album.leadPerformer)
        self.leadPerformer.setDisabled(album.compilation is True)

    def metadata(self, *keys):
        allValues = dict(releaseName=self.releaseName.text(),
                         compilation=self.compilation.isChecked(),
                         leadPerformer=self.leadPerformer.text(),
                         isni=self.isni.text(),
                         guestPerformers=formatting.fromPeopleList(self.guestPerformers.text()),
                         labelName=self.labelName.text(),
                         catalogNumber=self.catalogNumber.text(),
                         upc=self.upc.text(),
                         comments=self.comments.toPlainText(),
                         recordingTime=self.recordingTime.text(),
                         releaseTime=self.releaseTime.text(),
                         recordingStudios=self.recordingStudios.text(),
                         producer=self.producer.text(),
                         mixer=self.mixer.text(),
                         primaryStyle=self.primaryStyle.currentText())

        if len(keys) == 0:
            return allValues

        keysToRetrieve = [k for k in keys]
        if 'compilation' not in keysToRetrieve:
            keysToRetrieve.append('compilation')

        if 'leadPerformer' not in keysToRetrieve:
            keysToRetrieve.append('leadPerformer')

        return {k: allValues.get(k, None) for k in keysToRetrieve}

    def disableMacFocusFrame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def labelFor(self, widget):
        def withBuddy(buddy):
            return lambda w: w.buddy() == buddy

        return self.childWidget(QLabel, withBuddy(widget))

    def childWidget(self, ofType, matching):
        return next(child for child in self.findChildren(ofType) if matching(child))

    def enableOrDisableISNIButton(self, compilation, leadPerformer, *buttons):
        isDisabled = compilation or isBlank(leadPerformer)
        for button in buttons:
            button.setDisabled(isDisabled)


def isBlank(text):
    return not text or text.strip() == ''

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

from tgit.album import AlbumListener
from tgit.album_director import Snapshot
from tgit.genres import GENRES
from tgit.ui.helpers import form, image, formatting


class AlbumEditionPage(QWidget, AlbumListener):
    selectPicture = pyqtSignal()
    removePicture = pyqtSignal()
    metadataChanged = pyqtSignal(Snapshot)

    FRONT_COVER_SIZE = 350, 350

    def __init__(self):
        QWidget.__init__(self)
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
        self.display(album)

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
        selectPicture = form.button('select-picture')
        selectPicture.setText(self.tr('SELECT PICTURE...'))
        selectPicture.clicked.connect(lambda pressed: self.selectPicture.emit())
        buttons.addWidget(selectPicture)
        removePicture = form.button('remove-picture')
        removePicture.setText(self.tr('REMOVE'))
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
        self.releaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.releaseTime, self.tr('Release Time:')), self.releaseTime)
        self.digitalReleaseTime = form.lineEdit('digital-release-time')
        self.digitalReleaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.digitalReleaseTime, self.tr('Digital Release Time:')), self.digitalReleaseTime)
        self.originalReleaseTime = form.lineEdit('original-release-time')
        self.originalReleaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.originalReleaseTime, self.tr('Original Release Time:')), self.originalReleaseTime)
        self.recordingTime = form.lineEdit('recording-time')
        self.recordingTime.setPlaceholderText(self.tr('YYYY-MM-DD'))
        self.recordingTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.recordingTime, self.tr('Recording Time:')), self.recordingTime)
        dates.setLayout(layout)
        return dates

    def makeAlbumFields(self):
        albums = QGroupBox()
        albums.setTitle(self.tr('ALBUM'))
        layout = form.layout()
        self.releaseName = form.lineEdit('release-name')
        self.releaseName.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.releaseName, self.tr('Release Name:')), self.releaseName)
        self.compilation = form.checkBox('compilation')
        self.compilation.clicked.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.compilation, self.tr('Compilation:')), self.compilation)
        self.leadPerformer = form.lineEdit('lead-performer')
        self.leadPerformer.setPlaceholderText(self.tr('Artist, Band or Various Artists'))
        self.leadPerformer.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.leadPerformer, self.tr('Lead Performer:')), self.leadPerformer)
        self.area = form.lineEdit('area')
        layout.addRow(form.labelFor(self.area, self.tr('Area:')), self.area)
        self.guestPerformers = form.lineEdit('guest-performers')
        self.guestPerformers.setPlaceholderText(self.tr('Instrument1: Performer1; Instrument2: Performer2; ...'))
        self.guestPerformers.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.guestPerformers, self.tr('Guest Performers:')), self.guestPerformers)
        albums.setLayout(layout)
        return albums

    def makeRecordFields(self):
        record = QGroupBox()
        record.setTitle(self.tr('RECORD'))
        layout = form.layout()
        self.labelName = form.lineEdit('label-name')
        self.labelName.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.labelName, self.tr('Label Name:')), self.labelName)
        self.catalogNumber = form.lineEdit('catalog-number')
        self.catalogNumber.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.catalogNumber, self.tr('Catalog Number:')), self.catalogNumber)
        self.upc = form.lineEdit('upc')
        self.upc.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        self.upc.setPlaceholderText('1234567899999')
        layout.addRow(form.labelFor(self.upc, self.tr('UPC/EAN:')), self.upc)
        self.mediaType = form.lineEdit('media-type')
        self.mediaType.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.mediaType, self.tr('Media Type:')), self.mediaType)
        self.releaseType = form.lineEdit('release-type')
        self.releaseType.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.releaseType, self.tr('Release Type:')), self.releaseType)
        self.comments = form.textArea('comments')
        self.comments.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.comments, self.tr('Comments:')), self.comments)
        record.setLayout(layout)
        return record

    def makeRecordingFields(self):
        recording = QGroupBox()
        recording.setTitle(self.tr('RECORDING'))
        layout = form.layout()
        self.recordingStudios = form.lineEdit('recording-studios')
        self.recordingStudios.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.recordingStudios, self.tr('Recording Studios:')), self.recordingStudios)
        self.producer = form.lineEdit('producer')
        self.producer.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.producer, self.tr('Producer:')), self.producer)
        self.mixer = form.lineEdit('mixer')
        self.mixer.editingFinished.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.mixer, self.tr('Mixer:')), self.mixer)
        self.primaryStyles = form.comboBox('primary-style')
        self.primaryStyles.addItems(sorted(GENRES))
        self.primaryStyles.activated.connect(lambda: self.metadataChanged.emit(self.snapshot))
        self.primaryStyles.lineEdit().textEdited.connect(lambda: self.metadataChanged.emit(self.snapshot))
        layout.addRow(form.labelFor(self.primaryStyles, self.tr('Primary Style:')), self.primaryStyles)
        recording.setLayout(layout)
        return recording

    def disableTeaserFields(self):
        for field in (self.digitalReleaseTime, self.originalReleaseTime, self.area, self.mediaType, self.releaseType):
            field.setDisabled(True)
            self.labelFor(field).setDisabled(True)

    def display(self, album):
        self.mainCover.setPixmap(image.scale(album.mainCover, *self.FRONT_COVER_SIZE))
        self.releaseName.setText(album.releaseName)
        self.compilation.setChecked(album.compilation is True)
        self.displayLeadPerformer(album)
        self.guestPerformers.setText(formatting.toPeopleList(album.guestPerformers))
        self.labelName.setText(album.labelName)
        self.catalogNumber.setText(album.catalogNumber)
        self.upc.setText(album.upc)
        self.comments.setPlainText(album.comments)
        self.releaseTime.setText(album.releaseTime)
        self.recordingTime.setText(album.recordingTime)
        self.recordingStudios.setText(album.recordingStudios)
        self.producer.setText(album.producer)
        self.mixer.setText(album.mixer)
        self.primaryStyles.setEditText(album.primaryStyle)

    def displayLeadPerformer(self, album):
        self.leadPerformer.setText(album.compilation and self.tr('Various Artists') or album.leadPerformer)
        self.leadPerformer.setDisabled(album.compilation is True)

    @property
    def snapshot(self):
        snapshot = Snapshot()
        snapshot.releaseName = self.releaseName.text()
        snapshot.compilation = self.compilation.isChecked()
        snapshot.leadPerformer = self.leadPerformer.text()
        snapshot.guestPerformers = formatting.fromPeopleList(self.guestPerformers.text())
        snapshot.labelName = self.labelName.text()
        snapshot.catalogNumber = self.catalogNumber.text()
        snapshot.upc = self.upc.text()
        snapshot.comments = self.comments.toPlainText()
        snapshot.recordingTime = self.recordingTime.text()
        snapshot.releaseTime = self.releaseTime.text()
        snapshot.recordingStudios = self.recordingStudios.text()
        snapshot.producer = self.producer.text()
        snapshot.mixer = self.mixer.text()
        snapshot.primaryStyle = self.primaryStyles.currentText()

        return snapshot

    def disableMacFocusFrame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def labelFor(self, widget):
        def withBuddy(buddy):
            return lambda w: w.buddy() == buddy
        return self.childWidget(QLabel, withBuddy(widget))

    def childWidget(self, ofType, matching):
        return next(child for child in self.findChildren(ofType) if matching(child))


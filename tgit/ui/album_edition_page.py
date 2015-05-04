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

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QGroupBox, QLabel

from tgit.album import AlbumListener
from tgit.genres import GENRES
from tgit.ui.helpers import form, image, formatting


class AlbumEditionPage(QWidget, AlbumListener):
    selectPicture = pyqtSignal()
    removePicture = pyqtSignal()
    lookupISNI = pyqtSignal()
    clearISNI = pyqtSignal()
    assignISNI = pyqtSignal()
    addPerformer = pyqtSignal()
    metadataChanged = pyqtSignal(dict)

    FRONT_COVER_SIZE = 350, 350

    def __init__(self, album, use_local_isni_backend=False):
        QWidget.__init__(self)
        self.use_local_isni_backend = use_local_isni_backend
        self.album = album
        self.picture = None
        self._build()

    def _build(self):
        self.setObjectName("album-edition-page")
        layout = form.row()
        layout.setSpacing(0)
        layout.addWidget(self._make_left_column())
        layout.addWidget(self._make_right_column())
        self.setLayout(layout)
        self._disable_mac_focus_frame()
        self._disable_teaser_fields()

    def albumStateChanged(self, album):
        self.refresh()

    def _make_left_column(self):
        column = QWidget()
        column.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        layout = form.column()
        layout.addWidget(self._make_pictures_fields())
        layout.addWidget(self._make_dates_fields())
        layout.addStretch()
        column.setLayout(layout)
        return column

    def _make_right_column(self):
        column = QWidget()
        layout = form.column()
        layout.addWidget(self._make_album_fields())
        layout.addWidget(self._make_record_fields())
        layout.addWidget(self._make_recording_fields())
        layout.addStretch()
        column.setLayout(layout)
        return column

    def _make_pictures_fields(self):
        pictures = QGroupBox()
        pictures.setObjectName("pictures")
        pictures.setTitle(self.tr("PICTURES"))
        layout = form.column()
        self.mainCover = form.label("front-cover")
        self.mainCover.setFixedSize(*self.FRONT_COVER_SIZE)
        layout.addWidget(self.mainCover)
        buttons = form.row()
        buttons.addStretch()
        select_picture = form.button("select-picture", self.tr("SELECT PICTURE..."))
        select_picture.clicked.connect(lambda pressed: self.selectPicture.emit())
        buttons.addWidget(select_picture)
        remove_picture = form.button("remove-picture", self.tr("REMOVE"))
        remove_picture.clicked.connect(lambda pressed: self.removePicture.emit())
        buttons.addWidget(remove_picture)
        buttons.addStretch()
        layout.addLayout(buttons)
        pictures.setLayout(layout)
        return pictures

    def _make_dates_fields(self):
        dates = QGroupBox()
        dates.setTitle(self.tr("DATES"))
        layout = form.layout()
        self.releaseTime = form.lineEdit("release-time")
        self.releaseTime.setPlaceholderText(self.tr("YYYY-MM-DD"))
        self.releaseTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("releaseTime")))
        layout.addRow(form.labelFor(self.releaseTime, self.tr("Release Time:")), self.releaseTime)
        self.digitalReleaseTime = form.lineEdit("digital-release-time")
        self.digitalReleaseTime.editingFinished.connect(
            lambda: self.metadataChanged.emit(self.metadata("digitalReleaseTime")))
        layout.addRow(form.labelFor(self.digitalReleaseTime, self.tr("Digital Release Time:")), self.digitalReleaseTime)
        self.originalReleaseTime = form.lineEdit("original-release-time")
        self.originalReleaseTime.editingFinished.connect(
            lambda: self.metadataChanged.emit(self.metadata("originalReleaseTime")))
        layout.addRow(form.labelFor(self.originalReleaseTime, self.tr("Original Release Time:")),
                      self.originalReleaseTime)
        self.recordingTime = form.lineEdit("recording-time")
        self.recordingTime.setPlaceholderText(self.tr("YYYY-MM-DD"))
        self.recordingTime.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("recording_time")))
        layout.addRow(form.labelFor(self.recordingTime, self.tr("Recording Time:")), self.recordingTime)
        dates.setLayout(layout)
        return dates

    def _make_album_fields(self):
        def adjust_isni_lookup_state_on_compilation_changed(state):
            buttons = [lookup_isni]
            AlbumEditionPage._enable_or_disable_isni_button(state is Qt.Checked, self.album.lead_performer, buttons)

        def adjust_isni_lookup_and_assign_state_on_lead_performer_changed(text):
            buttons = [lookup_isni]
            if self.use_local_isni_backend and buttons.count(assign_isni) == 0:
                buttons.append(assign_isni)

            AlbumEditionPage._enable_or_disable_isni_button(self.album.compilation, text, buttons)

        albums = QGroupBox()
        albums.setObjectName("album-box")
        albums.setTitle(self.tr("ALBUM"))
        layout = form.layout()

        self.releaseName = form.lineEdit("release-name")
        self.releaseName.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("release_name")))
        layout.addRow(form.labelFor(self.releaseName, self.tr("Release Name:")), self.releaseName)

        lookup_isni = form.button("lookup-isni", self.tr("LOOKUP ISNI"), disabled=True)
        lookup_isni.clicked.connect(lambda pressed: self.lookupISNI.emit())
        lookup_isni.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        lookup_isni.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        assign_isni = form.button("assign-isni", self.tr("ASSIGN ISNI"), disabled=True)
        assign_isni.clicked.connect(lambda: self.assignISNI.emit())
        assign_isni.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        assign_isni.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.compilation = form.checkBox("compilation")
        self.compilation.clicked.connect(lambda: self.metadataChanged.emit(self.metadata("compilation")))
        self.compilation.stateChanged.connect(adjust_isni_lookup_state_on_compilation_changed)
        layout.addRow(form.labelFor(self.compilation, self.tr("Compilation:")), self.compilation)

        self.leadPerformer = form.lineEdit("lead-performer")
        self.leadPerformer.setPlaceholderText(self.tr("Artist, Band or Various Artists"))
        self.leadPerformer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("lead_performer")))
        self.leadPerformer.textChanged.connect(adjust_isni_lookup_and_assign_state_on_lead_performer_changed)
        lead_performer_row = form.row()
        lead_performer_row.addWidget(self.leadPerformer)
        lead_performer_row.addWidget(lookup_isni)
        lead_performer_row.addWidget(assign_isni)
        layout.addRow(form.labelFor(self.leadPerformer, self.tr("Lead Performer:")), lead_performer_row)

        clear_isni = form.button("clear-isni", self.tr("CLEAR ISNI"))
        clear_isni.clicked.connect(lambda: self.clearISNI.emit())
        clear_isni.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        clear_isni.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.isni = form.lineEdit("isni", disabled=True)
        isni_row = form.row()
        isni_row.addWidget(self.isni)
        isni_row.addWidget(clear_isni)
        layout.addRow(form.labelFor(self.isni, self.tr("ISNI:"), disabled=True), isni_row)

        self.area = form.lineEdit("area")
        layout.addRow(form.labelFor(self.area, self.tr("Area:")), self.area)

        add_performer = form.button("add-performer", self.tr("+"))
        add_performer.clicked.connect(lambda: self.addPerformer.emit())
        add_performer.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        add_performer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.guestPerformers = form.lineEdit("guest-performers")
        self.guestPerformers.setPlaceholderText(self.tr("Instrument1: Performer1; Instrument2: Performer2; ..."))
        self.guestPerformers.editingFinished.connect(
            lambda: self.metadataChanged.emit(self.metadata("guestPerformers")))
        performers_row = form.row()
        performers_row.addWidget(self.guestPerformers)
        performers_row.addWidget(add_performer)
        layout.addRow(form.labelFor(self.guestPerformers, self.tr("Guest Performers:")), performers_row)

        albums.setLayout(layout)
        return albums

    def _make_record_fields(self):
        record = QGroupBox()
        record.setTitle(self.tr("RECORD"))
        layout = form.layout()
        self.labelName = form.lineEdit("label-name")
        self.labelName.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("label_name")))
        layout.addRow(form.labelFor(self.labelName, self.tr("Label Name:")), self.labelName)
        self.catalogNumber = form.lineEdit("catalog-number")
        self.catalogNumber.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("catalogNumber")))
        layout.addRow(form.labelFor(self.catalogNumber, self.tr("Catalog Number:")), self.catalogNumber)
        self.upc = form.lineEdit("upc")
        self.upc.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("upc")))
        self.upc.setPlaceholderText("1234567899999")
        layout.addRow(form.labelFor(self.upc, self.tr("UPC/EAN:")), self.upc)
        self.mediaType = form.lineEdit("media-type")
        self.mediaType.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("mediaType")))
        layout.addRow(form.labelFor(self.mediaType, self.tr("Media Type:")), self.mediaType)
        self.releaseType = form.lineEdit("release-type")
        self.releaseType.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("releaseType")))
        # layout.addRow(form.labelFor(self.releaseType, self.tr("Release Type:")), self.releaseType)
        self.comments = form.textArea("comments")
        self.comments.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("comments")))
        layout.addRow(form.labelFor(self.comments, self.tr("Comments:")), self.comments)
        record.setLayout(layout)
        return record

    def _make_recording_fields(self):
        recording = QGroupBox()
        recording.setTitle(self.tr("RECORDING"))
        layout = form.layout()
        self.recordingStudios = form.lineEdit("recording-studios")
        self.recordingStudios.editingFinished.connect(
            lambda: self.metadataChanged.emit(self.metadata("recordingStudios")))
        layout.addRow(form.labelFor(self.recordingStudios, self.tr("Recording Studios:")), self.recordingStudios)
        self.producer = form.lineEdit("producer")
        self.producer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("producer")))
        layout.addRow(form.labelFor(self.producer, self.tr("Producer:")), self.producer)
        self.mixer = form.lineEdit("mixer")
        self.mixer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata("mixer")))
        layout.addRow(form.labelFor(self.mixer, self.tr("Mixer:")), self.mixer)
        self.primaryStyle = form.comboBox("primary-style")
        self.primaryStyle.addItems(sorted(GENRES))
        self.primaryStyle.activated.connect(lambda: self.metadataChanged.emit(self.metadata("primary_style")))
        self.primaryStyle.lineEdit().textEdited.connect(
            lambda: self.metadataChanged.emit(self.metadata("primary_style")))
        layout.addRow(form.labelFor(self.primaryStyle, self.tr("Primary Style:")), self.primaryStyle)
        recording.setLayout(layout)
        return recording

    def _disable_teaser_fields(self):
        for field in (self.digitalReleaseTime, self.originalReleaseTime, self.area, self.mediaType):#, self.releaseType):
            field.setDisabled(True)
            self._label_for(field).setDisabled(True)

    def refresh(self):
        if self.album.mainCover is not self.picture or self.album.mainCover is None:
            self.mainCover.setPixmap(image.scale(self.album.mainCover, *self.FRONT_COVER_SIZE))
            self.picture = self.album.mainCover
        self.releaseName.setText(self.album.release_name)
        self.compilation.setChecked(self.album.compilation is True)
        self._display_lead_performer(self.album)
        self.isni.setText(self.album.isni)
        self.guestPerformers.setText(formatting.toPeopleList(self.album.guestPerformers))
        self.labelName.setText(self.album.label_name)
        self.catalogNumber.setText(self.album.catalogNumber)
        self.upc.setText(self.album.upc)
        self.comments.setPlainText(self.album.comments)
        self.releaseTime.setText(self.album.releaseTime)
        self.recordingTime.setText(self.album.recording_time)
        self.recordingStudios.setText(self.album.recordingStudios)
        self.producer.setText(self.album.producer)
        self.mixer.setText(self.album.mixer)
        self.primaryStyle.setEditText(self.album.primary_style)

    def _display_lead_performer(self, album):
        # todo this should be set in the embedded metadata adapter and we should have a checkbox for various artists
        self.leadPerformer.setText(album.compilation and self.tr("Various Artists") or album.lead_performer)
        self.leadPerformer.setDisabled(album.compilation is True)

    def metadata(self, *keys):
        all_values = dict(release_name=self.releaseName.text(),
                          compilation=self.compilation.isChecked(),
                          lead_performer=self.leadPerformer.text(),
                          isni=self.isni.text(),
                          guestPerformers=formatting.fromPeopleList(self.guestPerformers.text()),
                          label_name=self.labelName.text(),
                          catalogNumber=self.catalogNumber.text(),
                          upc=self.upc.text(),
                          comments=self.comments.toPlainText(),
                          recording_time=self.recordingTime.text(),
                          releaseTime=self.releaseTime.text(),
                          recordingStudios=self.recordingStudios.text(),
                          producer=self.producer.text(),
                          mixer=self.mixer.text(),
                          primary_style=self.primaryStyle.currentText())

        if len(keys) == 0:
            return all_values

        keys_to_retrieve = [k for k in keys]
        if "compilation" not in keys_to_retrieve:
            keys_to_retrieve.append("compilation")

        if "lead_performer" not in keys_to_retrieve:
            keys_to_retrieve.append("lead_performer")

        return {k: all_values.get(k, None) for k in keys_to_retrieve}

    def _disable_mac_focus_frame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def _label_for(self, widget):
        def with_buddy(buddy):
            return lambda w: w.buddy() == buddy

        return self._child_widget(QLabel, with_buddy(widget))

    def _child_widget(self, of_type, matching):
        return next(child for child in self.findChildren(of_type) if matching(child))

    @staticmethod
    def _enable_or_disable_isni_button(compilation, lead_performer, buttons):
        is_disabled = compilation or is_blank(lead_performer)
        for button in buttons:
            button.setDisabled(is_disabled)


def is_blank(text):
    return not text or text.strip() == ""

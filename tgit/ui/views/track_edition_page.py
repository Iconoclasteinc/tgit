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

from PyQt4.QtGui import (QLabel, QLineEdit, QTimeEdit, QWidget, QSizePolicy, QGroupBox, QComboBox, QPixmap, QImage,
                         QFrame)
from tgit.languages import LANGUAGES

from tgit.ui import display, style
from tgit.ui.widgets.text_area import TextArea


def scaleImage(image, width, height):
    if image is None:
        return QPixmap()
    scaledImage = QImage.fromData(image.data).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return QPixmap.fromImage(scaledImage)


def withBuddy(buddy):
    return lambda w: w.buddy() == buddy


def makeLineEdit(name):
    edit = QLineEdit()
    edit.setObjectName(name)
    return edit


def makeLabel(name):
    label = QLabel()
    label.setObjectName(name)
    return label


def makeTextArea(name):
    text = TextArea()
    text.setObjectName(name)
    text.setTabChangesFocus(True)
    return text


def makeComboBox(name):
    combo = QComboBox()
    combo.setObjectName(name)
    combo.setEditable(True)
    combo.setInsertPolicy(QComboBox.NoInsert)
    combo.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
    return combo


def makeTimeEdit(name):
    time = QTimeEdit()
    time.setObjectName(name)
    time.setDisplayFormat('mm:ss')
    return time


def addLabelledFields(form, *fields):
    for field in fields:
        label = QLabel()
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setBuddy(field)
        form.addRow(label, field)


class TrackEditionPage(QWidget):
    NAME = 'track-edition-page'

    ALBUM_BANNER_NAME = 'album-banner'
    ALBUM_COVER_BANNER_NAME = 'album-cover'
    ALBUM_COVER_BANNER_SIZE = 60, 60
    ALBUM_TITLE_BANNER_NAME = 'album-title'
    ALBUM_LEAD_PERFORMER_BANNER_NAME = 'album-lead-performer'

    TRACK_TITLE_FIELD_NAME = 'track-title'
    LEAD_PERFORMER_FIELD_NAME = 'lead-performer'
    VERSION_INFO_FIELD_NAME = 'version-info'

    CONTENT_FIELD_SET_NAME = 'content'
    LYRICS_FIELD_NAME = 'lyrics'

    FEATURED_GUEST_FIELD_NAME = 'featured-guest'
    DURATION_FIELD_NAME = 'duration'
    TRACK_NUMBER_FIELD_NAME = 'track-number'
    TOTAL_TRACKS_FIELD_NAME = 'total-tracks'
    BITRATE_FIELD_NAME = 'bitrate'
    LYRICIST_FIELD_NAME = 'lyricist'
    COMPOSER_FIELD_NAME = 'composer'
    PUBLISHER_FIELD_NAME = 'publisher'
    ISRC_FIELD_NAME = 'isrc'
    ISWC_FIELD_NAME = 'iswc'
    TAGS_FIELD_NAME = 'tags'
    LANGUAGE_FIELD_NAME = 'language'
    PREVIEW_TIME_FIELD_NAME = 'preview-time'

    DURATION_FORMAT = 'mm:ss'

    def __init__(self):
        QWidget.__init__(self)
        self._build()
        self._disableMacFocusFrame()
        self._disableTeaserFields()
        self.translate()

    def onMetadataChange(self, callback):
        for edit in (self._trackTitleLineEdit,
                     self._leadPerformerLineEdit,
                     self._versionInfoLineEdit,
                     self._featuredGuestLineEdit,
                     self._lyricistLineEdit,
                     self._composerLineEdit,
                     self._publisherLineEdit,
                     self._isrcLineEdit,
                     self._tagsLineEdit,
                     self._lyricsTextArea):
            edit.editingFinished.connect(lambda: callback(self.trackMetadata))

        self._languageComboBox.activated.connect(lambda: callback(self.trackMetadata))
        self._languageComboBox.lineEdit().textEdited.connect(lambda: callback(self.trackMetadata))

    def _build(self):
        self.setObjectName(TrackEditionPage.NAME)
        layout = style.verticalLayout()
        layout.addWidget(self._makeAlbumBanner())
        layout.addWidget(self._makeMainContent())
        self.setLayout(layout)

    def _makeAlbumBanner(self):
        header = QFrame()
        header.setObjectName(self.ALBUM_BANNER_NAME)
        layout = style.horizontalLayout()
        self._albumCoverBannerLabel = makeLabel(self.ALBUM_COVER_BANNER_NAME)
        self._albumCoverBannerLabel.setFixedSize(*self.ALBUM_COVER_BANNER_SIZE)
        layout.addWidget(self._albumCoverBannerLabel)
        layout.addWidget(self._makeAlbumTitle())
        layout.addStretch()
        header.setLayout(layout)
        return header

    def _makeAlbumTitle(self):
        title = QWidget()
        layout = style.verticalLayout()
        self._albumTitleBannerLabel = makeLabel(self.ALBUM_TITLE_BANNER_NAME)
        self._albumTitleBannerLabel.setProperty('title', 'h2')
        layout.addWidget(self._albumTitleBannerLabel)
        self._albumLeadPerformerBannerLabel = makeLabel(self.ALBUM_LEAD_PERFORMER_BANNER_NAME)
        self._albumLeadPerformerBannerLabel.setProperty('title', 'h3')
        layout.addWidget(self._albumLeadPerformerBannerLabel)
        title.setLayout(layout)
        return title

    def _makeMainContent(self):
        content = QWidget()
        layout = style.horizontalLayout()
        layout.setSpacing(0)
        layout.addWidget(self._makeLeftColumn())
        layout.addWidget(self._makeRightColumn())
        content.setLayout(layout)
        return content

    def _makeLeftColumn(self):
        column = QWidget()
        self._trackFieldSet = self._makeTrackFieldSet()
        self._contributorsFieldSet = self._makeContributorsFieldSet()
        self._identificationFieldSet = self._makeIdentificationFieldSet()

        layout = style.verticalLayout()
        layout.addWidget(self._trackFieldSet)
        layout.addWidget(self._contributorsFieldSet)
        layout.addWidget(self._identificationFieldSet)
        layout.addStretch()

        column.setLayout(layout)
        return column

    def _makeRightColumn(self):
        column = QWidget()
        column.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self._contentFieldSet = self._makeContentFieldSet()

        layout = style.verticalLayout()
        layout.addWidget(self._contentFieldSet)
        layout.addStretch()

        column.setLayout(layout)
        return column

    def _makeTrackFieldSet(self):
        fieldSet = QGroupBox()
        self._trackTitleLineEdit = makeLineEdit(self.TRACK_TITLE_FIELD_NAME)
        self._leadPerformerLineEdit = makeLineEdit(self.LEAD_PERFORMER_FIELD_NAME)
        self._versionInfoLineEdit = makeLineEdit(self.VERSION_INFO_FIELD_NAME)
        self._trackNumberLabel = makeLabel(self.TRACK_NUMBER_FIELD_NAME)
        self._totalTracksLabel = makeLabel(self.TOTAL_TRACKS_FIELD_NAME)

        form = style.formLayout()
        addLabelledFields(form, self._trackTitleLineEdit, self._leadPerformerLineEdit, self._versionInfoLineEdit,
                          self._trackNumberLabel, self._totalTracksLabel)
        fieldSet.setLayout(form)
        return fieldSet

    def _makeContributorsFieldSet(self):
        fieldSet = QGroupBox()
        self._featuredGuestLineEdit = makeLineEdit(self.FEATURED_GUEST_FIELD_NAME)
        self._lyricistLineEdit = makeLineEdit(self.LYRICIST_FIELD_NAME)
        self._composerLineEdit = makeLineEdit(self.COMPOSER_FIELD_NAME)
        self._publisherLineEdit = makeLineEdit(self.PUBLISHER_FIELD_NAME)

        form = style.formLayout()
        addLabelledFields(form, self._featuredGuestLineEdit, self._lyricistLineEdit, self._composerLineEdit,
                          self._publisherLineEdit)
        fieldSet.setLayout(form)
        return fieldSet

    def _makeIdentificationFieldSet(self):
        fieldSet = QGroupBox()
        self._isrcLineEdit = makeLineEdit(self.ISRC_FIELD_NAME)
        self._iswcLineEdit = makeLineEdit(self.ISWC_FIELD_NAME)
        self._tagsLineEdit = makeLineEdit(self.TAGS_FIELD_NAME)

        form = style.formLayout()
        addLabelledFields(form, self._isrcLineEdit, self._iswcLineEdit, self._tagsLineEdit)
        fieldSet.setLayout(form)
        return fieldSet

    def _makeContentFieldSet(self):
        fieldSet = QGroupBox()
        fieldSet.setObjectName(self.CONTENT_FIELD_SET_NAME)
        self._lyricsTextArea = makeTextArea(self.LYRICS_FIELD_NAME)
        self._languageComboBox = makeComboBox(self.LANGUAGE_FIELD_NAME)
        self._languageComboBox.addItems(sorted(LANGUAGES))
        self._previewTimeEdit = makeTimeEdit(self.PREVIEW_TIME_FIELD_NAME)
        self._durationLabel = makeLabel(self.DURATION_FIELD_NAME)
        self._bitrateLabel = makeLabel(self.BITRATE_FIELD_NAME)
        form = style.formLayout()
        addLabelledFields(form, self._lyricsTextArea, self._languageComboBox, self._previewTimeEdit,
                          self._durationLabel, self._bitrateLabel)
        fieldSet.setLayout(form)
        return fieldSet

    def updateTrack(self, track, album):
        self._albumCoverBannerLabel.setPixmap(scaleImage(album.mainCover, *self.ALBUM_COVER_BANNER_SIZE))
        self._albumTitleBannerLabel.setText(album.releaseName)
        self._albumLeadPerformerBannerLabel.setText(album.compilation and self.tr('Various Artists') or album.leadPerformer)
        self._trackTitleLineEdit.setText(track.trackTitle)
        self._leadPerformerLineEdit.setText(track.leadPerformer)
        self._leadPerformerLineEdit.setEnabled(track.compilation is True)
        self._versionInfoLineEdit.setText(track.versionInfo)
        self._durationLabel.setText(display.asDuration(track.duration))
        self._bitrateLabel.setText('%s kbps' % display.inKbps(track.bitrate))
        self._trackNumberLabel.setText(str(album.positionOf(track) + 1))
        self._totalTracksLabel.setText(str(len(album)))
        self._featuredGuestLineEdit.setText(track.featuredGuest)
        self._lyricistLineEdit.setText(track.lyricist)
        self._composerLineEdit.setText(track.composer)
        self._publisherLineEdit.setText(track.publisher)
        self._isrcLineEdit.setText(track.isrc)
        self._tagsLineEdit.setText(track.tags)
        self._lyricsTextArea.setPlainText(track.lyrics)
        self._languageComboBox.setEditText(track.language)

    @property
    def trackMetadata(self):
        class Snapshot(object):
            def __str__(self):
                return str(self.__dict__)

        snapshot = Snapshot()
        snapshot.trackTitle = self._trackTitleLineEdit.text()
        snapshot.leadPerformer = self._leadPerformerLineEdit.text()
        snapshot.versionInfo = self._versionInfoLineEdit.text()
        snapshot.featuredGuest = self._featuredGuestLineEdit.text()
        snapshot.lyricist = self._lyricistLineEdit.text()
        snapshot.composer = self._composerLineEdit.text()
        snapshot.publisher = self._publisherLineEdit.text()
        snapshot.isrc = self._isrcLineEdit.text()
        snapshot.tags = self._tagsLineEdit.text()
        snapshot.lyrics = self._lyricsTextArea.toPlainText()
        snapshot.language = self._languageComboBox.currentText()
        return snapshot

    def _disableMacFocusFrame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def _disableTeaserFields(self):
        for field in (self._iswcLineEdit, self._previewTimeEdit):
            field.setDisabled(True)
            self._labelFor(field).setDisabled(True)

    def translate(self):
        self._translateTrackFields()
        self._translateContributorFields()
        self._translateIdentificationFields()
        self._translateContentFields()

    def _translateTrackFields(self):
        self._trackFieldSet.setTitle(self.tr('TRACK'))
        self._labelFor(self._trackTitleLineEdit).setText(self.tr('Track Title: '))
        self._labelFor(self._leadPerformerLineEdit).setText(self.tr('Lead Performer: '))
        self._labelFor(self._versionInfoLineEdit).setText(self.tr('Version Information: '))
        self._labelFor(self._trackNumberLabel).setText(self.tr('Track Number: '))
        self._labelFor(self._totalTracksLabel).setText(self.tr('Total Tracks: '))

    def _translateContributorFields(self):
        self._contributorsFieldSet.setTitle(self.tr('CONTRIBUTORS'))
        self._labelFor(self._featuredGuestLineEdit).setText(self.tr('Featured Guest: '))
        self._labelFor(self._lyricistLineEdit).setText(self.tr('Lyricist: '))
        self._labelFor(self._composerLineEdit).setText(self.tr('Composer: '))
        self._labelFor(self._publisherLineEdit).setText(self.tr('Publisher: '))

    def _translateIdentificationFields(self):
        self._identificationFieldSet.setTitle(self.tr('IDENTIFICATION'))
        self._labelFor(self._isrcLineEdit).setText('ISRC: ')
        self._isrcLineEdit.setPlaceholderText('ZZZ123456789')
        self._labelFor(self._iswcLineEdit).setText(self.tr('ISWC: '))
        self._labelFor(self._tagsLineEdit).setText(self.tr('Tags: '))
        self._tagsLineEdit.setPlaceholderText(self.tr('tag1, tag2, tag3 ...'))

    def _translateContentFields(self):
        self._contentFieldSet.setTitle(self.tr('CONTENT'))
        self._labelFor(self._lyricsTextArea).setText(self.tr('Lyrics: '))
        self._labelFor(self._languageComboBox).setText(self.tr('Language: '))
        self._labelFor(self._previewTimeEdit).setText(self.tr('Preview Time: '))
        self._labelFor(self._durationLabel).setText(self.tr('Duration: '))
        self._labelFor(self._bitrateLabel).setText(self.tr('Bitrate: '))

    def _labelFor(self, widget):
        return self._child(QLabel, withBuddy(widget))

    def _child(self, ofType, matching):
        return next(child for child in self.findChildren(ofType) if matching(child))
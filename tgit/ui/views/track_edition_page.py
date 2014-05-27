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
from dateutil import tz, parser as dateparser

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QLabel, QWidget, QGroupBox, QFrame)

from tgit.languages import LANGUAGES
from tgit.ui import display, style, formatting
from tgit.ui.widgets import form, image


class TrackEditionPage(QWidget):
    ALBUM_COVER_SIZE = 60, 60
    DURATION_FORMAT = 'mm:ss'

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName('track-edition-page')
        self.render()
        self.cover = None

    def bind(self, **handlers):
        if 'metadataChanged' in handlers:
            self.onMetadataChange(handlers['metadataChanged'])

    def onMetadataChange(self, handler):
        for edit in (self.trackTitle,
                     self.leadPerformer,
                     self.versionInfo,
                     self.featuredGuest,
                     self.lyricist,
                     self.composer,
                     self.publisher,
                     self.isrc,
                     self.tags,
                     self.lyrics):
            edit.editingFinished.connect(lambda: handler(self.trackMetadata))

        self.languages.activated.connect(lambda: handler(self.trackMetadata))
        self.languages.lineEdit().textEdited.connect(lambda: handler(self.trackMetadata))

    def render(self):
        layout = form.column()
        layout.addWidget(self.makeAlbumBanner())
        layout.addWidget(self.makeMainContent())
        self.setLayout(layout)
        self.disableMacFocusFrame()
        self.disableTeaserFields()

    def makeAlbumBanner(self):
        header = QFrame()
        header.setObjectName('album-banner')
        layout = form.row()
        layout.addWidget(self.makeAlbumCover())
        layout.addWidget(self.makeAlbumTitle())
        layout.addStretch()
        layout.addWidget(self.makeRecordLabel())
        layout.addStretch()
        layout.addStretch()
        layout.addWidget(self.makeTrackNumber())
        header.setLayout(layout)
        return header

    def makeAlbumCover(self):
        self.albumCover = form.label('album-cover')
        self.albumCover.setFixedSize(*self.ALBUM_COVER_SIZE)
        return self.albumCover

    def makeAlbumTitle(self):
        title = QWidget()
        layout = form.column()
        self.albumTitle = form.label('album-title')
        self.albumTitle.setProperty('title', 'h2')
        layout.addWidget(self.albumTitle)
        self.albumLeadPerformer = form.label('album-lead-performer')
        self.albumLeadPerformer.setProperty('title', 'h3')
        layout.addWidget(self.albumLeadPerformer)
        layout.addStretch()
        title.setLayout(layout)
        return title

    def makeRecordLabel(self):
        label = QWidget()
        layout = form.column()
        layout.addStretch()
        self.recordLabel = form.label('record-label')
        self.recordLabel.setProperty('title', 'h2')
        layout.addWidget(self.recordLabel)
        push = QLabel()
        push.setProperty('title', 'h3')
        layout.addWidget(push)
        layout.addStretch()
        label.setLayout(layout)
        return label

    def makeTrackNumber(self):
        numbering = QWidget()
        layout = form.column()
        layout.addStretch()
        self.trackNumber = form.label('track-number')
        self.trackNumber.setProperty('title', 'h3')
        self.trackNumber.setAlignment(Qt.AlignRight)
        layout.addWidget(self.trackNumber)
        numbering.setLayout(layout)
        return numbering

    def makeMainContent(self):
        content = QWidget()
        layout = form.row()
        layout.setSpacing(0)
        layout.addWidget(self.makeLeftColumn())
        layout.addWidget(self.makeRightColumn())
        content.setLayout(layout)
        return content

    def makeLeftColumn(self):
        column = QWidget()
        layout = form.column()
        layout.addWidget(self.makeTrackFields())
        layout.addWidget(self.makeContributorsFields())
        layout.addWidget(self.makeIdentificationFields())
        layout.addStretch()
        column.setLayout(layout)
        return column

    def makeTrackFields(self):
        fieldSet = QGroupBox()
        fieldSet.setTitle(self.tr('TRACK'))
        layout = form.layout()
        self.trackTitle = form.lineEdit('track-title')
        layout.addRow(form.labelFor(self.trackTitle, self.tr('Track Title: ')), self.trackTitle)
        self.leadPerformer = form.lineEdit('lead-performer')
        layout.addRow(form.labelFor(self.leadPerformer, self.tr('Lead Performer: ')), self.leadPerformer)
        self.versionInfo = form.lineEdit('version-info')
        layout.addRow(form.labelFor(self.versionInfo, self.tr('Version Information: ')), self.versionInfo)
        fieldSet.setLayout(layout)
        return fieldSet

    def makeContributorsFields(self):
        fieldSet = QGroupBox()
        fieldSet.setTitle(self.tr('CONTRIBUTORS'))
        layout = form.layout()
        self.featuredGuest = form.lineEdit('featured-guest')
        layout.addRow(form.labelFor(self.featuredGuest, self.tr('Featured Guest: ')), self.featuredGuest)
        self.lyricist = form.lineEdit('lyricist')
        layout.addRow(form.labelFor(self.lyricist, self.tr('Lyricist: ')), self.lyricist)
        self.composer = form.lineEdit('composer')
        layout.addRow(form.labelFor(self.composer, self.tr('Composer: ')), self.composer)
        self.publisher = form.lineEdit('publisher')
        layout.addRow(form.labelFor(self.publisher, self.tr('Publisher: ')), self.publisher)
        fieldSet.setLayout(layout)
        return fieldSet

    def makeIdentificationFields(self):
        fieldSet = QGroupBox()
        fieldSet.setTitle(self.tr('IDENTIFICATION'))
        layout = form.layout()
        self.isrc = form.lineEdit('isrc')
        self.isrc.setPlaceholderText('ZZZ123456789')
        layout.addRow(form.labelFor(self.isrc, self.tr('ISRC: ')), self.isrc)
        self.iswc = form.lineEdit('iswc')
        layout.addRow(form.labelFor(self.iswc, self.tr('ISWC: ')), self.iswc)
        self.tags = form.lineEdit('tags')
        self.tags.setPlaceholderText(self.tr('tag1, tag2, tag3 ...'))
        layout.addRow(form.labelFor(self.tags, self.tr('Tags: ')), self.tags)
        fieldSet.setLayout(layout)
        return fieldSet

    def makeRightColumn(self):
        column = QWidget()
        layout = form.column()
        layout.addWidget(self.makeContentFields())
        layout.addLayout(self.makeNotice())
        column.setLayout(layout)
        return column

    def makeContentFields(self):
        fieldSet = QGroupBox()
        fieldSet.setObjectName('content')
        fieldSet.setTitle(self.tr('CONTENT'))
        layout = style.formLayout()
        self.lyrics = form.textArea('lyrics')
        layout.addRow(form.labelFor(self.lyrics, self.tr('Lyrics: ')), self.lyrics)
        self.languages = form.comboBox('languages')
        self.languages.addItems(sorted(LANGUAGES))
        layout.addRow(form.labelFor(self.languages, self.tr('Language: ')), self.languages)
        self.previewTime = form.timeEdit('preview-time')
        layout.addRow(form.labelFor(self.previewTime, self.tr('Preview Time: ')), self.previewTime)
        self.duration = form.label('duration')
        layout.addRow(form.labelFor(self.duration, self.tr('Duration: ')), self.duration)
        self.bitrate = form.label('bitrate')
        layout.addRow(form.labelFor(self.bitrate, self.tr('Bitrate: ')), self.bitrate)
        fieldSet.setLayout(layout)
        return fieldSet

    def makeNotice(self):
        layout = form.row()
        layout.addStretch()
        self.softwareNotice = form.label('software-notice')
        layout.addWidget(self.softwareNotice)
        return layout

    def display(self, track):
        album = track.album
        self.displayAlbumCover(album)
        self.albumTitle.setText(album.releaseName)
        self.albumLeadPerformer.setText(album.compilation and self.tr('Various Artists') or album.leadPerformer)
        self.recordLabel.setText(album.labelName)
        self.trackNumber.setText(self.tr('Track %d of %d') % (track.number, len(album)))
        self.trackTitle.setText(track.trackTitle)
        self.leadPerformer.setText(track.leadPerformer)
        self.leadPerformer.setEnabled(track.compilation is True)
        self.versionInfo.setText(track.versionInfo)
        self.duration.setText(display.asDuration(track.duration))
        self.bitrate.setText('%s kbps' % formatting.toKbps(track.bitrate))
        self.featuredGuest.setText(track.featuredGuest)
        self.lyricist.setText(track.lyricist)
        self.composer.setText(track.composer)
        self.publisher.setText(track.publisher)
        self.isrc.setText(track.isrc)
        self.tags.setText(track.tags)
        self.lyrics.setPlainText(track.lyrics)
        self.languages.setEditText(track.language)
        self.displaySoftwareNotice(track)

    def displayAlbumCover(self, album):
        # Cache the cover image to avoid recomputing the image each time the screen updates
        if self.cover is not album.mainCover:
            self.cover = album.mainCover
            self.albumCover.setPixmap(image.scale(self.cover, *self.ALBUM_COVER_SIZE))

    def displaySoftwareNotice(self, track):
        date, time = self.parseTaggingTime(track)
        if track.tagger and date and time:
            self.softwareNotice.setText(self.tr('Tagged with %s on %s at %s') % (track.tagger, date, time))

    @staticmethod
    def parseTaggingTime(track):
        try:
            localTaggingTime = dateparser.parse(track.taggingTime).astimezone(tz.tzlocal())
        except:
            return None, None

        return localTaggingTime.strftime('%Y-%m-%d'), localTaggingTime.strftime('%H:%M:%S')

    @property
    def trackMetadata(self):
        # todo move Snapshot to top level
        class Snapshot(object):
            def __str__(self):
                return str(self.__dict__)

        snapshot = Snapshot()
        snapshot.trackTitle = self.trackTitle.text()
        snapshot.leadPerformer = self.leadPerformer.text()
        snapshot.versionInfo = self.versionInfo.text()
        snapshot.featuredGuest = self.featuredGuest.text()
        snapshot.lyricist = self.lyricist.text()
        snapshot.composer = self.composer.text()
        snapshot.publisher = self.publisher.text()
        snapshot.isrc = self.isrc.text()
        snapshot.tags = self.tags.text()
        snapshot.lyrics = self.lyrics.toPlainText()
        snapshot.language = self.languages.currentText()
        return snapshot

    def disableMacFocusFrame(self):
        for child in self.findChildren(QWidget):
            child.setAttribute(Qt.WA_MacShowFocusRect, False)

    def disableTeaserFields(self):
        for field in (self.iswc, self.previewTime):
            field.setDisabled(True)
            self.labelFor(field).setDisabled(True)

    def labelFor(self, widget):
        def withBuddy(buddy):
            return lambda w: w.buddy() == buddy
        return self.childWidget(QLabel, withBuddy(widget))

    def childWidget(self, ofType, matching):
        return next(child for child in self.findChildren(ofType) if matching(child))
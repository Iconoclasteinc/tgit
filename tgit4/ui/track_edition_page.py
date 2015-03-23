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
from PyQt4.QtGui import (QLabel, QWidget, QGroupBox, QFrame)

from tgit4.album import AlbumListener
from tgit4.languages import LANGUAGES
from tgit4.track import TrackListener
from tgit4.ui.helpers import form, image, formatting


class TrackEditionPage(QWidget, TrackListener, AlbumListener):
    metadataChanged = pyqtSignal(dict)

    ALBUM_COVER_SIZE = 60, 60
    DURATION_FORMAT = 'mm:ss'

    def __init__(self, album, track):
        QWidget.__init__(self)
        # we need this until track knows its position in the album
        self.album = album
        self.track = track
        self.cover = None
        self.build()

    def build(self):
        self.setObjectName('track-edition-page')
        layout = form.column()
        layout.addWidget(self.makeAlbumBanner())
        layout.addWidget(self.makeMainContent())
        self.setLayout(layout)
        self.disableMacFocusFrame()
        self.disableTeaserFields()

    def albumStateChanged(self, album):
        self.display(album=album)

    def trackStateChanged(self, track):
        self.display(track=track)

    # will eventually go away
    # but first we need track to know its track number and total tracks
    def trackAdded(self, track, position):
        self.display(track=self.track)

    # will eventually go away
    # but first we need track to know its track number and total tracks
    def trackRemoved(self, track, position):
        if track == self.track:
            self.album.removeAlbumListener(self)
        else:
            self.display(track=self.track)

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
        self.trackTitle.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.trackTitle, self.tr('Track Title: ')), self.trackTitle)
        self.leadPerformer = form.lineEdit('lead-performer')
        self.leadPerformer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.leadPerformer, self.tr('Lead Performer: ')), self.leadPerformer)
        self.versionInfo = form.lineEdit('version-info')
        self.versionInfo.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.versionInfo, self.tr('Version Information: ')), self.versionInfo)
        fieldSet.setLayout(layout)
        return fieldSet

    def makeContributorsFields(self):
        fieldSet = QGroupBox()
        fieldSet.setTitle(self.tr('CONTRIBUTORS'))
        layout = form.layout()
        self.featuredGuest = form.lineEdit('featured-guest')
        self.featuredGuest.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.featuredGuest, self.tr('Featured Guest: ')), self.featuredGuest)
        self.lyricist = form.lineEdit('lyricist')
        self.lyricist.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.lyricist, self.tr('Lyricist: ')), self.lyricist)
        self.composer = form.lineEdit('composer')
        self.composer.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.composer, self.tr('Composer: ')), self.composer)
        self.publisher = form.lineEdit('publisher')
        self.publisher.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.publisher, self.tr('Publisher: ')), self.publisher)
        fieldSet.setLayout(layout)
        return fieldSet

    def makeIdentificationFields(self):
        fieldSet = QGroupBox()
        fieldSet.setTitle(self.tr('IDENTIFICATION'))
        layout = form.layout()
        self.isrc = form.lineEdit('isrc')
        self.isrc.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        self.isrc.setPlaceholderText('ZZZ123456789')
        layout.addRow(form.labelFor(self.isrc, self.tr('ISRC: ')), self.isrc)
        self.iswc = form.lineEdit('iswc')
        self.iswc.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.iswc, self.tr('ISWC: ')), self.iswc)
        self.tags = form.lineEdit('tags')
        self.tags.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
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
        layout = form.layout()
        self.lyrics = form.textArea('lyrics')
        self.lyrics.editingFinished.connect(lambda: self.metadataChanged.emit(self.metadata))
        layout.addRow(form.labelFor(self.lyrics, self.tr('Lyrics: ')), self.lyrics)
        self.languages = form.comboBox('languages')
        self.languages.addItems(sorted(LANGUAGES))
        self.languages.activated.connect(lambda: self.metadataChanged.emit(self.metadata))
        self.languages.lineEdit().textEdited.connect(lambda: self.metadataChanged.emit(self.metadata))
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

    def display(self, album=None, track=None):
        if album:
            self.displayAlbum(album)
        if track:
            self.displayTrack(track)

    def displayAlbum(self, album):
        self.displayAlbumCover(album.mainCover)
        self.albumTitle.setText(album.releaseName)
        self.albumLeadPerformer.setText(album.compilation and self.tr('Various Artists') or album.leadPerformer)
        self.recordLabel.setText(album.labelName)
        self.leadPerformer.setEnabled(album.compilation is True)

    def displayTrack(self, track):
        self.trackNumber.setText(self.tr('Track %d of %d') % (track.number, len(self.album)))
        self.trackTitle.setText(track.trackTitle)
        self.leadPerformer.setText(track.leadPerformer)
        self.versionInfo.setText(track.versionInfo)
        self.duration.setText(formatting.toDuration(track.duration))
        self.bitrate.setText('%s kbps' % formatting.inKbps(track.bitrate))
        self.featuredGuest.setText(track.featuredGuest)
        self.lyricist.setText(track.lyricist)
        self.composer.setText(track.composer)
        self.publisher.setText(track.publisher)
        self.isrc.setText(track.isrc)
        self.tags.setText(track.labels)
        self.lyrics.setPlainText(track.lyrics)
        self.languages.setEditText(track.language)
        self.displaySoftwareNotice(track.taggingTime, track.tagger)

    def displayAlbumCover(self, picture):
        # Cache the cover image to avoid recomputing the image each time the screen updates
        if self.cover is not picture:
            self.cover = picture
            self.albumCover.setPixmap(image.scale(self.cover, *self.ALBUM_COVER_SIZE))

    def displaySoftwareNotice(self, taggingTime, tagger):
        try:
            date, time = formatting.asLocalDateTime(taggingTime)
        except:
            date, time = None, None

        if tagger and date and time:
            self.softwareNotice.setText(self.tr('Tagged with %s on %s at %s') % (tagger, date, time))

    @property
    def metadata(self):
        return dict(trackTitle=self.trackTitle.text(),
                    leadPerformer=self.leadPerformer.text(),
                    versionInfo=self.versionInfo.text(),
                    featuredGuest=self.featuredGuest.text(),
                    lyricist=self.lyricist.text(),
                    composer=self.composer.text(),
                    publisher=self.publisher.text(),
                    isrc=self.isrc.text(),
                    labels=self.tags.text(),
                    lyrics=self.lyrics.toPlainText(),
                    language=self.languages.currentText())

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
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

from PyQt4.QtGui import (QGridLayout, QVBoxLayout, QLabel, QLineEdit, QTimeEdit, QWidget)

from tgit.announcer import Announcer
from tgit.ui import display
from tgit.ui.text_area import TextArea


DURATION_FORMAT = 'mm:ss'


def trackEditionPage(listener):
    page = TrackEditionPage()
    page.announceTo(listener)
    return page


class TrackEditionPage(object):
    NAME = 'track-edition-page'

    TRACK_TITLE_FIELD_NAME = 'track-title'
    LEAD_PERFORMER_FIELD_NAME = 'lead-performer'
    VERSION_INFO_FIELD_NAME = 'version-info'
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
    LYRICS_FIELD_NAME = 'lyrics'
    LANGUAGE_FIELD_NAME = 'language'
    PREVIEW_TIME_FIELD_NAME = 'preview-time'

    DURATION_FORMAT = 'mm:ss'

    def __init__(self):
        self._announce = Announcer()

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def render(self):
        self._widget = self._build()
        self.translate()
        return self._widget

    def _build(self):
        widget = QWidget()
        widget.setObjectName(TrackEditionPage.NAME)
        layout = QVBoxLayout()
        grid = QGridLayout()
        self._fill(grid)
        layout.addLayout(grid)
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def _fill(self, layout):
        self._addTrackTitle(layout, 0)
        self._addLeadPerformer(layout, 1)
        self._addVersionInfo(layout, 2)
        self._addFeaturedGuest(layout, 3)
        self._addDuration(layout, 4)
        self._addTrackNumber(layout, 5)
        self._addTotalTracks(layout, 6)
        self._addBitrate(layout, 7)
        self._addLyricist(layout, 8)
        self._addComposer(layout, 9)
        self._addPublisher(layout, 10)
        self._addIsrc(layout, 11)
        self._addIswc(layout, 12)
        self._addTags(layout, 13)
        self._addLyrics(layout, 14)
        self._addLanguage(layout, 15)
        self._addPreviewTime(layout, 16)

    def _addTrackTitle(self, layout, row):
        self._trackTitleLabel = QLabel()
        layout.addWidget(self._trackTitleLabel, row, 0)
        self._trackTitleEdit = QLineEdit()
        self._trackTitleEdit.setObjectName(TrackEditionPage.TRACK_TITLE_FIELD_NAME)
        self._trackTitleEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._trackTitleEdit, row, 1)
        self._trackTitleLabel.setBuddy(self._trackTitleEdit)

    def _addLeadPerformer(self, layout, row):
        self._leadPerformerLabel = QLabel()
        layout.addWidget(self._leadPerformerLabel, row, 0)
        self._leadPerformerEdit = QLineEdit()
        self._leadPerformerEdit.setObjectName(TrackEditionPage.LEAD_PERFORMER_FIELD_NAME)
        self._leadPerformerEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._leadPerformerEdit, row, 1)
        self._leadPerformerLabel.setBuddy(self._leadPerformerEdit)

    def _addVersionInfo(self, layout, row):
        self._versionInfoLabel = QLabel()
        layout.addWidget(self._versionInfoLabel, row, 0)
        self._versionInfoEdit = QLineEdit()
        self._versionInfoEdit.setObjectName(self.VERSION_INFO_FIELD_NAME)
        self._versionInfoEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._versionInfoEdit, row, 1)
        self._versionInfoLabel.setBuddy(self._versionInfoEdit)

    def _addDuration(self, layout, row):
        self._durationLabel = QLabel()
        layout.addWidget(self._durationLabel, row, 0)
        self._durationValueLabel = QLabel()
        self._durationValueLabel.setObjectName(self.DURATION_FIELD_NAME)
        layout.addWidget(self._durationValueLabel, row, 1)
        self._durationLabel.setBuddy(self._durationValueLabel)

    def _addTrackNumber(self, layout, row):
        self._trackNumberLabel = QLabel()
        layout.addWidget(self._trackNumberLabel, row, 0)
        self._trackNumberValueLabel = QLabel()
        self._trackNumberValueLabel.setObjectName(self.TRACK_NUMBER_FIELD_NAME)
        layout.addWidget(self._trackNumberValueLabel, row, 1)
        self._trackNumberLabel.setBuddy(self._trackNumberValueLabel)

    def _addTotalTracks(self, layout, row):
        self._totalTracksLabel = QLabel()
        layout.addWidget(self._totalTracksLabel, row, 0)
        self._totalTracksValueLabel = QLabel()
        self._totalTracksValueLabel.setObjectName(self.TOTAL_TRACKS_FIELD_NAME)
        layout.addWidget(self._totalTracksValueLabel, row, 1)
        self._totalTracksLabel.setBuddy(self._totalTracksValueLabel)

    def _addBitrate(self, layout, row):
        self._bitrateLabel = QLabel()
        layout.addWidget(self._bitrateLabel, row, 0)
        self._bitrateValueLabel = QLabel()
        self._bitrateValueLabel.setObjectName(self.BITRATE_FIELD_NAME)
        layout.addWidget(self._bitrateValueLabel, row, 1)
        self._bitrateLabel.setBuddy(self._bitrateValueLabel)

    def _addFeaturedGuest(self, layout, row):
        self._featuredGuestLabel = QLabel()
        layout.addWidget(self._featuredGuestLabel, row, 0)
        self._featuredGuestEdit = QLineEdit()
        self._featuredGuestEdit.setObjectName(self.FEATURED_GUEST_FIELD_NAME)
        self._featuredGuestEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._featuredGuestEdit, row, 1)
        self._featuredGuestLabel.setBuddy(self._featuredGuestEdit)

    def _addLyricist(self, layout, row):
        self._lyricistLabel = QLabel()
        layout.addWidget(self._lyricistLabel, row, 0)
        self._lyricistEdit = QLineEdit()
        self._lyricistEdit.setObjectName(self.LYRICIST_FIELD_NAME)
        self._lyricistEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._lyricistEdit, row, 1)
        self._lyricistLabel.setBuddy(self._lyricistEdit)

    def _addComposer(self, layout, row):
        self._composerLabel = QLabel()
        layout.addWidget(self._composerLabel, row, 0)
        self._composerEdit = QLineEdit()
        self._composerEdit.setObjectName(self.COMPOSER_FIELD_NAME)
        self._composerEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._composerEdit, row, 1)
        self._composerLabel.setBuddy(self._composerEdit)

    def _addPublisher(self, layout, row):
        self._publisherLabel = QLabel()
        layout.addWidget(self._publisherLabel, row, 0)
        self._publisherEdit = QLineEdit()
        self._publisherEdit.setObjectName(self.PUBLISHER_FIELD_NAME)
        self._publisherEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._publisherEdit, row, 1)
        self._publisherLabel.setBuddy(self._publisherEdit)

    def _addIsrc(self, layout, row):
        self._isrcLabel = QLabel()
        layout.addWidget(self._isrcLabel, row, 0)
        self._isrcEdit = QLineEdit()
        self._isrcEdit.setObjectName(self.ISRC_FIELD_NAME)
        self._isrcEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._isrcEdit, row, 1)
        self._isrcLabel.setBuddy(self._isrcEdit)

    def _addIswc(self, layout, row):
        self._iswcLabel = QLabel()
        self._iswcLabel.setDisabled(True)
        layout.addWidget(self._iswcLabel, row, 0)
        self._iswcEdit = QLineEdit()
        self._iswcEdit.setObjectName(self.ISWC_FIELD_NAME)
        self._iswcEdit.setDisabled(True)
        layout.addWidget(self._iswcEdit, row, 1)
        self._iswcLabel.setBuddy(self._iswcEdit)

    def _addTags(self, layout, row):
        self._tagsLabel = QLabel()
        layout.addWidget(self._tagsLabel, row, 0)
        self._tagsEdit = QLineEdit()
        self._tagsEdit.setObjectName(self.TAGS_FIELD_NAME)
        self._tagsEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._tagsEdit, row, 1)
        self._tagsLabel.setBuddy(self._tagsEdit)

    def _addLyrics(self, layout, row):
        self._lyricsLabel = QLabel()
        layout.addWidget(self._lyricsLabel, row, 0)
        self._lyricsEdit = TextArea()
        self._lyricsEdit.setObjectName(self.LYRICS_FIELD_NAME)
        self._lyricsEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._lyricsEdit, row, 1)
        self._lyricsLabel.setBuddy(self._lyricsEdit)

    def _addLanguage(self, layout, row):
        self._languageLabel = QLabel()
        layout.addWidget(self._languageLabel, row, 0)
        self._languageEdit = QLineEdit()
        self._languageEdit.setObjectName(self.LANGUAGE_FIELD_NAME)
        self._languageEdit.editingFinished.connect(self._signalMetadataChange)
        layout.addWidget(self._languageEdit, row, 1)
        self._languageLabel.setBuddy(self._languageEdit)

    def _addPreviewTime(self, layout, row):
        self._previewTimeLabel = QLabel()
        self._previewTimeLabel.setDisabled(True)
        layout.addWidget(self._previewTimeLabel, row, 0)
        self._previewTimeEdit = QTimeEdit()
        self._previewTimeEdit.setDisplayFormat(self.DURATION_FORMAT)
        # self._previewTimeEdit.setTime(QTime.fromString('00:00'))
        self._previewTimeEdit.setObjectName(self.PREVIEW_TIME_FIELD_NAME)
        self._previewTimeEdit.setDisabled(True)
        layout.addWidget(self._previewTimeEdit, row, 1)
        self._previewTimeLabel.setBuddy(self._previewTimeEdit)

    def show(self, album, track):
        self._trackTitleEdit.setText(track.trackTitle)
        self._leadPerformerEdit.setText(track.leadPerformer)
        self._versionInfoEdit.setText(track.versionInfo)
        self._durationValueLabel.setText(display.asDuration(track.duration))
        self._trackNumberValueLabel.setText(str(album.positionOf(track) + 1))
        self._totalTracksValueLabel.setText(str(len(album)))
        self._bitrateValueLabel.setText('%s kbps' % display.inKbps(track.bitrate))
        self._featuredGuestEdit.setText(track.featuredGuest)
        self._lyricistEdit.setText(track.lyricist)
        self._composerEdit.setText(track.composer)
        self._publisherEdit.setText(track.publisher)
        self._isrcEdit.setText(track.isrc)
        self._tagsEdit.setText(track.tags)
        self._lyricsEdit.setPlainText(track.lyrics)
        self._languageEdit.setText(track.language)

    @property
    def trackMetadata(self):
        class Snapshot(object):
            def __str__(self):
                return str(self.__dict__)

        snapshot = Snapshot()
        snapshot.trackTitle = self._trackTitleEdit.text()
        snapshot.leadPerformer = self._leadPerformerEdit.text()
        snapshot.versionInfo = self._versionInfoEdit.text()
        snapshot.featuredGuest = self._featuredGuestEdit.text()
        snapshot.lyricist = self._lyricistEdit.text()
        snapshot.composer = self._composerEdit.text()
        snapshot.publisher = self._publisherEdit.text()
        snapshot.isrc = self._isrcEdit.text()
        snapshot.tags = self._tagsEdit.text()
        snapshot.lyrics = self._lyricsEdit.toPlainText()
        snapshot.language = self._languageEdit.text()
        return snapshot

    def _signalMetadataChange(self):
        self._announce.metadataEdited(self.trackMetadata)

    def translate(self):
        self._trackTitleLabel.setText(self.tr('Track Title: '))
        self._leadPerformerLabel.setText(self.tr('Lead Performer: '))
        self._versionInfoLabel.setText(self.tr('Version Information: '))
        self._durationLabel.setText(self.tr('Duration: '))
        self._trackNumberLabel.setText(self.tr('Track: '))
        self._totalTracksLabel.setText(self.tr('Of: '))
        self._bitrateLabel.setText(self.tr('Bitrate: '))
        self._featuredGuestLabel.setText(self.tr('Featured Guest: '))
        self._lyricistLabel.setText(self.tr('Lyricist: '))
        self._composerLabel.setText(self.tr('Composer: '))
        self._publisherLabel.setText(self.tr('Publisher: '))
        self._isrcLabel.setText(self.tr('ISRC: '))
        self._isrcEdit.setPlaceholderText(self.tr('ZZZ123456789'))
        self._iswcLabel.setText(self.tr('ISWC: '))
        self._tagsLabel.setText(self.tr('Tags: '))
        self._tagsEdit.setPlaceholderText(self.tr('tag1, tag2, tag3 ...'))
        self._lyricsLabel.setText(self.tr('Lyrics: '))
        self._languageLabel.setText(self.tr('Language: '))
        self._languageEdit.setPlaceholderText(self.tr('fra, eng, und (for undetermined), '
                                                        'or mul (for multiple languages)'))
        self._previewTimeLabel.setText(self.tr('Preview Time: '))

    def tr(self, text):
        return self._widget.tr(text)
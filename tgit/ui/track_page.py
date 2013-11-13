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

from PyQt4.QtGui import (QWidget, QGridLayout, QVBoxLayout, QLabel, QLineEdit, QTimeEdit)

from tgit.album import AlbumListener
from tgit.track import TrackListener
from tgit.ui import constants as ui, display
from tgit.ui.text_area import TextArea


DURATION_FORMAT = 'mm:ss'


class TrackPage(QWidget, AlbumListener, TrackListener):
    def __init__(self, album, track, parent=None):
        QWidget.__init__(self, parent)
        self._album = album
        self._album.addAlbumListener(self)
        self._track = track
        self._track.addTrackListener(self)

        self._assemble()

    def _assemble(self):
        self.setObjectName(ui.TRACK_PAGE_NAME)
        grid = QGridLayout()
        self._fill(grid)
        self.translateUi()
        self._layout(grid)
        self.trackStateChanged(self._track)

    def _layout(self, grid):
        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def _fill(self, layout):
        self._addTrackTitle(layout, 0)
        self._addVersionInfo(layout, 1)
        self._addDuration(layout, 2)
        self._addTrackNumber(layout, 3)
        self._addTotalTracks(layout, 4)
        self._addBitrate(layout, 5)
        self._addFeaturedGuest(layout, 6)
        self._addLyricist(layout, 7)
        self._addComposer(layout, 8)
        self._addPublisher(layout, 9)
        self._addIsrc(layout, 10)
        self._addIswc(layout, 11)
        self._addTags(layout, 12)
        self._addLyrics(layout, 13)
        self._addLanguage(layout, 14)
        self._addPreviewTime(layout, 15)

    def _addTrackTitle(self, layout, row):
        self._trackTitleLabel = QLabel()
        layout.addWidget(self._trackTitleLabel, row, 0)
        self._trackTitleEdit = QLineEdit()
        self._trackTitleEdit.setObjectName(ui.TRACK_TITLE_EDIT_NAME)
        self._trackTitleEdit.editingFinished.connect(self._updateTrackTitle)
        layout.addWidget(self._trackTitleEdit, row, 1)
        self._trackTitleLabel.setBuddy(self._trackTitleEdit)

    def _addVersionInfo(self, layout, row):
        self._versionInfoLabel = QLabel()
        layout.addWidget(self._versionInfoLabel, row, 0)
        self._versionInfoEdit = QLineEdit()
        self._versionInfoEdit.setObjectName(ui.VERSION_INFO_EDIT_NAME)
        self._versionInfoEdit.editingFinished.connect(self._updateVersionInfo)
        layout.addWidget(self._versionInfoEdit, row, 1)
        self._versionInfoLabel.setBuddy(self._versionInfoEdit)

    def _addDuration(self, layout, row):
        self._durationLabel = QLabel()
        layout.addWidget(self._durationLabel, row, 0)
        self._durationValueLabel = QLabel()
        self._durationValueLabel.setObjectName(ui.DURATION_NAME)
        layout.addWidget(self._durationValueLabel, row, 1)
        self._durationLabel.setBuddy(self._durationValueLabel)

    def _addTrackNumber(self, layout, row):
        self._trackNumberLabel = QLabel()
        layout.addWidget(self._trackNumberLabel, row, 0)
        self._trackNumberValueLabel = QLabel()
        self._trackNumberValueLabel.setObjectName(ui.TRACK_NUMBER_NAME)
        layout.addWidget(self._trackNumberValueLabel, row, 1)
        self._trackNumberLabel.setBuddy(self._trackNumberValueLabel)

    def _addTotalTracks(self, layout, row):
        self._totalTracksLabel = QLabel()
        layout.addWidget(self._totalTracksLabel, row, 0)
        self._totalTracksValueLabel = QLabel()
        self._totalTracksValueLabel.setObjectName(ui.TOTAL_TRACKS_NAME)
        layout.addWidget(self._totalTracksValueLabel, row, 1)
        self._totalTracksLabel.setBuddy(self._totalTracksValueLabel)

    def _addBitrate(self, layout, row):
        self._bitrateLabel = QLabel()
        layout.addWidget(self._bitrateLabel, row, 0)
        self._bitrateValueLabel = QLabel()
        self._bitrateValueLabel.setObjectName(ui.BITRATE_NAME)
        layout.addWidget(self._bitrateValueLabel, row, 1)
        self._bitrateLabel.setBuddy(self._bitrateValueLabel)

    def _addFeaturedGuest(self, layout, row):
        self._featuredGuestLabel = QLabel()
        layout.addWidget(self._featuredGuestLabel, row, 0)
        self._featuredGuestEdit = QLineEdit()
        self._featuredGuestEdit.setObjectName(ui.FEATURED_GUEST_EDIT_NAME)
        self._featuredGuestEdit.editingFinished.connect(self._updateFeaturedGuest)
        layout.addWidget(self._featuredGuestEdit, row, 1)
        self._featuredGuestLabel.setBuddy(self._featuredGuestEdit)

    def _addLyricist(self, layout, row):
        self._lyricistLabel = QLabel()
        layout.addWidget(self._lyricistLabel, row, 0)
        self._lyricistEdit = QLineEdit()
        self._lyricistEdit.setObjectName(ui.LYRICIST_EDIT_NAME)
        self._lyricistEdit.editingFinished.connect(self._updateLyricist)
        layout.addWidget(self._lyricistEdit, row, 1)
        self._lyricistLabel.setBuddy(self._lyricistEdit)

    def _addComposer(self, layout, row):
        self._composerLabel = QLabel()
        layout.addWidget(self._composerLabel, row, 0)
        self._composerEdit = QLineEdit()
        self._composerEdit.setObjectName(ui.COMPOSER_EDIT_NAME)
        self._composerEdit.editingFinished.connect(self._updateComposer)
        layout.addWidget(self._composerEdit, row, 1)
        self._composerLabel.setBuddy(self._composerEdit)

    def _addPublisher(self, layout, row):
        self._publisherLabel = QLabel()
        layout.addWidget(self._publisherLabel, row, 0)
        self._publisherEdit = QLineEdit()
        self._publisherEdit.setObjectName(ui.PUBLISHER_EDIT_NAME)
        self._publisherEdit.editingFinished.connect(self._updatePublisher)
        layout.addWidget(self._publisherEdit, row, 1)
        self._publisherLabel.setBuddy(self._publisherEdit)

    def _addIsrc(self, layout, row):
        self._isrcLabel = QLabel()
        layout.addWidget(self._isrcLabel, row, 0)
        self._isrcEdit = QLineEdit()
        self._isrcEdit.setObjectName(ui.ISRC_EDIT_NAME)
        self._isrcEdit.editingFinished.connect(self._updateIsrc)
        layout.addWidget(self._isrcEdit, row, 1)
        self._isrcLabel.setBuddy(self._isrcEdit)

    def _addIswc(self, layout, row):
        self._iswcLabel = QLabel()
        layout.addWidget(self._iswcLabel, row, 0)
        self._iswcEdit = QLineEdit()
        self._iswcEdit.setObjectName(ui.ISWC_EDIT_NAME)
        self._iswcEdit.setDisabled(True)
        layout.addWidget(self._iswcEdit, row, 1)
        self._iswcLabel.setBuddy(self._iswcEdit)

    def _addTags(self, layout, row):
        self._tagsLabel = QLabel()
        layout.addWidget(self._tagsLabel, row, 0)
        self._tagsEdit = QLineEdit()
        self._tagsEdit.setObjectName(ui.TAGS_EDIT_NAME)
        self._tagsEdit.editingFinished.connect(self._updateTags)
        layout.addWidget(self._tagsEdit, row, 1)
        self._tagsLabel.setBuddy(self._tagsEdit)

    def _addLyrics(self, layout, row):
        self._lyricsLabel = QLabel()
        layout.addWidget(self._lyricsLabel, row, 0)
        self._lyricsEdit = TextArea()
        self._lyricsEdit.setObjectName(ui.LYRICS_EDIT_NAME)
        self._lyricsEdit.editingFinished.connect(self._updateLyrics)
        layout.addWidget(self._lyricsEdit, row, 1)
        self._lyricsLabel.setBuddy(self._lyricsEdit)

    def _addLanguage(self, layout, row):
        self._languageLabel = QLabel()
        layout.addWidget(self._languageLabel, row, 0)
        self._languageEdit = QLineEdit()
        self._languageEdit.setObjectName(ui.LANGUAGE_EDIT_NAME)
        self._languageEdit.editingFinished.connect(self._updateLanguage)
        layout.addWidget(self._languageEdit, row, 1)
        self._languageLabel.setBuddy(self._languageEdit)

    def _addPreviewTime(self, layout, row):
        self._previewTimeLabel = QLabel()
        layout.addWidget(self._previewTimeLabel, row, 0)
        self._previewTimeEdit = QTimeEdit()
        self._previewTimeEdit.setDisplayFormat(DURATION_FORMAT)
        # self._previewTimeEdit.setTime(QTime.fromString('00:00'))
        self._previewTimeEdit.setObjectName(ui.PREVIEW_TIME_EDIT_NAME)
        self._previewTimeEdit.setDisabled(True)
        layout.addWidget(self._previewTimeEdit, row, 1)
        self._previewTimeLabel.setBuddy(self._previewTimeEdit)

    def translateUi(self):
        self._trackTitleLabel.setText(self.tr('Track Title: '))
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
        self._iswcLabel.setText(self.tr('ISWC: '))
        self._tagsLabel.setText(self.tr('Tags: '))
        self._lyricsLabel.setText(self.tr('Lyrics: '))
        self._languageLabel.setText(self.tr('Language: '))
        self._previewTimeLabel.setText(self.tr('Preview Time: '))

    def trackAdded(self, track, position):
        self.trackStateChanged(self._track)

    def trackRemoved(self, track, position):
        if track == self._track:
            self._album.removeAlbumListener(self)
        else:
            self.trackStateChanged(self._track)

    def trackStateChanged(self, track):
        if not track in self._album.tracks:
            return

        self._trackTitleEdit.setText(track.trackTitle)
        self._versionInfoEdit.setText(track.versionInfo)
        self._durationValueLabel.setText(display.asDuration(track.duration))
        self._trackNumberValueLabel.setText(str(self._album.indexOf(track) + 1))
        self._totalTracksValueLabel.setText(str(self._album.totalTracks()))
        self._bitrateValueLabel.setText('%s kbps' % display.inKbps(track.bitrate))
        self._featuredGuestEdit.setText(track.featuredGuest)
        self._lyricistEdit.setText(track.lyricist)
        self._composerEdit.setText(track.composer)
        self._publisherEdit.setText(track.publisher)
        self._isrcEdit.setText(track.isrc)
        self._tagsEdit.setText(track.tags)
        self._lyricsEdit.setPlainText(track.lyrics)
        self._languageEdit.setText(track.language)

    def _updateTrackTitle(self):
        self._track.trackTitle = self._trackTitleEdit.text()

    def _updateVersionInfo(self):
        self._track.versionInfo = self._versionInfoEdit.text()

    def _updateFeaturedGuest(self):
        self._track.featuredGuest = self._featuredGuestEdit.text()

    def _updateLyricist(self):
        self._track.lyricist = self._lyricistEdit.text()

    def _updateComposer(self):
        self._track.composer = self._composerEdit.text()

    def _updatePublisher(self):
        self._track.publisher = self._publisherEdit.text()

    def _updateIsrc(self):
        self._track.isrc = self._isrcEdit.text()

    def _updateTags(self):
        self._track.tags = self._tagsEdit.text()

    def _updateLyrics(self):
        self._track.lyrics = self._lyricsEdit.toPlainText()

    def _updateLanguage(self):
        self._track.language = self._languageEdit.text()
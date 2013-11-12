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

from PyQt4.QtGui import (QWidget, QGridLayout, QVBoxLayout, QLabel, QLineEdit)

from tgit.ui import constants as ui, display
from tgit.ui.text_area import TextArea


class TrackPage(QWidget):
    def __init__(self, track, parent=None):
        QWidget.__init__(self, parent)
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
        self._addBitrate(layout, 2)
        self._addDuration(layout, 3)
        self._addFeaturedGuest(layout, 4)
        self._addLyricist(layout, 5)
        self._addComposer(layout, 6)
        self._addPublisher(layout, 7)
        self._addIsrc(layout, 8)
        self._addTags(layout, 9)
        self._addLyrics(layout, 10)
        self._addLanguage(layout, 11)

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

    def _addBitrate(self, layout, row):
        self._bitrateLabel = QLabel()
        layout.addWidget(self._bitrateLabel, row, 0)
        self._bitrateInfoLabel = QLabel()
        self._bitrateInfoLabel.setObjectName(ui.BITRATE_NAME)
        layout.addWidget(self._bitrateInfoLabel, row, 1)
        self._bitrateLabel.setBuddy(self._bitrateInfoLabel)

    def _addDuration(self, layout, row):
        self._durationLabel = QLabel()
        layout.addWidget(self._durationLabel, row, 0)
        self._durationInfoLabel = QLabel()
        self._durationInfoLabel.setObjectName(ui.DURATION_NAME)
        layout.addWidget(self._durationInfoLabel, row, 1)
        self._durationLabel.setBuddy(self._durationInfoLabel)

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

    def translateUi(self):
        self._trackTitleLabel.setText(self.tr('Track Title: '))
        self._versionInfoLabel.setText(self.tr('Version Information: '))
        self._bitrateLabel.setText(self.tr('Bitrate: '))
        self._durationLabel.setText(self.tr('Duration: '))
        self._featuredGuestLabel.setText(self.tr('Featured Guest: '))
        self._lyricistLabel.setText(self.tr('Lyricist: '))
        self._composerLabel.setText(self.tr('Composer: '))
        self._publisherLabel.setText(self.tr('Publisher: '))
        self._isrcLabel.setText(self.tr('ISRC: '))
        self._tagsLabel.setText(self.tr('Tags: '))
        self._lyricsLabel.setText(self.tr('Lyrics: '))
        self._languageLabel.setText(self.tr('Language: '))

    def trackStateChanged(self, track):
        self._trackTitleEdit.setText(track.trackTitle)
        self._versionInfoEdit.setText(track.versionInfo)
        self._bitrateInfoLabel.setText('%s kbps' % display.inKbps(track.bitrate))
        self._durationInfoLabel.setText(display.asDuration(track.duration))
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
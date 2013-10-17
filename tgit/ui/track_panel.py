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

from tgit.ui import display

# todo consider moving all ui constants to the same module (ui?)
TRACK_PANEL_NAME = 'Track Panel'
TRACK_TITLE_NAME = 'Track Title'
VERSION_INFO_NAME = "Version Info"
FEATURED_GUEST_NAME = "Featured Guest"
ISRC_NAME = "ISRC"
BITRATE_NAME = "Bitrate"
DURATION_NAME = "Duration"


class TrackPanel(QWidget):
    # todo pass track to constructor
    def __init__(self, track, parent=None):
        QWidget.__init__(self, parent)
        self.setObjectName(TRACK_PANEL_NAME)
        grid = QGridLayout()
        self._fill(grid)
        self.translateUi()
        self._layout(grid)
        self._track = track
        self.trackStateChanged(track)

    def _layout(self, grid):
        layout = QVBoxLayout()
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)

    def _fill(self, layout):
        self._addTrackTitle(layout, 0)
        self._addVersionInfo(layout, 1)
        self._addFeaturedGuest(layout, 2)
        self._addIsrc(layout, 3)
        self._addBitrate(layout, 4)
        self._addDuration(layout, 5)

    def _addTrackTitle(self, layout, row):
        self._trackTitleLabel = QLabel()
        layout.addWidget(self._trackTitleLabel, row, 0)
        self._trackTitleEdit = QLineEdit()
        self._trackTitleEdit.setObjectName(TRACK_TITLE_NAME)
        layout.addWidget(self._trackTitleEdit, row, 1)
        self._trackTitleLabel.setBuddy(self._trackTitleEdit)

    def _addVersionInfo(self, layout, row):
        self._versionInfoLabel = QLabel()
        layout.addWidget(self._versionInfoLabel, row, 0)
        self._versionInfoEdit = QLineEdit()
        self._versionInfoEdit.setObjectName(VERSION_INFO_NAME)
        layout.addWidget(self._versionInfoEdit, row, 1)
        self._versionInfoLabel.setBuddy(self._versionInfoEdit)

    def _addFeaturedGuest(self, layout, row):
        self._featuredGuestLabel = QLabel()
        layout.addWidget(self._featuredGuestLabel, row, 0)
        self._featuredGuestEdit = QLineEdit()
        self._featuredGuestEdit.setObjectName(FEATURED_GUEST_NAME)
        layout.addWidget(self._featuredGuestEdit, row, 1)
        self._featuredGuestLabel.setBuddy(self._featuredGuestEdit)

    def _addIsrc(self, layout, row):
        self._isrcLabel = QLabel()
        layout.addWidget(self._isrcLabel, row, 0)
        self._isrcEdit = QLineEdit()
        self._isrcEdit.setObjectName(ISRC_NAME)
        layout.addWidget(self._isrcEdit, row, 1)
        self._isrcLabel.setBuddy(self._isrcEdit)

    def _addBitrate(self, layout, row):
        self._bitrateLabel = QLabel()
        layout.addWidget(self._bitrateLabel, row, 0)
        self._bitrateInfoLabel = QLabel()
        self._bitrateInfoLabel.setObjectName(BITRATE_NAME)
        layout.addWidget(self._bitrateInfoLabel, row, 1)
        self._bitrateLabel.setBuddy(self._bitrateInfoLabel)

    def _addDuration(self, layout, row):
        self._durationLabel = QLabel()
        layout.addWidget(self._durationLabel, row, 0)
        self._durationInfoLabel = QLabel()
        self._durationInfoLabel.setObjectName(DURATION_NAME)
        layout.addWidget(self._durationInfoLabel, row, 1)
        self._durationLabel.setBuddy(self._durationInfoLabel)

    def translateUi(self):
        self._trackTitleLabel.setText(self.tr("Track Title: "))
        self._versionInfoLabel.setText(self.tr("Version Information: "))
        self._featuredGuestLabel.setText(self.tr("Featured Guest: "))
        self._isrcLabel.setText(self.tr("ISRC: "))
        self._bitrateLabel.setText(self.tr("Bitrate: "))
        self._durationLabel.setText(self.tr("Duration: "))

    def trackStateChanged(self, track):
        self._trackTitleEdit.setText(track.trackTitle)
        self._versionInfoEdit.setText(track.versionInfo)
        self._featuredGuestEdit.setText(track.featuredGuest)
        self._isrcEdit.setText(track.isrc)
        self._bitrateInfoLabel.setText("%s kbps" % display.inKbps(track.bitrate))
        self._durationInfoLabel.setText(display.asDuration(track.duration))

    def updateTrack(self):
        self._track.trackTitle = self._trackTitleEdit.text()
        self._track.versionInfo = self._versionInfoEdit.text()
        self._track.featuredGuest = self._featuredGuestEdit.text()
        self._track.isrc = self._isrcEdit.text()

    def displays(self, track):
        return self._track == track
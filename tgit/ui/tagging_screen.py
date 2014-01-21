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
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QLabel

from tgit.announcer import Announcer
from tgit.album import AlbumListener
from tgit.mp3.id3_tagger import Id3Tagger
from tgit.mp3.track_files import TrackFiles
from tgit.ui.album_mixer import AlbumMixer
from tgit.ui import constants as ui, style
from tgit.ui.album_editor import AlbumEditor
from tgit.ui.track_editor import TrackEditor
from tgit.ui.track_list_page import TrackListPage


TRACK_LIST_PAGE = 0
ALBUM_PAGE = 1
TRACK_PAGE = 2

HELP_URL = 'http://tagtamusique.com/2013/12/03/tgit_style_guide/'


class TaggingScreen(QWidget, AlbumListener):
    def __init__(self, album, player):
        QWidget.__init__(self)
        self._album = album
        self._album.addAlbumListener(self)
        self._player = player
        self._requestListeners = Announcer()

        self._assemble()
        self.localize()

    def addRequestListener(self, listener):
        self._requestListeners.addListener(listener)

    # Eventually, event will bubble up to top level presenter.
    # For that we need to do some prep work on the menubar first.
    def selectFiles(self, folders=False):
        mixer = AlbumMixer(self._album, TrackFiles(Id3Tagger()))
        mixer.show(folders=folders)

    def recordAlbum(self):
        self._requestListeners.recordAlbum(self._album)

    def _assemble(self):
        self.setObjectName(ui.TAGGING_SCREEN_NAME)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addWidget(self._makeNavigationBar())
        layout.addWidget(self._makePages())
        layout.addWidget(self._makeButtonBar())

    def _makeNavigationBar(self):
        self._navigationBar = QWidget()
        self._navigationBar.setObjectName(ui.NAVIGATION_BAR)
        helpLink = self._makeHelpLink()
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 10, 25, 10)
        layout.addStretch()
        layout.addWidget(helpLink)

        self._navigationBar.setLayout(layout)
        return self._navigationBar

    def _makeHelpLink(self):
        label = QLabel()
        label.setText('<a style="color: white" href="%s">%s</a>' % (HELP_URL, self.tr('Help')))
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        return label

    def _makePages(self):
        self._pages = QStackedWidget()
        page = TrackListPage(self._album, self._player)
        page.addRequestListener(self)
        self._pages.addWidget(page)
        albumPage = QWidget()
        editor = AlbumEditor(self._album)
        editor.show(albumPage)
        self._pages.addWidget(albumPage)
        self._pages.setCurrentIndex(TRACK_LIST_PAGE)
        return self._pages

    def _makeButtonBar(self):
        self._buttonBar = QWidget()
        self._buttonBar.setObjectName(ui.BUTTON_BAR)
        layout = style.horizontalLayout()
        self._buttonBar.setLayout(layout)
        self._previousPageButton = QPushButton()
        self._previousPageButton.setObjectName(ui.PREVIOUS_BUTTON_NAME)
        self._previousPageButton.clicked.connect(self._showPreviousPage)
        style.disableButton(self._previousPageButton)
        layout.addWidget(self._previousPageButton)
        layout.addStretch()
        self._saveButton = QPushButton()
        self._saveButton.setObjectName(ui.SAVE_BUTTON_NAME)
        self._saveButton.setFocusPolicy(Qt.StrongFocus)
        self._saveButton.clicked.connect(self.recordAlbum)
        style.disableButton(self._saveButton)
        layout.addWidget(self._saveButton)
        layout.addStretch()
        self._nextStepButton = QPushButton()
        self._nextStepButton.setObjectName(ui.NEXT_BUTTON_NAME)
        self._nextStepButton.clicked.connect(self._showNextPage)
        style.disableButton(self._nextStepButton)
        layout.addWidget(self._nextStepButton)

        return self._buttonBar

    def trackAdded(self, track, position):
        self._addTrackPage(track, position)
        style.enableButton(self._nextStepButton)

    def trackRemoved(self, track, position):
        self._removeTrackPage(track, position)
        if self._album.empty():
            style.disableButton(self._nextStepButton)

    def _addTrackPage(self, track, position):
        trackPage = QWidget()
        editor = TrackEditor(self._album, track)
        editor.render(trackPage)
        self._pages.insertWidget(TRACK_PAGE + position, trackPage)

    def _removeTrackPage(self, track, position):
        self._pages.removeWidget(self._trackPage(position))

    def _currentPage(self):
        return self._pages.currentIndex()

    def _onPage(self, index):
        return self._currentPage() == index

    def _previousPage(self):
        return self._currentPage() - 1

    def _nextPage(self):
        return self._currentPage() + 1

    def _lastPage(self):
        return self._pages.count() - 1

    def showTrackList(self):
        self._showPage(TRACK_LIST_PAGE)

    def _showPage(self, page):
        self._pages.setCurrentIndex(page)

    def _showPreviousPage(self):
        self._showPage(self._previousPage())
        if self._onPage(TRACK_LIST_PAGE):
            style.disableButton(self._previousPageButton)
            style.disableButton(self._saveButton)
        style.enableButton(self._nextStepButton)

    def _showNextPage(self):
        self._showPage(self._nextPage())
        style.enableButton(self._previousPageButton)
        style.enableButton(self._saveButton)
        if self._onPage(self._lastPage()):
            style.disableButton(self._nextStepButton)

    def _trackListPage(self):
        return self._pages.widget(TRACK_LIST_PAGE)

    def _albumPage(self):
        return self._pages.widget(ALBUM_PAGE)

    def _trackPage(self, position):
        return self._pages.widget(TRACK_PAGE + position)

    def localize(self):
        self._previousPageButton.setText(self.tr('PREVIOUS'))
        self._saveButton.setText(self.tr('SAVE'))
        self._nextStepButton.setText(self.tr('NEXT'))
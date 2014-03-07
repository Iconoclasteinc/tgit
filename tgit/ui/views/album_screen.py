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
from PyQt4.QtGui import QWidget, QLabel, QStackedWidget, QPushButton
from tgit.announcer import Announcer
from tgit.ui import style


def albumScreen(listener):
    screen = AlbumScreen()
    screen.announceTo(listener)
    return screen


class AlbumScreen(object):
    NAME = 'album-screen'

    NAVIGATION_BAR_NAME = 'navigation'
    CONTROL_BAR_NAME = 'controls'
    PREVIOUS_PAGE_BUTTON_NAME = 'previous'
    NEXT_PAGE_BUTTON_NAME = 'next'
    SAVE_BUTTON_NAME = 'save'
    HELP_LINK_NAME = 'help-link'

    HELP_URL = 'http://tagtamusique.com/2013/12/03/tgit_style_guide/'
    COMPOSITION_PAGE, ALBUM_PAGE, TRACK_PAGES = range(0, 3)

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
        widget.setObjectName(self.NAME)
        layout = style.verticalLayout()
        layout.addWidget(self._makeNavigationBar())
        layout.addWidget(self._makePages())
        layout.addWidget(self._makeControls())
        widget.setLayout(layout)
        return widget

    def _makeNavigationBar(self):
        self._navigationBar = QWidget()
        self._navigationBar.setObjectName(self.NAVIGATION_BAR_NAME)
        self._helpLink = self._makeHelpLink()
        layout = style.horizontalLayout()
        layout.setContentsMargins(25, 10, 25, 10)
        layout.addStretch()
        layout.addWidget(self._helpLink)

        self._navigationBar.setLayout(layout)
        return self._navigationBar

    def _makeHelpLink(self):
        label = QLabel()
        label.setObjectName(self.HELP_LINK_NAME)
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        return label

    def _makePages(self):
        self._pages = QStackedWidget()
        self._pages.currentChanged.connect(self._updateNavigationControls)
        return self._pages

    def _makeControls(self):
        self._controls = QWidget()
        self._controls.setObjectName(self.CONTROL_BAR_NAME)
        layout = style.horizontalLayout()
        self._controls.setLayout(layout)
        self._previousButton = QPushButton()
        self._previousButton.setObjectName(self.PREVIOUS_PAGE_BUTTON_NAME)
        self._previousButton.clicked.connect(self.toPreviousPage)
        style.disableButton(self._previousButton)
        layout.addWidget(self._previousButton)
        layout.addStretch()
        self._saveButton = QPushButton()
        self._saveButton.setObjectName(self.SAVE_BUTTON_NAME)
        self._saveButton.setFocusPolicy(Qt.StrongFocus)
        self._saveButton.clicked.connect(lambda pressed: self._announce.recordAlbum())
        style.disableButton(self._saveButton)
        layout.addWidget(self._saveButton)
        layout.addStretch()
        self._nextButton = QPushButton()
        self._nextButton.setObjectName(self.NEXT_PAGE_BUTTON_NAME)
        self._nextButton.clicked.connect(self.toNextPage)
        style.disableButton(self._nextButton)
        layout.addWidget(self._nextButton)

        return self._controls

    def _updateNavigationControls(self):
        if self._onLastPage():
            style.disableButton(self._nextButton)
        else:
            style.enableButton(self._nextButton)

        if self._onFirstPage():
            style.disableButton(self._previousButton)
        else:
            style.enableButton(self._previousButton)

    def _onLastPage(self):
        return self._onPage(self.pageCount - 1)

    def _onFirstPage(self):
        return self._onPage(0)

    def _onPage(self, number):
        return self.pageNumber == number

    def allowSaves(self, allowed=True):
        if allowed:
            style.enableButton(self._saveButton)
        else:
            style.disableButton(self._saveButton)

    def setAlbumCompositionPage(self, page):
        self.insertPage(page, self.COMPOSITION_PAGE)

    def setAlbumEditionPage(self, page):
        self.insertPage(page, self.ALBUM_PAGE)

    def addTrackEditionPage(self, page, position):
        self.insertPage(page, self.TRACK_PAGES + position)

    def removeTrackEditionPage(self, position):
        self.removePage(self.TRACK_PAGES + position)

    def appendPage(self, widget):
        self._pages.addWidget(widget)
        self._updateNavigationControls()

    def insertPage(self, widget, position):
        self._pages.insertWidget(position, widget)
        self._updateNavigationControls()

    def removePage(self, number):
        self._pages.removeWidget(self._pages.widget(number))
        self._updateNavigationControls()

    @property
    def pageNumber(self):
        return self._pages.currentIndex()

    @property
    def pageCount(self):
        return self._pages.count()

    def toPage(self, number):
        self._pages.setCurrentIndex(number)

    def toPreviousPage(self):
        self.toPage(self.pageNumber - 1)

    def toNextPage(self):
        self.toPage(self.pageNumber + 1)

    def _atPage(self, number):
        return self._pages.currentIndex() == number

    def translate(self):
        self._previousButton.setText(self.tr('PREVIOUS'))
        self._saveButton.setText(self.tr('SAVE'))
        self._nextButton.setText(self.tr('NEXT'))
        self._helpLink.setText('<a style="color: white" href="%s">%s</a>' % (self.HELP_URL, self.tr('Help')))

    def tr(self, text):
        return self._widget.tr(text)

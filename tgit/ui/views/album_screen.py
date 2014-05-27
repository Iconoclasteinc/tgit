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
from tgit.ui.widgets import form


def albumScreen(listener):
    screen = AlbumScreen()
    screen.announceTo(listener)
    return screen


class AlbumScreen(QWidget):
    HELP_URL = 'http://tagtamusique.com/2013/12/03/tgit_style_guide/'
    FEATURE_REQUEST_URL = "mailto:iconoclastejr@gmail.com?subject=[TGiT] J'en veux plus !"

    COMPOSITION_PAGE, ALBUM_PAGE, TRACK_PAGES = range(0, 3)

    def __init__(self):
        QWidget.__init__(self)
        self.setObjectName('album-screen')
        self.render()

    def bind(self, **handlers):
        if 'recordAlbum' in handlers:
            self.save.clicked.connect(lambda pressed: handlers['recordAlbum']())

    def render(self):
        layout = form.column()
        layout.addWidget(self.makeNavigationBar())
        layout.addWidget(self.makePages())
        layout.addWidget(self.makeControls())
        self.setLayout(layout)

    def makeNavigationBar(self):
        navigation = QWidget()
        navigation.setObjectName('navigation')
        layout = form.row()
        layout.setContentsMargins(25, 10, 25, 10)
        layout.addStretch()
        layout.addWidget(self.makeFeatureRequestLink())
        layout.addWidget(self.makeHelpLink())
        navigation.setLayout(layout)
        return navigation

    def makeHelpLink(self):
        label = QLabel()
        label.setObjectName('help-link')
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        label.setText('<a style="color: white" href="%s">%s</a>' % (self.HELP_URL, self.tr('Help')))
        return label

    def makeFeatureRequestLink(self):
        label = QLabel()
        label.setObjectName('feature-request-link')
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        label.setText('<a style="color: white" href="%s">%s</a>' % (self.FEATURE_REQUEST_URL, self.tr('Request Feature')))
        return label

    def makePages(self):
        self.pages = QStackedWidget()
        self.pages.currentChanged.connect(self.updateNavigationControls)
        return self.pages

    def makeControls(self):
        controls = QWidget()
        controls.setObjectName('controls')
        layout = form.row()
        self.previous = QPushButton()
        self.previous.setObjectName('previous')
        self.previous.setText(self.tr('PREVIOUS'))
        self.previous.clicked.connect(self.toPreviousPage)
        form.disableButton(self.previous)
        layout.addWidget(self.previous)
        layout.addStretch()
        self.save = QPushButton()
        self.save.setObjectName('save')
        self.save.setText(self.tr('SAVE'))
        self.save.setFocusPolicy(Qt.StrongFocus)
        form.disableButton(self.save)
        layout.addWidget(self.save)
        layout.addStretch()
        self.next = QPushButton()
        self.next.setObjectName('next')
        self.next.setText(self.tr('NEXT'))
        self.next.clicked.connect(self.toNextPage)
        form.disableButton(self.next)
        layout.addWidget(self.next)

        controls.setLayout(layout)
        return controls

    def updateNavigationControls(self):
        if self.onLastPage():
            form.disableButton(self.next)
        else:
            form.enableButton(self.next)

        if self.onFirstPage():
            form.disableButton(self.previous)
        else:
            form.enableButton(self.previous)

    def onLastPage(self):
        return self.onPage(self.pageCount - 1)

    def onFirstPage(self):
        return self.onPage(0)

    def onPage(self, number):
        return self.pageNumber == number

    def allowSaves(self, allowed=True):
        if allowed:
            form.enableButton(self.save)
        else:
            form.disableButton(self.save)

    def setAlbumCompositionPage(self, page):
        self.insertPage(page, self.COMPOSITION_PAGE)

    def setAlbumEditionPage(self, page):
        self.insertPage(page, self.ALBUM_PAGE)

    def addTrackEditionPage(self, page, position):
        self.insertPage(page, self.TRACK_PAGES + position)

    def removeTrackEditionPage(self, position):
        self.removePage(self.TRACK_PAGES + position)

    def appendPage(self, widget):
        self.pages.addWidget(widget)
        self.updateNavigationControls()

    def insertPage(self, widget, position):
        self.pages.insertWidget(position, widget)
        self.updateNavigationControls()

    def removePage(self, number):
        self.pages.removeWidget(self.pages.widget(number))
        self.updateNavigationControls()

    @property
    def pageNumber(self):
        return self.pages.currentIndex()

    @property
    def pageCount(self):
        return self.pages.count()

    def toPage(self, number):
        self.pages.setCurrentIndex(number)

    def toPreviousPage(self):
        self.toPage(self.pageNumber - 1)

    def toNextPage(self):
        self.toPage(self.pageNumber + 1)

    def atPage(self, number):
        return self.pages.currentIndex() == number
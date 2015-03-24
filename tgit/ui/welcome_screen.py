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

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel


def centerHorizontally(widget):
    container = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    container.setLayout(layout)
    layout.addStretch()
    layout.addWidget(widget)
    layout.addStretch()
    return container


# We have to inherit from QFrame and not QWidget if we want a background without reimplementing QWidget.paintEvent
class WelcomeScreen(QFrame):
    newAlbum = pyqtSignal()

    def __init__(self):
        QFrame.__init__(self)
        self.build()

    def build(self):
        self.setObjectName('welcome-screen')
        layout = QGridLayout()
        layout.addWidget(self.makeWelcomeDialog(), 0, 0)
        self.setLayout(layout)

    # todo use form? (needs rename?)
    def makeWelcomeDialog(self):
        welcome = QWidget()
        welcome.setObjectName('welcome-dialog')
        layout = QVBoxLayout()
        layout.addWidget(self.makeTitle())
        layout.addWidget(self.makeMsg())
        layout.addWidget(self.makeDescription())
        layout.addWidget(self.makeButtonBar())
        welcome.setLayout(layout)
        return welcome

    def makeTitle(self):
        title = QLabel()
        title.setProperty('title', 'h1')
        title.setText(self.tr('Welcome to TGiT!'))
        return centerHorizontally(title)

    def makeMsg(self):
        msg = QLabel()
        msg.setText(self.tr('Your album is empty right now.'))
        return centerHorizontally(msg)

    def makeDescription(self):
        help = QLabel()
        help.setText(self.tr('Click on the button below to add some tracks.'))
        return centerHorizontally(help)

    def makeButtonBar(self):
        buttons = QWidget()
        layout = QHBoxLayout()
        buttons.setLayout(layout)
        layout.setContentsMargins(0, 40, 0, 30)
        layout.addStretch()
        layout.addWidget(self.makeNewAlbumButton())
        layout.addStretch()
        return buttons

    def makeNewAlbumButton(self):
        button = QPushButton()
        button.setObjectName('new-album')
        button.setText(self.tr('ADD FILES...'))
        button.clicked.connect(lambda: self.newAlbum.emit())
        button.setCursor(Qt.PointingHandCursor)
        return button
# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QPushButton, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel)

from tgit.ui.helpers import display


# We have to inherit from QFrame and not QWidget if we want a background without reimplementing QWidget.paintEvent
class WelcomeScreen(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setObjectName('welcome-screen')
        self.render()

    def render(self):
        layout = QGridLayout()
        layout.addWidget(self.makeWelcomeDialog(), 0, 0)
        self.setLayout(layout)

    def bind(self, **handlers):
        if 'newAlbum' in handlers:
            self.newAlbum.clicked.connect(lambda: handlers['newAlbum']())

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
        return display.centeredHorizontally(title)

    def makeMsg(self):
        msg = QLabel()
        msg.setText(self.tr('Your album is empty right now.'))
        return display.centeredHorizontally(msg)

    def makeDescription(self):
        help = QLabel()
        help.setText(self.tr('Click on the button below to add some tracks.'))
        return display.centeredHorizontally(help)

    def makeButtonBar(self):
        buttons = QWidget()
        layout = QHBoxLayout()
        buttons.setLayout(layout)
        layout.setContentsMargins(0, 40, 0, 30)
        layout.addStretch()
        self.newAlbum = QPushButton()
        self.newAlbum.setObjectName('new-album')
        self.newAlbum.setText(self.tr('ADD FILES...'))
        self.newAlbum.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.newAlbum)
        layout.addStretch()
        return buttons
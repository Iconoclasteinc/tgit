# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import (QWidget, QPushButton, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel)

from tgit4.ui.helpers import display


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
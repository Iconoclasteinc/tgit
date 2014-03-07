# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QPushButton, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout,
                         QLabel)

from tgit.announcer import Announcer
from tgit.ui import display


# We have to inherit from QFrame and not QWidget if we want a background without
# reimplementing paintEvent()
class WelcomeScreen():

    NAME = "welcome-screen"
    WELCOME_DIALOG_NAME = 'welcome-dialog'
    NEW_ALBUM_BUTTON_NAME = 'new-album'

    TITLE_TYPE = 'title'
    H1 = 'h1'

    def __init__(self):
        self._announce = Announcer()

    def announceTo(self, listener):
        self._announce.addListener(listener)

    def render(self):
        self._widget = self._build()
        self.translate()
        return self._widget

    def _build(self):
        frame = QFrame()
        frame.setObjectName(self.NAME)
        layout = QGridLayout()
        frame.setLayout(layout)
        layout.addWidget(self._makeWelcomeDialog(), 0, 0)
        return frame

    def _makeWelcomeDialog(self):
        welcomeDialog = QWidget()
        welcomeDialog.setObjectName(self.WELCOME_DIALOG_NAME)
        layout = QVBoxLayout()
        welcomeDialog.setLayout(layout)
        self._addTitle(layout)
        self._addText(layout)
        self._addButtons(layout)
        return welcomeDialog

    def _addTitle(self, layout):
        self._dialogTitle = QLabel()
        self._dialogTitle.setProperty(self.TITLE_TYPE, self.H1)
        layout.addWidget(display.centeredHorizontally(self._dialogTitle))

    def _addText(self, layout):
        self._msg = QLabel()
        layout.addWidget(display.centeredHorizontally(self._msg))
        self._help = QLabel()
        layout.addWidget(display.centeredHorizontally(self._help))

    def _addButtons(self, layout):
        layout.addWidget(self._makeButtonBar())

    def _makeButtonBar(self):
        buttons = QWidget()
        layout = QHBoxLayout()
        buttons.setLayout(layout)
        layout.setContentsMargins(0, 40, 0, 30)
        layout.addStretch()
        self._newAlbumButton = QPushButton()
        self._newAlbumButton.setObjectName(self.NEW_ALBUM_BUTTON_NAME)
        self._newAlbumButton.setCursor(Qt.PointingHandCursor)
        self._newAlbumButton.clicked.connect(lambda: self._announce.newAlbum())
        layout.addWidget(self._newAlbumButton)
        layout.addStretch()
        return buttons

    def translate(self):
        self._dialogTitle.setText(self.tr('Welcome to TGiT!'))
        self._msg.setText(self.tr('Your album is empty right now.'))
        self._help.setText(self.tr('Click on the button below to add some tracks.'))
        self._newAlbumButton.setText(self.tr('ADD FILES...'))

    def tr(self, text):
        return self._widget.tr(text)

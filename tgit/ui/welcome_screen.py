# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton

from tgit.announcer import Announcer
from tgit.ui import constants as ui


class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.requestListeners = Announcer()

        self._build()
        self.localize()

    def addRequestListener(self, listener):
        self.requestListeners.addListener(listener)

    def _build(self):
        self.setObjectName(ui.WELCOME_SCREEN_NAME)
        layout = QHBoxLayout()
        layout.addStretch()
        self._newAlbumButton = QPushButton()
        self._newAlbumButton.setObjectName(ui.NEW_ALBUM_BUTTON_NAME)
        self._newAlbumButton.clicked.connect(self.newAlbum)
        layout.addWidget(self._newAlbumButton)
        layout.addStretch()
        self.setLayout(layout)

    def newAlbum(self):
        self.requestListeners.newAlbum()

    def localize(self):
        self._newAlbumButton.setText(self.tr('New Album...'))

# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QHBoxLayout, QPushButton

from tgit.announcer import Announcer

NEW_ALBUM_BUTTON_NAME = "New Album Button"


class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.requestListeners = Announcer()
        self._build()
        self.localize()

    def addRequestListener(self, listener):
        self.requestListeners.add(listener)

    def _build(self):
        layout = QHBoxLayout()
        layout.addStretch()
        self._newAlbumButton = QPushButton()
        self._newAlbumButton.setObjectName(NEW_ALBUM_BUTTON_NAME)
        self._newAlbumButton.clicked.connect(self.newAlbum)
        layout.addWidget(self._newAlbumButton)
        layout.addStretch()
        self.setLayout(layout)

    def newAlbum(self):
        self.requestListeners.announce().newAlbum()

    def localize(self):
        self._newAlbumButton.setText(self.tr("New Album..."))

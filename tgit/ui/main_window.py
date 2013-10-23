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

from PyQt4.QtGui import QMainWindow, QMenu, QAction, QStatusBar

from tgit.announcer import Announcer
from tgit.producer import ProductionListener

from tgit.ui import constants as ui
from tgit.ui.welcome_screen import WelcomeScreen
from tgit.ui.tagging_screen import TaggingScreen


class MainWindow(QMainWindow, ProductionListener):
    def __init__(self, productionPortfolio, player, audioFileChooser, imageFileChooser):
        QMainWindow.__init__(self)

        self._productionPortfolio = productionPortfolio
        self._productionPortfolio.addProductionListener(self)
        self._player = player
        self._audioFileChooser = audioFileChooser
        self._imageFileChooser = imageFileChooser
        self._productionHouses = Announcer()

        self._build()
        self.show()

    def addProductionHouse(self, house):
        self._productionHouses.addListener(house)

    def productionAdded(self, director, album):
        mainScreen = TaggingScreen(album, self._player, self._audioFileChooser,
                                   self._imageFileChooser, self)
        mainScreen.addRequestListener(director)
        self.setCentralWidget(mainScreen)
        self._importAction.setEnabled(True)
        mainScreen.selectTrack()

    def _build(self):
        self.setObjectName(ui.MAIN_WINDOW_NAME)
        self.resize(*ui.MAIN_WINDOW_SIZE)
        self._fillMenu()
        self._makeStatusBar()
        self.setCentralWidget(self._makeWelcomeScreen())
        self.localize()

    def _fillMenu(self):
        menuBar = self.menuBar()
        self._fileMenu = QMenu(menuBar)
        self._fileMenu.setObjectName(ui.FILE_MENU_NAME)
        self._importAction = QAction(self._fileMenu)
        self._importAction.setObjectName(ui.IMPORT_TRACK_ACTION_NAME)
        self._importAction.triggered.connect(lambda: self.centralWidget().selectTrack())
        self._importAction.setDisabled(True)
        self._fileMenu.addAction(self._importAction)
        menuBar.addMenu(self._fileMenu)

    def _makeStatusBar(self):
        self.setStatusBar(QStatusBar())

    def _makeWelcomeScreen(self):
        welcomeScreen = WelcomeScreen(self)
        welcomeScreen.addRequestListener(self._productionHouses)
        return welcomeScreen

    def localize(self):
        self.setWindowTitle(self.tr('TGiT'))
        self._fileMenu.setTitle(self.tr('File'))
        self._importAction.setText(self.tr('Import File...'))
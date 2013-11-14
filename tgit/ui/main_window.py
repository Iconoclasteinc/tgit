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
from tgit.record_label import AlbumPortfolioListener
from tgit.ui import constants as ui
from tgit.ui.welcome_screen import WelcomeScreen
from tgit.ui.tagging_screen import TaggingScreen


class MainWindow(QMainWindow, AlbumPortfolioListener):
    def __init__(self, albumPortfolio, audioPlayer, audioFileChooser, imageFileChooser):
        QMainWindow.__init__(self)

        self._albumPortfolio = albumPortfolio
        self._albumPortfolio.addPortfolioListener(self)
        self._audioPlayer = audioPlayer
        self._audioFileChooser = audioFileChooser
        self._imageFileChooser = imageFileChooser
        self._productionHouses = Announcer()

        self._build()

    def addProductionHouse(self, house):
        self._productionHouses.addListener(house)

    def albumCreated(self, album):
        mainScreen = TaggingScreen(album, self._audioPlayer, self._audioFileChooser,
                                   self._imageFileChooser, self)
        mainScreen.addRequestListener(self._productionHouses)
        self.setCentralWidget(mainScreen)
        self._enableFileActions()
        mainScreen.selectFiles()

    def _enableFileActions(self):
        self._addFilesAction.setEnabled(True)
        self._addFolderAction.setEnabled(True)

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
        self._addFilesAction = QAction(self._fileMenu)
        self._addFilesAction.setObjectName(ui.ADD_FILES_ACTION_NAME)
        self._addFilesAction.triggered.connect(lambda: self.centralWidget().selectFiles())
        self._addFilesAction.setDisabled(True)
        self._fileMenu.addAction(self._addFilesAction)
        self._addFolderAction = QAction(self._fileMenu)
        self._addFolderAction.setObjectName(ui.ADD_FOLDER_ACTION_NAME)
        self._addFolderAction.triggered.connect(lambda: self.centralWidget().selectDirectory())
        self._addFolderAction.setDisabled(True)
        self._fileMenu.addAction(self._addFolderAction)
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
        self._addFilesAction.setText(self.tr('Add Files...'))
        self._addFolderAction.setText(self.tr('Add Folder...'))
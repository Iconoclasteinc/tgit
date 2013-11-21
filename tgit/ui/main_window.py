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

from PyQt4.QtGui import QMainWindow, QStatusBar

from tgit.announcer import Announcer
from tgit.record_label import AlbumPortfolioListener
from tgit.csv.csv_format import CsvFormat
from tgit.ui import constants as ui
from tgit.ui.menu_bar import MenuBar
from tgit.ui.welcome_screen import WelcomeScreen
from tgit.ui.tagging_screen import TaggingScreen
from tgit.ui.export_as_dialog import ExportAsDialog
from tgit.ui import stylesheets


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
        taggingScreen = TaggingScreen(album, self._audioPlayer, self._audioFileChooser,
                                      self._imageFileChooser, self)
        taggingScreen.addRequestListener(self._productionHouses)
        self.setCentralWidget(taggingScreen)
        taggingScreen.selectFiles()

    def _build(self):
        self.setObjectName(ui.MAIN_WINDOW_NAME)
        self.setStyleSheet(stylesheets.Main)
        self.resize(*ui.MAIN_WINDOW_SIZE)
        self.setMenuBar(self._makeMenuBar())
        self.setStatusBar(self._makeStatusBar())
        self.setCentralWidget(self._makeWelcomeScreen())
        self.localize()

    def _makeMenuBar(self):
        menuBar = MenuBar()
        menuBar.announceTo(self)
        self._albumPortfolio.addPortfolioListener(menuBar)
        return menuBar

    def selectFiles(self):
        self.centralWidget().selectFiles()

    def selectFolder(self):
        self.centralWidget().selectFolder()

    def _makeStatusBar(self):
        return QStatusBar()

    #todo Organize properly
    def export(self, album):
        dialog = ExportAsDialog(native=True, parent=self)

        class Exporter(object):
            def export(self, album, filename):
                with open(filename, 'wb') as out:
                    format_ = CsvFormat('ISO-8859-1')
                    format_.write(album, out)

        dialog.announceTo(Exporter())
        dialog.show(album)

    def _makeWelcomeScreen(self):
        welcomeScreen = WelcomeScreen(self)
        welcomeScreen.addRequestListener(self._productionHouses)
        return welcomeScreen

    def localize(self):
        self.setWindowTitle(self.tr('TGiT'))
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

from PyQt4.QtGui import QMainWindow

from tgit.announcer import Announcer
from tgit.record_label import AlbumPortfolioListener
from tgit.csv.csv_format import CsvFormat
from tgit.ui import constants as ui
from tgit.ui.menu_bar import MenuBar
from tgit.ui.welcome_screen import WelcomeScreen
from tgit.ui.tagging_screen import TaggingScreen
from tgit.ui.export_as_dialog import ExportAsDialog
from tgit.ui import style

WIN_LATIN1_ENCODING = 'Windows-1252'


class MainWindow(QMainWindow, AlbumPortfolioListener):
    def __init__(self, albumPortfolio, audioPlayer):
        QMainWindow.__init__(self)

        self._albumPortfolio = albumPortfolio
        self._albumPortfolio.addPortfolioListener(self)
        self._audioPlayer = audioPlayer
        self._productionHouses = Announcer()

        self._assemble()

    def addProductionHouse(self, house):
        self._productionHouses.addListener(house)

    def albumCreated(self, album):
        taggingScreen = TaggingScreen(album, self._audioPlayer)
        taggingScreen.addRequestListener(self._productionHouses)
        self.setCentralWidget(taggingScreen)
        taggingScreen.selectFiles()

    def _assemble(self):
        self.setObjectName(ui.MAIN_WINDOW_NAME)
        self.setStyleSheet(style.Sheet)
        self.setMenuBar(self._makeMenuBar())
        self.setCentralWidget(self._makeWelcomeScreen())
        self.localize()
        self.resize(*ui.MAIN_WINDOW_SIZE)

    def _makeMenuBar(self):
        menuBar = MenuBar()
        menuBar.announceTo(self)
        self._albumPortfolio.addPortfolioListener(menuBar)
        return menuBar

    def selectFiles(self):
        self.centralWidget().selectFiles(folders=False)

    def selectFolder(self):
        self.centralWidget().selectFiles(folders=True)

    #todo Organize properly
    def export(self, album):
        dialog = ExportAsDialog(native=True, parent=self)

        class Exporter(object):
            def export(self, album, filename):
                with open(filename, 'wb') as out:
                    format_ = CsvFormat(WIN_LATIN1_ENCODING)
                    format_.write(album, out)

        dialog.announceTo(Exporter())
        dialog.show(album)

    def _makeWelcomeScreen(self):
        welcomeScreen = WelcomeScreen(self)
        welcomeScreen.addRequestListener(self._productionHouses)
        return welcomeScreen

    def localize(self):
        self.setWindowTitle(self.tr('TGiT'))
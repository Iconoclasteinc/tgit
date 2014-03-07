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

from tgit.album import Album
from tgit.mp3.id3_tagger import ID3Tagger
from tgit.embedded_metadata import EmbeddedMetadata
from tgit.album_portfolio import AlbumPortfolioListener
from tgit.csv.csv_format import CsvFormat
from tgit.ui.album_director import AlbumDirector
from tgit.ui.album_exporter import AlbumExporter
from tgit.ui.views.menu_bar import MenuBar
from tgit.ui.welcome_screen import WelcomeScreen
from tgit.ui import style


WIN_LATIN1_ENCODING = 'Windows-1252'


class MainWindow(QMainWindow, AlbumPortfolioListener):
    NAME = 'main-window'
    SIZE = (1100, 750)

    def __init__(self, albumPortfolio, audioPlayer):
        QMainWindow.__init__(self)

        self._albumPortfolio = albumPortfolio
        self._albumPortfolio.addPortfolioListener(self)
        self._audioPlayer = audioPlayer
        self._menuBar = MenuBar()
        self._menuBar.announceTo(self)
        self._welcomeScreen = WelcomeScreen()
        self._welcomeScreen.announceTo(self)

        self._assemble()

    def albumCreated(self, album):
        self._menuBar.enableAlbumMenu()
        self._director = AlbumDirector(album, EmbeddedMetadata(ID3Tagger()), self._audioPlayer)
        self._director.addTracksToAlbum()
        self.setCentralWidget(self._director.render())

    def addFiles(self):
        self._director.addTracksToAlbum()

    def addFolder(self):
        self._director.addTracksToAlbum(folders=True)

    def export(self, album):
        exporter = AlbumExporter(album, CsvFormat(WIN_LATIN1_ENCODING))
        exporter.show()

    def newAlbum(self):
        self._albumPortfolio.addAlbum(Album())

    def _assemble(self):
        self.setObjectName(self.NAME)
        self.setStyleSheet(style.Sheet)
        self.setMenuBar(self._menuBar.render())
        self.setCentralWidget(self._welcomeScreen.render())
        self.translate()
        self.resize(*self.SIZE)

    def translate(self):
        self.setWindowTitle(self.tr('TGiT'))
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
from tgit.album import Album

# todo have shortcuts in tgit.ui.views
from tgit.album_portfolio import AlbumPortfolioListener
from tgit.csv.csv_format import CsvFormat
from tgit.track_library import TrackLibrary
from tgit.mp3.id3_tagger import ID3Tagger
from tgit.ui.album_director import AlbumDirector
from tgit.ui.album_exporter import AlbumExporter
from tgit.ui.views.main_window import MainWindow
from tgit.ui.views.menu_bar import MenuBar
from tgit.ui.views.welcome_screen import WelcomeScreen


WIN_LATIN1_ENCODING = 'windows-1252'


class Tagger(AlbumPortfolioListener):
    def __init__(self, albumPortfolio, audioPlayer):
        self._albumPortfolio = albumPortfolio
        self._albumPortfolio.addPortfolioListener(self)
        self._audioPlayer = audioPlayer
        self._mainWindow = MainWindow()
        self._menuBar = MenuBar()
        self._menuBar.announceTo(self)
        self._welcomeScreen = WelcomeScreen()
        self._welcomeScreen.announceTo(self)

    def render(self):
        window = self._mainWindow.render()
        self._mainWindow.setMenuBar(self._menuBar.render())
        self._mainWindow.show(self._welcomeScreen.render())
        return window

    def newAlbum(self):
        self._albumPortfolio.addAlbum(Album())

    def albumCreated(self, album):
        self._menuBar.enableAlbumMenu()
        self._director = AlbumDirector(album, TrackLibrary(ID3Tagger()), self._audioPlayer)
        self._director.addTracksToAlbum()
        self._mainWindow.show(self._director.render())

    def addFiles(self):
        self._director.addTracksToAlbum()

    def addFolder(self):
        self._director.addTracksToAlbum(folders=True)

    def export(self, album):
        exporter = AlbumExporter(album, CsvFormat(WIN_LATIN1_ENCODING))
        exporter.show()
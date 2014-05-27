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
from tgit.ui.views.album_screen import AlbumScreen
from tgit.ui.views.export_as_dialog import ExportAsDialog
from tgit.ui.views.main_window import MainWindow
from tgit.ui.views.menu_bar import MenuBar
from tgit.ui.views.message_box import MessageBox
from tgit.ui.views.settings_dialog import SettingsDialog
from tgit.ui.views.welcome_screen import WelcomeScreen


WIN_LATIN1_ENCODING = 'windows-1252'


class Tagger(AlbumPortfolioListener):
    def __init__(self, albumPortfolio, player, preferences):
        self.preferences = preferences
        self.albumPortfolio = albumPortfolio
        self.albumPortfolio.addPortfolioListener(self)
        self.player = player

        self.menuBar = MenuBar()
        self.mainWindow = MainWindow()
        self.welcomeScreen = WelcomeScreen()
        self.settings = SettingsDialog(self.mainWindow)
        self.messageBox = MessageBox(self.mainWindow)

    def render(self):
        # todo move to a more appropriate place
        self.settings.addLanguage('en', 'English')
        self.settings.addLanguage('fr', 'French')
        self.settings.bind(ok=self.savePreferences, cancel=self.settings.close)
        self.menuBar.bind(settings=self.editPreferences, addFiles=self.addFiles, addFolder=self.addFolder,
                          exportAlbum=self.export)
        self.mainWindow.setMenuBar(self.menuBar)
        self.welcomeScreen.bind(newAlbum=self.newAlbum)
        self.mainWindow.display(self.welcomeScreen)
        return self.mainWindow

    def newAlbum(self):
        self.albumPortfolio.addAlbum(Album())

    def albumCreated(self, album):
        self.menuBar.enableAlbumActions()
        self.director = AlbumDirector(album, TrackLibrary(ID3Tagger()), self.player, AlbumScreen())
        self.mainWindow.display(self.director.render())
        self.director.addTracksToAlbum()
        self.exporter = AlbumExporter(album, CsvFormat(WIN_LATIN1_ENCODING), ExportAsDialog())

    def addFiles(self):
        self.director.addTracksToAlbum()

    def addFolder(self):
        self.director.addTracksToAlbum(folders=True)

    def export(self):
        self.exporter.select()

    def editPreferences(self):
        self.settings.display(**self.preferences)

    def savePreferences(self):
        self.settings.close()
        self.preferences.add(**self.settings.settings)
        self.messageBox.displayRestartNotice()
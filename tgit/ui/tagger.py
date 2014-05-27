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
    def __init__(self, albumPortfolio, audioPlayer, preferences):
        self.preferences = preferences
        self._albumPortfolio = albumPortfolio
        self._albumPortfolio.addPortfolioListener(self)
        self._audioPlayer = audioPlayer
        self._mainWindow = MainWindow()
        self._menuBar = MenuBar()
        self._menuBar.announceTo(self)
        self._welcomeScreen = WelcomeScreen()

    def render(self):
        self._window = self._mainWindow.render()
        self.settings = SettingsDialog(self._window)
        # todo move to a more appropriate place
        self.settings.addLanguage('en', 'English')
        self.settings.addLanguage('fr', 'French')
        self.settings.bind(ok=self.savePreferences, cancel=self.settings.close)
        self._mainWindow.setMenuBar(self._menuBar.render())
        self._menuBar.bind(settings=self.editPreferences)
        self._welcomeScreen.bind(newAlbum=self.newAlbum)
        self._mainWindow.show(self._welcomeScreen)
        self.messageBox = MessageBox(self._window)
        return self._window

    def newAlbum(self):
        self._albumPortfolio.addAlbum(Album())

    def albumCreated(self, album):
        self._menuBar.enableAlbumMenu()
        self._director = AlbumDirector(album, TrackLibrary(ID3Tagger()), self._audioPlayer, AlbumScreen())
        self._mainWindow.show(self._director.render())
        self._director.addTracksToAlbum()
        self._exporter = AlbumExporter(album, CsvFormat(WIN_LATIN1_ENCODING), ExportAsDialog())

    def addFiles(self):
        self._director.addTracksToAlbum()

    def addFolder(self):
        self._director.addTracksToAlbum(folders=True)

    def export(self):
        self._exporter.select()

    def editPreferences(self):
        self.settings.display(**self.preferences)

    def savePreferences(self):
        self.settings.close()
        self.preferences.add(**self.settings.settings)
        self.messageBox.displayRestartNotice()
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

import functools as func

from tgit.album import Album
from tgit import album_director as director
from tgit.album_portfolio import AlbumPortfolioListener
from tgit.csv.csv_format import CsvFormat
from tgit.track_library import TrackLibrary
from tgit.mp3.id3_tagger import ID3Tagger
from tgit.ui import display
from tgit.ui.album_composer import AlbumComposer
from tgit.ui.album_director import AlbumDirector
from tgit.ui.album_editor import AlbumEditor
from tgit.ui.album_exporter import AlbumExporter
from tgit.ui.album_mixer import AlbumMixer
from tgit.ui.views.album_composition_page import AlbumCompositionPage
from tgit.ui.views.album_edition_page import AlbumEditionPage
from tgit.ui.views.album_screen import AlbumScreen
from tgit.ui.views.export_as_dialog import ExportAsDialog
from tgit.ui.views.main_window import MainWindow
from tgit.ui.views.menu_bar import MenuBar
from tgit.ui.views.message_box import MessageBox
from tgit.ui.views.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.views.settings_dialog import SettingsDialog
from tgit.ui.views.track_edition_page import TrackEditionPage
from tgit.ui.views.track_selection_dialog import TrackSelectionDialog
from tgit.ui.views.welcome_screen import WelcomeScreen


WIN_LATIN1_ENCODING = 'windows-1252'


class Tagger(AlbumPortfolioListener):
    def __init__(self, albumPortfolio, player, preferences):
        self.preferences = preferences
        self.albumPortfolio = albumPortfolio
        self.albumPortfolio.addPortfolioListener(self)
        self.player = player

        self.mainWindow = MainWindow()
        self.menuBar = MenuBar()
        self.mainWindow.setMenuBar(self.menuBar)
        self.welcomeScreen = WelcomeScreen()
        self.mainWindow.display(self.welcomeScreen)

        self.settings = SettingsDialog(self.mainWindow)
        self.settings.addLanguage('en', 'English')
        self.settings.addLanguage('fr', 'French')

        self.messageBox = MessageBox(self.mainWindow)

        self.bindEventHandlers()

    def bindEventHandlers(self):
        self.settings.bind(ok=self.savePreferences, cancel=self.settings.close)
        self.menuBar.bind(settings=self.editPreferences, addFiles=self.mixTracks, addFolder=self.mixAlbum,
                          exportAlbum=self.exportAlbum)
        self.welcomeScreen.bind(newAlbum=self.newAlbum)

    def show(self):
        display.centeredOnScreen(self.mainWindow)

    def newAlbum(self):
        self.albumPortfolio.addAlbum(Album())

    def albumCreated(self, album):
        self.menuBar.enableAlbumActions()

        albumCompositionPage = AlbumCompositionPage()
        albumCompositionPage.bind(add=self.mixTracks)
        composer = AlbumComposer(album, self.player, albumCompositionPage)
        composer.render()

        albumEditionPage = AlbumEditionPage()
        editor = AlbumEditor(album, albumEditionPage, PictureSelectionDialog())
        editor.render()

        trackLibrary = TrackLibrary(ID3Tagger())
        albumScreen = AlbumScreen()
        albumScreen.setAlbumCompositionPage(albumCompositionPage)
        albumScreen.setAlbumEditionPage(albumEditionPage)

        # todo find a home for creation functions
        def makeTrackEditionPage(track):
            page = TrackEditionPage(track)
            page.bind(metadataChanged=func.partial(director.updateTrack, track))
            track.addTrackListener(page)
            album.addAlbumListener(page)
            return page

        self.director = AlbumDirector(album, trackLibrary, self.player, albumScreen, makeTrackEditionPage)

        self.mixer = AlbumMixer(album, trackLibrary, TrackSelectionDialog())
        self.exporter = AlbumExporter(album, CsvFormat(WIN_LATIN1_ENCODING), ExportAsDialog())

        self.mixTracks()
        self.mainWindow.display(albumScreen)

    def mixTracks(self):
        self.mixer.select(album=False)

    def mixAlbum(self):
        self.mixer.select(album=True)

    def exportAlbum(self):
        self.exporter.select()

    def editPreferences(self):
        self.settings.display(**self.preferences)

    def savePreferences(self):
        self.settings.close()
        self.preferences.add(**self.settings.settings)
        self.messageBox.displayRestartNotice()
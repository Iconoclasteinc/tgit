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

from tgit import album_director as director
from tgit.album_portfolio import AlbumPortfolioListener
from tgit.csv.csv_format import CsvFormat
from tgit.track_library import TrackLibrary
from tgit.mp3.id3_tagger import ID3Tagger
from tgit.ui import display
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


def AlbumCompositionPageController(selectTracks, player, album):
    page = AlbumCompositionPage()
    page.bind(add=lambda: selectTracks(album),
              trackMoved=func.partial(director.moveTrack, album),
              play=func.partial(director.playTrack, player, album),
              remove=func.partial(director.removeTrack, player, album))
    page.display(player, album)
    return page


def AlbumEditionPageController(selectPicture, album):
    page = AlbumEditionPage()
    # todo try to replace with signals
    page.bind(metadataChanged=func.partial(director.updateAlbum, album),
              selectPicture=lambda: selectPicture(album),
              removePicture=func.partial(director.removeAlbumCover, album))
    # let page handle this?
    album.addAlbumListener(page)
    page.display(album)
    return page


def TrackEditionPageController(track):
    page = TrackEditionPage(track)
    page.bind(metadataChanged=func.partial(director.updateTrack, track))
    track.addTrackListener(page)
    track.album.addAlbumListener(page)
    return page


def AlbumScreenController(compositionPage, albumPage, trackPage, library, album):
    page = AlbumScreen(album, compositionPage(album), albumPage(album), trackPage)
    page.bind(recordAlbum=func.partial(director.recordAlbum, library, album))
    return page


def PictureSelectionDialogController(parent, album):
    dialog = PictureSelectionDialog(parent)
    dialog.pictureSelected.connect(lambda selection: director.changeAlbumCover(album, selection))
    dialog.display()


def SettingsDialogController(messageBox, preferences, parent):
    dialog = SettingsDialog(parent)

    def savePreferences():
        preferences.add(**dialog.settings)
        dialog.close()
        messageBox(parent).displayRestartNotice()

    dialog.bind(ok=savePreferences, cancel=dialog.close)
    dialog.addLanguage('en', 'English')
    dialog.addLanguage('fr', 'French')
    dialog.display(**preferences)
    return dialog


def ExportAsDialogController(format_, album, parent):
    dialog = ExportAsDialog(parent)
    dialog.exportAs.connect(lambda destination: director.exportAlbum(format_, album, destination))
    dialog.display()


def TrackSelectionDialogController(library, album, parent, folders):
    dialog = TrackSelectionDialog(parent)
    dialog.tracksSelected.connect(lambda selection: director.addTracksToAlbum(library, album, selection))
    dialog.display(folders)


def MenuBarController(exportAs, selectTracks, changeSettings):
    menuBar = MenuBar()
    menuBar.bind(
        addFiles=lambda album: selectTracks(album),
        addFolder=lambda album: selectTracks(album, True),
        exportAlbum=lambda album: exportAs(album),
        settings=lambda: changeSettings())
    return menuBar


def WelcomeScreenController(portfolio):
    page = WelcomeScreen()
    page.bind(newAlbum=lambda: director.createAlbum(portfolio))
    return page


def MainWindowController(menuBar, welcomeScreen, portfolio):
    window = MainWindow()
    menu = menuBar()
    portfolio.addPortfolioListener(menu)
    window.setMenuBar(menu)
    window.display(welcomeScreen())
    return window


class Tagger(AlbumPortfolioListener):
    def __init__(self, albumPortfolio, player, preferences):
        self.preferences = preferences
        self.albumPortfolio = albumPortfolio
        self.albumPortfolio.addPortfolioListener(self)
        self.player = player
        self.trackLibrary = TrackLibrary(ID3Tagger())

        def showSettingsDialog():
            return SettingsDialogController(MessageBox, preferences, self.mainWindow)

        def showExportAsDialog(album):
            return ExportAsDialogController(CsvFormat('windows-1252'), album, self.mainWindow)

        def createMenuBar():
            return MenuBarController(showExportAsDialog, self.showTrackSelectionDialog, showSettingsDialog)

        def createWelcomeScreen():
            return WelcomeScreenController(albumPortfolio)

        def createMainWindow():
            return MainWindowController(createMenuBar, createWelcomeScreen, albumPortfolio)

        self.mainWindow = createMainWindow()

    def show(self):
        display.centeredOnScreen(self.mainWindow)

    def showTrackSelectionDialog(self, album, folders=False):
        return TrackSelectionDialogController(self.trackLibrary, album, self.mainWindow, folders)

    def albumCreated(self, album):
        def createCompositionPage(album):
            return AlbumCompositionPageController(self.showTrackSelectionDialog, self.player, album)

        def createAlbumPage(album):
            return AlbumEditionPageController(showPictureSelectionDialog, album)

        def showPictureSelectionDialog(album):
            return PictureSelectionDialogController(self.mainWindow, album)

        def createTrackPage(track):
            return TrackEditionPageController(track)

        def createAlbumScreen(album):
            return AlbumScreenController(createCompositionPage, createAlbumPage, createTrackPage, self.trackLibrary,
                                         album)

        # 1- change center component
        self.mainWindow.display(createAlbumScreen(album))

        # 2- select tracks
        self.showTrackSelectionDialog(album)
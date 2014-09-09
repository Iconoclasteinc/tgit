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
from Queue import Queue
from threading import Thread
import thread
import threading
from tgit.album import Album
from tgit.ui.isni_lookup_dialog import ISNILookupDialog

from tgit.util import sip_api
from tgit.util import async_task_runner as taskRunner

sip_api.use_v2()

from PyQt4.QtCore import QTimer, QObject, pyqtSignal, QThread

from tgit import album_director as director
from tgit.album_portfolio import AlbumPortfolioListener
from tgit.export.csv_format import CsvFormat

from tgit.ui.album_composition_page import AlbumCompositionPage
from tgit.ui.album_edition_page import AlbumEditionPage
from tgit.ui.album_screen import AlbumScreen
from tgit.ui.export_as_dialog import ExportAsDialog
from tgit.ui.main_window import MainWindow
from tgit.ui.menu_bar import MenuBar
from tgit.ui.restart_message_box import RestartMessageBox
from tgit.ui.picture_selection_dialog import PictureSelectionDialog
from tgit.ui.settings_dialog import SettingsDialog
from tgit.ui.track_edition_page import TrackEditionPage
from tgit.ui.track_selection_dialog import TrackSelectionDialog
from tgit.ui.welcome_screen import WelcomeScreen

# noinspection PyUnresolvedReferences
from tgit.ui import resources


def AlbumCompositionPageController(selectTracks, player, album):
    page = AlbumCompositionPage()
    page.addTracks.connect(lambda: selectTracks(album))
    page.trackMoved.connect(lambda track, position: director.moveTrack(album, track, position))
    page.playTrack.connect(lambda track: director.playTrack(player, track))
    page.removeTrack.connect(lambda track: director.removeTrack(player, album, track))
    page.display(player, album)
    return page


def AlbumEditionPageController(selectPicture, lookupISNIDialogFactory, album, nameRegistry):
    def lookupISNI():
        dialog = lookupISNIDialogFactory(album, queue)
        dialog.show()
        taskRunner.runAsync(lambda: director.lookupISNI(nameRegistry, album.leadPerformer)).andPutResultInto(queue).run()
        dialog.pollIdentityQueue()

    queue = Queue()
    page = AlbumEditionPage(album)
    page.metadataChanged.connect(lambda metadata: director.updateAlbum(album, **metadata))
    page.selectPicture.connect(lambda: selectPicture(album))
    page.removePicture.connect(lambda: director.removeAlbumCover(album))
    page.lookupISNI.connect(lookupISNI)
    page.clearISNI.connect(lambda: director.clearISNI(album))
    album.addAlbumListener(page)
    page.refresh()
    return page


def ISNILookupDialogController(parent, album, queue):
    dialog = ISNILookupDialog(parent, album.leadPerformer, queue)
    dialog.accepted.connect(lambda: director.selectISNI(dialog.selectedIdentity, album))
    dialog.open()
    return dialog


def TrackEditionPageController(album, track):
    page = TrackEditionPage(album, track)
    page.metadataChanged.connect(lambda metadata: director.updateTrack(track, **metadata))
    album.addAlbumListener(page)
    track.addTrackListener(page)
    page.display(album=album, track=track)
    return page


def AlbumScreenController(compositionPage, albumPage, trackPage, library, album):
    page = AlbumScreen(compositionPage(album), albumPage(album), trackPage)
    album.addAlbumListener(page)
    page.recordAlbum.connect(lambda: director.recordAlbum(library, album))
    return page


def PictureSelectionDialogController(parent, album, native):
    dialog = PictureSelectionDialog(parent, native)
    dialog.pictureSelected.connect(lambda selection: director.changeAlbumCover(album, selection))
    dialog.display()


def SettingsDialogController(restartNotice, preferences, parent):
    dialog = SettingsDialog(parent)

    def savePreferences():
        preferences.add(**dialog.settings)
        dialog.close()
        restartNotice(parent).display()

    dialog.accepted.connect(savePreferences)
    dialog.addLanguage('en', dialog.tr('English'))
    dialog.addLanguage('fr', dialog.tr('French'))
    dialog.display(**preferences)
    return dialog


def ExportAsDialogController(format_, album, parent, native):
    dialog = ExportAsDialog(parent, native)
    dialog.exportAs.connect(lambda destination: director.exportAlbum(format_, album, destination))
    dialog.display()


def TrackSelectionDialogController(library, album, parent, native, folders):
    dialog = TrackSelectionDialog(parent, native)
    dialog.tracksSelected.connect(lambda selection: director.addTracksToAlbum(library, album, selection))
    dialog.display(folders)


def MenuBarController(exportAs, selectTracks, changeSettings, portfolio):
    menuBar = MenuBar()
    portfolio.addPortfolioListener(menuBar)
    menuBar.addFiles.connect(lambda album: selectTracks(album))
    menuBar.addFolder.connect(lambda album: selectTracks(album, True))
    menuBar.export.connect(lambda album: exportAs(album))
    menuBar.settings.connect(lambda: changeSettings())
    return menuBar


def WelcomeScreenController(portfolio):
    page = WelcomeScreen()
    page.newAlbum.connect(lambda: director.createAlbum(portfolio))
    return page


def MainWindowController(menuBar, welcomeScreen, albumScreen, portfolio):
    window = MainWindow(menuBar(), welcomeScreen(), albumScreen)
    portfolio.addPortfolioListener(window)
    return window


def createMainWindow(albumPortfolio, player, preferences, library, nameRegistry, native):
    def showSettingsDialog():
        return SettingsDialogController(RestartMessageBox, preferences, window)

    def showExportAsDialog(album):
        return ExportAsDialogController(CsvFormat('windows-1252'), album, window, native)

    def showTrackSelectionDialog(album, folders=False):
        return TrackSelectionDialogController(library, album, window, native, folders)

    def createMenuBar():
        return MenuBarController(showExportAsDialog, showTrackSelectionDialog, showSettingsDialog, albumPortfolio)

    def createWelcomeScreen():
        return WelcomeScreenController(albumPortfolio)

    def createCompositionPage(album):
        return AlbumCompositionPageController(showTrackSelectionDialog, player, album)

    def createAlbumPage(album):
        return AlbumEditionPageController(showPictureSelectionDialog, showISNILookupDialog, album, nameRegistry)

    def showPictureSelectionDialog(album):
        return PictureSelectionDialogController(window, album, native)

    def showISNILookupDialog(album, queue):
        return ISNILookupDialogController(window, album, queue)

    def createAlbumScreen(album):
        def createTrackPage(track):
            return TrackEditionPageController(album, track)

        return AlbumScreenController(createCompositionPage, createAlbumPage, createTrackPage, library, album)

    window = MainWindowController(createMenuBar, createWelcomeScreen, createAlbumScreen, albumPortfolio)

    class SelectAlbumTracks(AlbumPortfolioListener):
        def albumCreated(self, album):
            QTimer.singleShot(250, lambda: showTrackSelectionDialog(album))

    albumPortfolio.addPortfolioListener(SelectAlbumTracks())
    return window

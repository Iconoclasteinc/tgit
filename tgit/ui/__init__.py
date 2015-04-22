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

from queue import Queue

from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QTimer, QEventLoop

from tgit import album_director as director
from tgit.album_portfolio import AlbumPortfolioListener
from tgit.export.csv_format import CsvFormat
from tgit.ui.activity_indicator_dialog import ActivityIndicatorDialog
from tgit.ui.isni_lookup_dialog import ISNILookupDialog
from tgit.ui.performer_dialog import PerformerDialog
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
from tgit.util import async_task_runner as taskRunner


def show(widget):
    widget.show()


def centerOnScreen(widget):
    desktop = QApplication.desktop()
    position = widget.frameGeometry()
    position.moveCenter(desktop.availableGeometry().center())
    widget.move(position.topLeft())


def activate(widget):
    from PyQt5.QtCore import QSysInfo

    if hasattr(QSysInfo, 'MacintoshVersion') and QSysInfo.MacintoshVersion > QSysInfo.MV_10_8:
        # Since Maverick, menu bar does not appear until the window is manually activated, so force
        # user to activate by not raising the window
        pass
    else:
        # we can safely raise the window
        widget.raise_()

    widget.activateWindow()


def showCenteredOnScreen(widget):
    show(widget)
    centerOnScreen(widget)
    activate(widget)


def AlbumCompositionPageController(selectTracks, player, album):
    page = AlbumCompositionPage()
    page.addTracks.connect(lambda: selectTracks(album))
    page.trackMoved.connect(lambda track, position: director.moveTrack(album, track, position))
    page.playTrack.connect(lambda track: director.playTrack(player, track))
    page.removeTrack.connect(lambda track: director.removeTrack(player, album, track))
    page.display(player, album)
    return page


def AlbumEditionPageController(selectPicture, lookupISNIDialogFactory, activityIndicatorDialogFactory,
                               performerDialogFactory, album, nameRegistry):
    def pollQueue():
        while queue.empty():
            QApplication.processEvents(QEventLoop.AllEvents, 100)
        return queue.get(True)

    def lookupISNI():
        activityDialog = activityIndicatorDialogFactory()
        activityDialog.show()
        taskRunner \
            .runAsync(lambda: director.lookupISNI(nameRegistry, album.lead_performer)).andPutResultInto(queue).run()

        identities = pollQueue()
        activityDialog.close()
        dialog = lookupISNIDialogFactory(album, identities)
        dialog.show()

    def assignISNI():
        activityDialog = activityIndicatorDialogFactory()
        activityDialog.show()
        taskRunner.runAsync(lambda: director.assignISNI(nameRegistry, album)).andPutResultInto(queue).run()
        album.isni = pollQueue()
        activityDialog.close()

    def addPerformer():
        dialog = performerDialogFactory(album)
        dialog.show()

    queue = Queue()
    page = AlbumEditionPage(album)
    page.metadataChanged.connect(lambda metadata: director.updateAlbum(album, **metadata))
    page.selectPicture.connect(lambda: selectPicture(album))
    page.removePicture.connect(lambda: director.removeAlbumCover(album))
    page.lookupISNI.connect(lookupISNI)
    page.assignISNI.connect(assignISNI)
    page.clearISNI.connect(lambda: director.clearISNI(album))
    page.addPerformer.connect(addPerformer)
    album.addAlbumListener(page)
    page.refresh()
    return page


def PerformerDialogController(parent, album):
    def assignGuestPerformers():
        album.guestPerformers = dialog.getPerformers()

    dialog = PerformerDialog(parent, album.guestPerformers)
    dialog.accepted.connect(assignGuestPerformers)
    dialog.open()
    return dialog


def ISNILookupDialogController(parent, album, identities):
    dialog = ISNILookupDialog(parent, identities)
    dialog.accepted.connect(lambda: director.selectISNI(dialog.selectedIdentity, album))
    dialog.open()
    return dialog


def ActivityIndicatorDialogController(parent):
    dialog = ActivityIndicatorDialog(parent)
    dialog.open()
    return dialog


def TrackEditionPageController(album, track):
    page = TrackEditionPage(album, track)
    page.metadataChanged.connect(lambda metadata: director.updateTrack(track, **metadata))
    album.addAlbumListener(page)
    track.addTrackListener(page)
    page.display(album=album, track=track)
    return page


def AlbumScreenController(compositionPage, albumPage, trackPage, album):
    page = AlbumScreen(compositionPage(album), albumPage(album), trackPage)
    album.addAlbumListener(page)
    page.recordAlbum.connect(lambda: director.recordAlbum(album))
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
    dialog.exportAs.connect(lambda destination: director.export_album(format_, album, destination, 'windows-1252'))
    dialog.display()


def TrackSelectionDialogController(album, parent, native, folders):
    dialog = TrackSelectionDialog(parent, native)
    dialog.tracks_selected.connect(lambda selection: director.add_tracks_to_album(album, selection))
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


def createMainWindow(albumPortfolio, player, preferences, nameRegistry, native):
    def showSettingsDialog():
        return SettingsDialogController(RestartMessageBox, preferences, window)

    def showExportAsDialog(album):
        return ExportAsDialogController(CsvFormat(), album, window, native)

    def showTrackSelectionDialog(album, folders=False):
        return TrackSelectionDialogController(album, window, native, folders)

    def createMenuBar():
        return MenuBarController(showExportAsDialog, showTrackSelectionDialog, showSettingsDialog, albumPortfolio)

    def createWelcomeScreen():
        return WelcomeScreenController(albumPortfolio)

    def createCompositionPage(album):
        return AlbumCompositionPageController(showTrackSelectionDialog, player, album)

    def createAlbumPage(album):
        return AlbumEditionPageController(showPictureSelectionDialog, showISNILookupDialog, showActivityIndicatorDialog,
                                          showPerformerDialog, album, nameRegistry)

    def showPictureSelectionDialog(album):
        return PictureSelectionDialogController(window, album, native)

    def showISNILookupDialog(album, identities):
        return ISNILookupDialogController(window, album, identities)

    def showPerformerDialog(album):
        return PerformerDialogController(window, album)

    def showActivityIndicatorDialog():
        return ActivityIndicatorDialogController(window)

    def createAlbumScreen(album):
        def createTrackPage(track):
            return TrackEditionPageController(album, track)

        return AlbumScreenController(createCompositionPage, createAlbumPage, createTrackPage, album)

    window = MainWindowController(createMenuBar, createWelcomeScreen, createAlbumScreen, albumPortfolio)

    class SelectAlbumTracks(AlbumPortfolioListener):
        def albumCreated(self, album):
            QTimer.singleShot(250, lambda: showTrackSelectionDialog(album))

    albumPortfolio.addPortfolioListener(SelectAlbumTracks())
    return window

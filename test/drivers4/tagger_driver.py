# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog, QAbstractButton
from test.cute4 import matchers as match
from test.cute4.matchers import showingOnScreen, withText

from test.cute4.widgets import MainWindowDriver, WidgetDriver, ButtonDriver
from test.drivers4.export_as_dialog_driver import exportAsDialog
from test.drivers4.menu_bar_driver import menuBar
from test.drivers4.album_screen_driver import albumScreen
from test.drivers4.settings_dialog_driver import settingsDialog
from test.drivers4.track_selection_dialog_driver import trackSelectionDialog
from test.drivers4.welcome_screen_driver import welcomeScreen


def restartMessage(parent):
    return WidgetDriver.findSingle(parent, QDialog, match.named('restart-message'), showingOnScreen())


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def enterAudioFile(self, filename):
        trackSelectionDialog(self).enterTrack(filename)

    def selectAudioFiles(self, *paths):
        trackSelectionDialog(self).selectTracks(*paths)

    def cancelSelection(self):
        trackSelectionDialog(self).cancel()

    def createAlbum(self):
        welcomeScreen(self).newAlbum()
        self.showsAlbumScreen()

    def showsWelcomeScreen(self):
        welcomeScreen(self).isShowingOnScreen()

    def showsAlbumScreen(self):
        albumScreen(self).isShowingOnScreen()

    def showsExportAsDialog(self):
        exportAsDialog(self).isShowingOnScreen()

    def removeTrack(self, title):
        albumScreen(self).removeTrack(title)

    def moveTrack(self, title, to):
        albumScreen(self).moveTrack(title, to)

    # todo have a quick navigation button
    def next(self):
        albumScreen(self).nextPage()

    def showsAlbumContains(self, *tracks):
        albumScreen(self).showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        albumScreen(self).showsAlbumMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        albumScreen(self).editAlbumMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        albumScreen(self).showsTrackMetadata(**tags)

    def editTrackMetadata(self, **tags):
        albumScreen(self).editTrackMetadata(**tags)

    def saveAlbum(self):
        albumScreen(self).save()

    def changeSettings(self, **settings):
        menuBar(self).settings()
        settingsDialog(self).changeSettings(settings)
        self.acknowledge()

    def hasSettings(self, **settings):
        dialog = menuBar(self).settings()
        dialog.showsSettings(settings)
        dialog.close()

    def acknowledge(self):
        message = restartMessage(self)
        ok = ButtonDriver.findSingle(message, QAbstractButton, withText('OK'))
        ok.click()
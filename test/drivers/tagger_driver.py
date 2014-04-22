# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog, QAbstractButton
from test.cute import matchers as match
from test.cute.matchers import showingOnScreen, withText

from test.cute.widgets import MainWindowDriver, WidgetDriver, ButtonDriver
from test.drivers.export_as_dialog_driver import exportAsDialog
from test.drivers.menu_bar_driver import menuBar
from test.drivers.album_screen_driver import albumScreen
from test.drivers.settings_dialog_driver import settingsDialog
from test.drivers.track_selection_dialog_driver import trackSelectionDialog
from test.drivers.welcome_screen_driver import welcomeScreen


def messageBox(parent):
    return WidgetDriver.findSingle(parent, QDialog, match.named('message-box'), showingOnScreen())


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def addTrack(self, path):
        menuBar(self).addFiles()
        self.selectAudioFile(path)

    def selectAudioFile(self, filename):
        trackSelectionDialog(self).selectTracks(filename)

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
    def toAlbum(self):
        albumScreen(self).nextPage()
        albumScreen(self).isShowingAlbumEditionPage()

    # todo have a quick navigation button
    def toNextTrack(self):
        albumScreen(self).nextPage()
        albumScreen(self).isShowingTrackEditionPage()

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
        menuBar(self).settings()
        settingsDialog(self).showsSettings(settings)

    def acknowledge(self):
        message = messageBox(self)
        ok = ButtonDriver.findSingle(message, QAbstractButton, withText('OK'))
        ok.click()
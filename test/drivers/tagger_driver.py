# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QFileDialog, QWidget, QMenuBar

from test.cute.matchers import named
from test.cute.widgets import dialogWindow, MainWindowDriver, FileDialogDriver, MenuBarDriver
from test.drivers.tagging_screen_driver import TaggingScreenDriver
from test.drivers.welcome_screen_driver import WelcomeScreenDriver

from tgit.ui import constants as ui


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def importTrack(self, path):
        self.selectImportTrackMenuItem()
        self.selectAudioFile(path)

    def selectImportTrackMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._importTrackMenuItem(menu)
        menuItem.isEnabled()
        menuItem.click()

    def _openFileMenu(self):
        menuBar = MenuBarDriver.findSingle(self, QMenuBar)
        menu = menuBar.menu(named(ui.FILE_MENU_NAME))
        menu.open()
        return menu

    def selectAudioFile(self, trackFile):
        dialog = FileDialogDriver(dialogWindow(QFileDialog,
                                               named(ui.CHOOSE_AUDIO_FILE_DIALOG_NAME)),
                                  self.prober, self.gesturePerformer)
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(trackFile))
        dialog.selectFile(os.path.basename(trackFile))
        dialog.accept()

    def createAlbum(self):
        self._welcomeScreen().newAlbum()
        self.isShowingTaggingScreen()

    def isShowingWelcomeScreen(self):
        self._welcomeScreen().isShowingOnScreen()

    def isShowingTaggingScreen(self):
        self._taggingScreen().isShowingOnScreen()

    def hasEnabledImportTrackMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._importTrackMenuItem(menu)
        menuItem.isEnabled()
        menu.close()

    def removeTrack(self, title):
        self._taggingScreen().removeTrack(title)

    def moveTrack(self, title, to):
        self._taggingScreen().moveTrack(title, to)

    # todo have a quick navigation button
    def toAlbum(self):
        self._taggingScreen().nextPage()
        self._taggingScreen().isShowingAlbumMetadata()

    # todo have a quick navigation button
    def toNextTrack(self):
        self._taggingScreen().nextPage()
        self._taggingScreen().isShowingTrackMetadata()

    def showsAlbumContains(self, *tracks):
        self._taggingScreen().showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        self._taggingScreen().showsAlbumMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        self._taggingScreen().editAlbumMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        self._taggingScreen().showsTrackMetadata(**tags)

    def editTrackMetadata(self, **tags):
        self._taggingScreen().editTrackMetadata(**tags)

    def saveAlbum(self):
        self._taggingScreen().saveAlbum()

    def _taggingScreen(self):
        return TaggingScreenDriver.findSingle(self, QWidget, named(ui.TAGGING_SCREEN_NAME))

    def _welcomeScreen(self):
        return WelcomeScreenDriver.findSingle(self, QWidget, named(ui.WELCOME_SCREEN_NAME))

    def _importTrackMenuItem(self, menu):
        return menu.menuItem(named(ui.IMPORT_TRACK_ACTION_NAME))
# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QFileDialog, QWidget, QMenuBar

from test.cute.matchers import named
from test.cute.widgets import window, MainWindowDriver, FileDialogDriver, MenuBarDriver
from test.drivers.tagging_screen_driver import TaggingScreenDriver
from test.drivers.welcome_screen_driver import WelcomeScreenDriver

from tgit.ui import constants as ui


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def addTrack(self, path):
        self.selectAddFilesMenuItem()
        self.selectAudioFile(path)

    def selectAddFilesMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._addFilesMenuItem(menu)
        menuItem.isEnabled()
        menuItem.click()

    def _openFileMenu(self):
        menuBar = MenuBarDriver.findSingle(self, QMenuBar)
        menu = menuBar.menu(named(ui.FILE_MENU_NAME))
        menu.open()
        return menu

    def selectAudioFile(self, filename):
        dialog = FileDialogDriver(window(QFileDialog, named(ui.CHOOSE_AUDIO_FILES_DIALOG_NAME)),
                                  self.prober, self.gesturePerformer)
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def createAlbum(self):
        self._welcomeScreen().newAlbum()
        self.isShowingTaggingScreen()

    def isShowingWelcomeScreen(self):
        self._welcomeScreen().isShowingOnScreen()

    def isShowingTaggingScreen(self):
        self._taggingScreen().isShowingOnScreen()

    def hasEnabledAddFilesMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._addFilesMenuItem(menu)
        menuItem.isEnabled()
        menu.close()

    def hasEnabledAddFolderMenuItem(self):
        menu = self._openFileMenu()
        menuItem = self._addFolderMenuItem(menu)
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

    def _addFilesMenuItem(self, menu):
        return menu.menuItem(named(ui.ADD_FILES_ACTION_NAME))

    def _addFolderMenuItem(self, menu):
        return menu.menuItem(named(ui.ADD_FOLDER_ACTION_NAME))
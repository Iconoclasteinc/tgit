# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QFileDialog, QWidget

from test.cute.matchers import named
from test.cute.widgets import window, MainWindowDriver, FileDialogDriver
from test.drivers.menu_bar_driver import menuBar
from test.drivers.tagging_screen_driver import TaggingScreenDriver
from test.drivers.welcome_screen_driver import welcomeScreen

from tgit.ui import constants as ui


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def addTrack(self, path):
        menuBar(self).addFiles()
        self.selectAudioFile(path)

    def selectAudioFile(self, filename):
        dialog = FileDialogDriver(window(QFileDialog, named(ui.CHOOSE_AUDIO_FILES_DIALOG_NAME)),
                                  self.prober, self.gesturePerformer)
        dialog.showHiddenFiles()
        dialog.navigateToDir(os.path.dirname(filename))
        dialog.selectFile(os.path.basename(filename))
        dialog.accept()

    def createAlbum(self):
        welcomeScreen(self).newAlbum()
        self.showsTaggingScreen()

    def showsWelcomeScreen(self):
        welcomeScreen(self).isShowingOnScreen()

    def showsTaggingScreen(self):
        self._taggingScreen().isShowingOnScreen()

    def showsExportAsDialog(self):
        self._exportAsDialog().isShowingOnScreen()

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

    def _exportAsDialog(self):
        return FileDialogDriver(window(QFileDialog, named(ui.EXPORT_AS_DIALOG_NAME)),
                                self.prober, self.gesturePerformer)
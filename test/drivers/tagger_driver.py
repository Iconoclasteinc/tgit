# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import QFileDialog, QWidget

from test.cute.matchers import named
from test.cute.widgets import window, MainWindowDriver, FileDialogDriver
from test.drivers.menu_bar_driver import menuBar
from test.drivers.tagging_screen_driver import TaggingScreenDriver, taggingScreen
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
        taggingScreen(self).isShowingOnScreen()

    def showsExportAsDialog(self):
        self._exportAsDialog().isShowingOnScreen()

    def removeTrack(self, title):
        taggingScreen(self).removeTrack(title)

    def moveTrack(self, title, to):
        taggingScreen(self).moveTrack(title, to)

    # todo have a quick navigation button
    def toAlbum(self):
        taggingScreen(self).nextPage()
        taggingScreen(self).isShowingAlbumMetadata()

    # todo have a quick navigation button
    def toNextTrack(self):
        taggingScreen(self).nextPage()
        taggingScreen(self).isShowingTrackMetadata()

    def showsAlbumContains(self, *tracks):
        taggingScreen(self).showsAlbumContains(*tracks)

    def showsAlbumMetadata(self, **tags):
        taggingScreen(self).showsAlbumMetadata(**tags)

    def editAlbumMetadata(self, **tags):
        taggingScreen(self).editAlbumMetadata(**tags)

    def showsTrackMetadata(self, **tags):
        taggingScreen(self).showsTrackMetadata(**tags)

    def editTrackMetadata(self, **tags):
        taggingScreen(self).editTrackMetadata(**tags)

    def saveAlbum(self):
        taggingScreen(self).saveAlbum()

    def _exportAsDialog(self):
        return FileDialogDriver(window(QFileDialog, named(ui.EXPORT_AS_DIALOG_NAME)),
                                self.prober, self.gesturePerformer)
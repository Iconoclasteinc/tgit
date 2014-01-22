# -*- coding: utf-8 -*-

from test.cute.widgets import MainWindowDriver
from test.drivers.export_as_dialog_driver import exportAsDialog
from test.drivers.menu_bar_driver import menuBar
from test.drivers.tagging_screen_driver import taggingScreen
from test.drivers.track_selection_dialog_driver import trackSelectionDialog
from test.drivers.welcome_screen_driver import welcomeScreen


class TaggerDriver(MainWindowDriver):
    def __init__(self, selector, prober, gesturePerformer):
        super(TaggerDriver, self).__init__(selector, prober, gesturePerformer)

    def addTrack(self, path):
        menuBar(self).addFiles()
        self.selectAudioFile(path)

    def selectAudioFile(self, filename):
        trackSelectionDialog(self).selectTracks(filename)

    def createAlbum(self):
        welcomeScreen(self).newAlbum()
        self.showsTaggingScreen()

    def showsWelcomeScreen(self):
        welcomeScreen(self).isShowingOnScreen()

    def showsTaggingScreen(self):
        taggingScreen(self).isShowingOnScreen()

    def showsExportAsDialog(self):
        exportAsDialog(self).isShowingOnScreen()

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
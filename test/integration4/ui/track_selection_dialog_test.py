# -*- coding: utf-8 -*-
import sys
import unittest

from hamcrest import contains

from PyQt4.QtGui import QMainWindow, QFileDialog

from test.cute4.matchers import named
from test.cute4.widgets import window
from test.drivers4.track_selection_dialog_driver import TrackSelectionDialogDriver
from test.integration4.ui import ViewTest
from test.cute4.probes import ValueMatcherProbe
from test.util4 import resources

from tgit4.ui.track_selection_dialog import TrackSelectionDialog


class TrackSelectionDialogTest(ViewTest):
    def setUp(self):
        super(TrackSelectionDialogTest, self).setUp()
        window = QMainWindow()
        self.show(window)
        self.dialog = TrackSelectionDialog(window, native=False)
        self.driver = self.trackSelectionDriver()

    def trackSelectionDriver(self):
        return TrackSelectionDialogDriver(window(QFileDialog, named('track-selection-dialog')), self.prober,
                                          self.gesturePerformer)

    def testSignalsWhenAudioFilesSelected(self):
        audioFiles = [resources.path('audio', 'Rolling in the Deep.mp3'),
                      resources.path('audio', 'Set Fire to the Rain.mp3'),
                      resources.path('audio', 'Someone Like You.mp3')]
        trackSelectionSignal = ValueMatcherProbe('track(s) selection', audioFiles)
        self.dialog.tracksSelected.connect(trackSelectionSignal.received)

        self.dialog.display(folders=False)
        self.driver.selectTracks(*audioFiles)
        self.check(trackSelectionSignal)

    def testAlternativelySelectsDirectoriesInsteadOfFiles(self):
        audioFolder = resources.path('audio')
        trackSelectionSignal = ValueMatcherProbe('track(s) selection', contains(audioFolder))
        self.dialog.tracksSelected.connect(trackSelectionSignal.received)

        self.dialog.display(folders=True)
        self.driver.selectTracksInFolder(audioFolder)
        self.check(trackSelectionSignal)

    @unittest.skipIf(sys.platform.startswith("win"), "not supported on Windows")
    def testRejectsNonAudioFiles(self):
        self.dialog.display(folders=False)
        unsupportedFile = resources.path('front-cover.jpg')
        self.driver.rejectsSelectionOf(unsupportedFile)

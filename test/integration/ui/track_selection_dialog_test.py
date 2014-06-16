# -*- coding: utf-8 -*-

from hamcrest import contains
from PyQt4.QtGui import QMainWindow

from test.drivers.track_selection_dialog_driver import trackSelectionDialog
from test.integration.ui import ViewTest
from test.cute.probes import ValueMatcherProbe
from test.util import resources
from tgit.ui.track_selection_dialog import TrackSelectionDialog


class TrackSelectionDialogTest(ViewTest):
    def setUp(self):
        super(TrackSelectionDialogTest, self).setUp()
        window = QMainWindow()
        self.show(window)
        TrackSelectionDialog.native = False
        self.dialog = TrackSelectionDialog(window)
        self.driver = trackSelectionDialog(self)

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

    def testRejectsNonAudioFiles(self):
        self.dialog.display(folders=False)
        unsupportedFile = resources.path('front-cover.jpg')
        self.driver.rejectsSelectionOf(unsupportedFile)

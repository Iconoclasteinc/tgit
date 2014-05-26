# -*- coding: utf-8 -*-

from hamcrest import contains
from PyQt4.QtGui import QMainWindow

from test.drivers.track_selection_dialog_driver import trackSelectionDialog
from test.integration.ui.views import ViewTest
from test.cute.probes import ValueMatcherProbe
from test.util import resources
from tgit.ui.views.track_selection_dialog import TrackSelectionDialog


class TrackSelectionDialogTest(ViewTest):
    def setUp(self):
        super(TrackSelectionDialogTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.show(self.mainWindow)
        TrackSelectionDialog.native = False
        self.dialog = TrackSelectionDialog()
        self.driver = trackSelectionDialog(self)

    def testSignalsWhenAudioFilesSelected(self):
        audioFiles = [resources.path('audio', '1.mp3'),
                      resources.path('audio', '2.mp3'),
                      resources.path('audio', '3.mp3')]
        trackSelectionSignal = ValueMatcherProbe('track(s) selection', audioFiles)
        self.dialog.bind(tracksSelected=trackSelectionSignal.received)
        self.dialog.show()
        self.driver.selectTracks(*audioFiles)
        self.check(trackSelectionSignal)

    def testSupportsSelectingDirectoriesInsteadOfFiles(self):
        audioFolder = resources.path('audio')
        trackSelectionSignal = ValueMatcherProbe('track(s) selection', contains(audioFolder))
        self.dialog.bind(tracksSelected=trackSelectionSignal.received)
        self.dialog.show(folders=True)
        self.driver.selectTracksInFolder(audioFolder)
        self.check(trackSelectionSignal)

    def testRejectsNonAudioFiles(self):
        self.dialog.show()
        unsupportedFile = resources.path('front-cover.jpg')
        self.driver.rejectsSelectionOf(unsupportedFile)

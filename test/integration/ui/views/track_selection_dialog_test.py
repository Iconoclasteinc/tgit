# -*- coding: utf-8 -*-

from hamcrest import contains
from PyQt4.QtGui import QMainWindow

from test.drivers.track_selection_dialog_driver import trackSelectionDialog
from test.integration.ui.view_test import ViewTest
from test.cute.probes import ValueMatcherProbe
from test.util import resources
from tgit.ui.views.track_selection_dialog import TrackSelectionDialog


class TrackSelectionDialogTest(ViewTest):
    def setUp(self):
        super(TrackSelectionDialogTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.show(self.mainWindow)
        self.dialog = TrackSelectionDialog()
        self.dialog.native = False
        self.dialog.filter = '*.mp3'
        self.driver = trackSelectionDialog(self)

    def testSignalsWhenAudioFilesSelected(self):
        audioFiles = [resources.path('audio', '1.mp3'),
                      resources.path('audio', '2.mp3'),
                      resources.path('audio', '3.mp3')]
        selection = ValueMatcherProbe('track(s) selection', audioFiles)

        class SelectionListener(object):
            def tracksSelected(self, files):
                selection.received(files)

        self.dialog.announceTo(SelectionListener())
        self.dialog.render()
        self.driver.selectTracks(*audioFiles)
        self.check(selection)

    def testSupportsSelectingDirectoriesInsteadOfFiles(self):
        audioFolder = resources.path('audio')
        selection = ValueMatcherProbe('track(s) selection', contains(audioFolder))

        class SelectionListener(object):
            def tracksSelected(self, files):
                selection.received(files)

        self.dialog.announceTo(SelectionListener())
        self.dialog.render(folderMode=True)
        self.driver.selectTracksInFolder(audioFolder)
        self.check(selection)

    def testRejectsNonAudioFiles(self):
        self.dialog.render()
        unsupportedFile = resources.path('front-cover.jpg')
        self.driver.rejectsSelectionOf(unsupportedFile)

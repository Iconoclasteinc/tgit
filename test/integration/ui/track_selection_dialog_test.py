# -*- coding: utf-8 -*-

from hamcrest import equal_to
from test.drivers.track_selection_dialog_driver import trackSelectionDialog

from test.integration.ui.view_test import ViewTest
from PyQt4.QtGui import QMainWindow

from test.cute.probes import ValueMatcherProbe
from test.util import resources
from tgit.ui.track_selection_dialog import TrackSelectionDialog


class TrackSelectionDialogTest(ViewTest):
    def setUp(self):
        super(TrackSelectionDialogTest, self).setUp()
        self.mainWindow = QMainWindow()
        self.show(self.mainWindow)
        self.chooser = TrackSelectionDialog()
        self.chooser.native = False
        self.driver = trackSelectionDialog(self)

    def testSelectsMultipleAudioFilesAndNotifiesListeners(self):
        audioFiles = (resources.path('audio', '1.mp3'),
                      resources.path('audio', '2.mp3'),
                      resources.path('audio', '3.mp3'))
        filesChosen = ValueMatcherProbe('choosen files', equal_to(audioFiles))

        class ChosenFiles(object):
            def filesChosen(self, *filenames):
                filesChosen.received(filenames)

        self.chooser.addChoiceListener(ChosenFiles())
        self.chooser.chooseFiles()
        self.driver.selectTracks(*audioFiles)
        self.check(filesChosen)

    def testSelectsAudioFilesInDirectoryAndNotifiesListeners(self):
        audioFiles = (resources.path('audio', '1.mp3'),
                      resources.path('audio', '2.mp3'),
                      resources.path('audio', '3.mp3'))
        filesChosen = ValueMatcherProbe('choosen files', equal_to(audioFiles))

        class ChosenFiles(object):
            def filesChosen(self, *filenames):
                filesChosen.received(filenames)

        self.chooser.addChoiceListener(ChosenFiles())
        self.chooser.chooseDirectory()
        self.driver.selectTracks(resources.path('audio'))

        self.check(filesChosen)

    # todo when file does not exist, it pops up a dialog that we have to dismiss
    # def testOnlyAcceptsExistingFiles(self):
    #     filename = resources.path('unknown.mp3')
    #     self.chooser.chooseFile()
    #     self.driver.enterManually(filename)
    #     self.driver.acceptButton().isDisabled()
    #     self.driver.reject()

    def testOnlyAcceptsAudioFiles(self):
        imageFile = resources.path('front-cover.jpg')
        self.chooser.chooseFiles()
        self.driver.rejectsSelectionOf(imageFile)


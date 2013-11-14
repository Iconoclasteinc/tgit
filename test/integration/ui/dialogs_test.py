# -*- coding: utf-8 -*-

import os

from hamcrest import equal_to

from test.integration.ui.base_widget_test import BaseWidgetTest
from PyQt4.QtGui import QMainWindow, QFileDialog

from test.cute.widgets import FileDialogDriver, window
from test.cute.matchers import named
from test.cute.probes import ValueMatcherProbe
from test.util import resources
from tgit.ui import constants as ui
from tgit.ui.dialogs import AudioFileChooserDialog


class AudioFileChooserDialogTest(BaseWidgetTest):
    def setUp(self):
        super(AudioFileChooserDialogTest, self).setUp()
        mainWindow = QMainWindow()
        self.view(mainWindow)
        self.chooser = AudioFileChooserDialog(native=False, parent=mainWindow)

        self.driver = FileDialogDriver(
            window(QFileDialog, named(ui.CHOOSE_AUDIO_FILES_DIALOG_NAME)),
            self.prober, self.gesturePerformer)

    def testSelectsMultipleAudioFilesAndNotifiesListeners(self):
        files = (resources.path('audio', '1.mp3'),
                 resources.path('audio', '2.mp3'),
                 resources.path('audio', '3.mp3'))
        filesChosen = ValueMatcherProbe('choosen files', equal_to(files))

        class ChosenFiles(object):
            def filesChosen(self, *filenames):
                filesChosen.received(filenames)

        self.chooser.addChoiceListener(ChosenFiles())
        self.chooser.chooseFiles()
        self.driver.navigateToDir(resources.path('audio'))
        self.driver.selectFiles(*[os.path.basename(filename) for filename in files])
        self.driver.accept()

        self.check(filesChosen)

    def testSelectsAudioFilesAudioFilesInDirectoryAndNotifiesListeners(self):
        files = (resources.path('audio', '1.mp3'),
                 resources.path('audio', '2.mp3'),
                 resources.path('audio', '3.mp3'))
        filesChosen = ValueMatcherProbe('choosen files', equal_to(files))

        class ChosenFiles(object):
            def filesChosen(self, *filenames):
                filesChosen.received(filenames)

        self.chooser.addChoiceListener(ChosenFiles())
        self.chooser.chooseDirectory()
        self.driver.navigateToDir(resources.TEST_RESOURCES_DIR)
        self.driver.selectFile('audio')
        self.driver.accept()

        self.check(filesChosen)

    # todo when file does not exist, it pops up a dialog that we have to dismiss
    # def testOnlyAcceptsExistingFiles(self):
    #     filename = resources.path('unknown.mp3')
    #     self.chooser.chooseFile()
    #     self.driver.enterManually(filename)
    #     self.driver.acceptButton().isDisabled()
    #     self.driver.reject()

    def testOnlyAcceptsAudioFiles(self):
        filename = resources.path('front-cover.jpg')

        self.chooser.chooseFiles()
        self.driver.navigateToDir(os.path.dirname(filename))
        self.driver.selectFile(os.path.basename(filename))
        self.driver.acceptButton().isDisabled()
        self.driver.reject()


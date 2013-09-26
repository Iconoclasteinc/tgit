# -*- coding: utf-8 -*-

import unittest
from hamcrest.core import *
from flexmock import flexmock

import use_sip_api_v2
from PyQt4.Qt import QApplication

from tests.cute.probes import ValueMatcherProbe
from tests.endtoend.tgit_driver import TGiTDriver
from tests.util import resources
from tgit.ui.main_window import MainWindow


class MainWindowTest(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.mainWindow = MainWindow()
        self.driver = TGiTDriver(1000)

    def tearDown(self):
        self.driver.close()
        del self.driver
        del self.app

    def testRequestsTrackToBeAddedToAlbumWhenTrackFileHasBeenSelectedForImport(self):
        trackFile = resources.path("Hallelujah.mp3")
        importRequest = ValueMatcherProbe(equal_to(trackFile), "request to import track file")

        class DetectTrackImport(object):
            def importTrack(self, filename):
                importRequest.setReceivedValue(filename)

        self.mainWindow.addMusicDirector(DetectTrackImport())
        self.driver.importTrack(trackFile)
        self.driver.check(importRequest)

    def testDisplaysSelectedTrackReleaseName(self):
        track = flexmock(releaseName='Release Name')
        self.mainWindow.trackSelected(track)
        self.driver.showsReleaseName('Release Name')

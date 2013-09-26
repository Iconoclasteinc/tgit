# -*- coding: utf-8 -*-

import unittest
from hamcrest.core import equal_to
from flexmock import flexmock

import use_sip_api_v2
from PyQt4.Qt import QApplication

from tests.cute.probes import ValueMatcherProbe
from tests.endtoend.tgit_driver import TGiTDriver
from tests.util import resources
from tests.endtoend.fake_audio_library import readContent
from tgit.ui.main_window import MainWindow


def buildTrack(**tags):
    defaults = dict(releaseName='',
                    frontCoverPicture=(None, None),
                    leadPerformer='')
    return flexmock(**dict(defaults.items() + tags.items()))


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

    @unittest.skip("todo")
    def testHasNothingToShowWhenTrackHasNoMetadata(self):
        raise AssertionError("Not yet implemented")

    def testDisplaysSelectedTrackAlbumReleaseName(self):
        track = buildTrack(releaseName='Release Name')
        self.mainWindow.trackSelected(track)
        self.driver.showsReleaseName('Release Name')

    def testDisplaysSelectedTrackAlbumFrontCoverScaledToPictureDisplayArea(self):
        frontCover = ('image/jpeg', readContent(resources.path("front-cover.jpg")))
        track = buildTrack(frontCoverPicture=frontCover)
        self.mainWindow.trackSelected(track)
        self.driver.displaysFrontCoverPictureWithSize(125, 125)

    def testDisplaysSelectedTrackAlbumLeadPerformer(self):
        track = buildTrack(leadPerformer='Lead Performer')
        self.mainWindow.trackSelected(track)
        self.driver.showsLeadPerformer('Lead Performer')
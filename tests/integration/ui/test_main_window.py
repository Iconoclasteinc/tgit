# -*- coding: utf-8 -*-

import unittest
from hamcrest.core import equal_to
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
from PyQt4.Qt import QApplication

from tests.cute.probes import ValueMatcherProbe
from tests.endtoend.tgit_driver import TGiTDriver
from tests.util import resources
from tests.endtoend.fake_audio_library import readContent
from tgit.ui.main_window import MainWindow


def buildTrack(**tags):
    defaults = dict(releaseName=None,
                    frontCoverPicture=(None, None),
                    leadPerformer=None,
                    releaseDate=None,
                    upc=None,
                    trackTitle=None,
                    versionInfo=None,
                    featuredGuest=None,
                    isrc=None,
                    bitrate=96000,
                    duration=200)
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

    def testDisplaysSelectedTrackAlbumReleaseDate(self):
        track = buildTrack(releaseDate='2009-08-05')
        self.mainWindow.trackSelected(track)
        self.driver.showsReleaseDate('2009-08-05')

    def testDisplaysSelectedTrackAlbumUpc(self):
        track = buildTrack(upc='1234567899999')
        self.mainWindow.trackSelected(track)
        self.driver.showsUpc('1234567899999')

    def testDisplaysSelectedTrackTitle(self):
        track = buildTrack(trackTitle='Track Title')
        self.mainWindow.trackSelected(track)
        self.driver.showsTrackTitle('Track Title')

    def testDisplaysSelectedTrackVersionInfo(self):
        track = buildTrack(versionInfo='Version Info')
        self.mainWindow.trackSelected(track)
        self.driver.showsVersionInfo('Version Info')

    def testDisplaysSelectedTrackFeaturedGuest(self):
        track = buildTrack(featuredGuest='Featured Guest')
        self.mainWindow.trackSelected(track)
        self.driver.showsFeaturedGuest('Featured Guest')

    def testDisplaysSelectedTrackIsrc(self):
        track = buildTrack(isrc='ISRC')
        self.mainWindow.trackSelected(track)
        self.driver.showsIsrc('ISRC')

    def testDisplaysSelectedTrackBitrateInKbps(self):
        track = buildTrack(bitrate=128000)
        self.mainWindow.trackSelected(track)
        self.driver.showsBitrate('128 kbps')

    def testDisplaysSelectedTrackDurationAsText(self):
        track = buildTrack(duration=275)
        self.mainWindow.trackSelected(track)
        self.driver.showsDuration('04:35')
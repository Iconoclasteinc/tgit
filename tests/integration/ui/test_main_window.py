# -*- coding: utf-8 -*-

import unittest
import mimetypes
from hamcrest.core import equal_to
from hamcrest.library import has_properties, contains, has_length
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)
from PyQt4.Qt import QApplication

from tests.cute.probes import ValueMatcherProbe
from tests.drivers.tagger_driver import TaggerDriver
from tests.util import resources
from tests.endtoend.fake_audio_library import readContent
from tgit.ui import main_window as main
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
        self.driver = TaggerDriver(1000)

    def tearDown(self):
        self.driver.close()
        del self.driver
        del self.app

    def testMakesRequestToAddTrackToAlbumWhenTrackFileIsSelectedUsingImportDialog(self):
        trackFile = resources.path("Hallelujah.mp3")
        importRequest = ValueMatcherProbe(equal_to(trackFile), "request to import track")

        class DetectTrackImport(object):
            def importTrack(self, filename):
                importRequest.setReceivedValue(filename)

        self.mainWindow.addMusicDirector(DetectTrackImport())
        self.driver.importTrack(trackFile)
        self.driver.check(importRequest)

    @unittest.skip("todo")
    def testHasNothingToShowWhenTrackHasNoMetadata(self):
        raise AssertionError("Not yet implemented")

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

    def testMakesRequestToSaveModifiedTrackWhenSaveButtonIsClicked(self):
        modifications = dict(releaseName='Release Name',
                             frontCoverPicture=resources.path("front-cover.jpg"),
                             leadPerformer='Lead Performer',
                             releaseDate='2009-08-05',
                             upc='123456789999',
                             trackTitle='Track Title',
                             versionInfo='Version Info',
                             featuredGuest='Featured Guest',
                             isrc='AABB12345678')
        saveRequest = ValueMatcherProbe(sameMetadataAs(**modifications), "request to save track")

        class DetectSaveTrack(object):
            def saveTrack(self, track):
                saveRequest.setReceivedValue(track)

        self.mainWindow.addMusicDirector(DetectSaveTrack())
        self.mainWindow.trackSelected(buildTrack())
        self.driver.editAlbumMetadata(**modifications)
        self.driver.editTrackMetadata(**modifications)
        self.driver.saveTrack()
        self.driver.check(saveRequest)


def sameMetadataAs(**tags):
    if 'frontCoverPicture' in tags:
        tags['frontCoverPicture'] = samePictureAs(tags['frontCoverPicture'])
    return has_properties(**tags)


# todo move to a file related utilities module
def readContent(filename):
    return open(filename, "rb").read()


# todo move to a file related utilities module
def guessMimeType(filename):
    return mimetypes.guess_type(filename)[0]


# todo move to a matchers module
def samePictureAs(filename):
    return contains(equal_to(guessMimeType(filename)),
                    has_length(len(readContent(filename))))


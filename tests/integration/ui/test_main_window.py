# -*- coding: utf-8 -*-

import unittest
from hamcrest.core import equal_to
from hamcrest.library import has_properties
from flexmock import flexmock

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)

from tests.cute.probes import ValueMatcherProbe
from tests.cute.finders import WidgetIdentity
from tests.drivers.tagger_driver import TaggerDriver
from tests.integration.ui.base_widget_test import BaseWidgetTest
from tests.util import resources
from tests.util.matchers import samePictureAs
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


class MainWindowTest(BaseWidgetTest):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.mainWindow = MainWindow()
        self.view(self.mainWindow)
        self.driver = self.createDriverFor(self.mainWindow)

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    def testMakesRequestToAddTrackToAlbumWhenTrackFileIsSelectedUsingImportDialog(self):
        trackFile = resources.path("Hallelujah.mp3")
        importRequest = ValueMatcherProbe(equal_to(trackFile), "request to import track")

        class DetectTrackImport(object):
            def importTrack(self, filename):
                importRequest.setReceivedValue(filename)

        self.mainWindow.addMusicDirector(DetectTrackImport())
        self.driver.importTrack(trackFile)
        self.driver.check(importRequest)

    def testCanNavigateBetweenAlbumAndTrackPanels(self):
        self.mainWindow.trackSelected(buildTrack())
        self.driver.nextStep()
        self.driver.previousStep()
        self.driver.nextStep()

    @unittest.skip("todo")
    def testHasNothingToShowWhenTrackHasNoMetadata(self):
        raise AssertionError("Not yet implemented")

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
        self.driver.nextStep()
        self.driver.editTrackMetadata(**modifications)
        self.driver.saveTrack()
        self.driver.check(saveRequest)


def sameMetadataAs(**tags):
    if 'frontCoverPicture' in tags:
        tags['frontCoverPicture'] = samePictureAs(tags['frontCoverPicture'])
    return has_properties(**tags)
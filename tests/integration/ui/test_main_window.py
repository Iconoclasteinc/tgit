# -*- coding: utf-8 -*-

import unittest
from hamcrest import equal_to, has_properties

import use_sip_api_v2 as sipApi
sipApi.useVersion(sipApi.VERSION_2)

from tgit.ui.main_window import MainWindow

from tests.cute.probes import ValueMatcherProbe
from tests.cute.finders import WidgetIdentity
from tests.drivers.tagger_driver import TaggerDriver
from tests.integration.ui.base_widget_test import BaseWidgetTest
from tests.util import resources, doubles
from tests.util.matchers import samePictureAs


class MainWindowTest(BaseWidgetTest):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.mainWindow = MainWindow()
        self.view(self.mainWindow)
        self.tagger = self.createDriverFor(self.mainWindow)

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    # todo Move to welcome panel tests once welcome panel is extracted
    def testImportsTrackToAlbumWhenAddTrackButtonIsClicked(self):
        trackFile = resources.path("Hallelujah.mp3")
        importRequest = ValueMatcherProbe(equal_to(trackFile), "request to import track")

        class DetectTrackImport(object):
            def importTrack(self, filename):
                importRequest.setReceivedValue(filename)

        self.mainWindow.addMusicDirector(DetectTrackImport())
        self.tagger.addTrackToAlbum(trackFile)
        self.tagger.check(importRequest)

    def testImportsTrackToAlbumWhenImportTrackMenuItemIsSelected(self):
        trackFile = resources.path("Hallelujah.mp3")
        importRequest = ValueMatcherProbe(equal_to(trackFile), "request to import track")

        class DetectTrackImport(object):
            def importTrack(self, filename):
                importRequest.setReceivedValue(filename)

        self.mainWindow.addMusicDirector(DetectTrackImport())
        self.tagger.importTrackThroughMenu(trackFile)
        self.tagger.check(importRequest)

    def testSwitchesToTrackListWhenFirstTrackIsImported(self):
        self.tagger.isShowingWelcomePanel()
        self.mainWindow.trackImported(doubles.track())
        self.tagger.isShowingTrackList()

    def testAddsATrackPageForEachImportedTrack(self):
        self.mainWindow.trackImported(doubles.track(title='First Track'))
        self.mainWindow.trackImported(doubles.track(title='Second Track'))
        self.mainWindow.trackImported(doubles.track(title='Third Track'))
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(title='First Track')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(title='Second Track')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(title='Third Track')

    def testCanNavigateBackAndForthBetweenPages(self):
        self.mainWindow.trackImported(doubles.track())
        self.mainWindow.trackImported(doubles.track())
        self.tagger.isShowingTrackList()
        self.tagger.nextStep()
        self.tagger.isShowingAlbumMetadata()
        self.tagger.nextStep()
        self.tagger.isShowingTrackMetadata()
        self.tagger.nextStep()
        self.tagger.isShowingTrackMetadata()
        self.tagger.previousStep()
        self.tagger.isShowingTrackMetadata()
        self.tagger.previousStep()
        self.tagger.isShowingAlbumMetadata()
        self.tagger.previousStep()
        self.tagger.isShowingTrackList()
        self.tagger.nextStep()
        self.tagger.isShowingAlbumMetadata()

    def testNextButtonIsDisabledWhenViewingLastTrack(self):
        self.mainWindow.trackImported(doubles.track())
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.hasNextStepDisabled()

        self.mainWindow.trackImported(doubles.track())
        self.tagger.nextStep()
        self.tagger.hasNextStepDisabled()

    def testStaysOnCurrentPageWhenASubsequentTrackIsImported(self):
        self.mainWindow.trackImported(doubles.track(title='First Track'))
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(title='First Track')
        self.mainWindow.trackImported(doubles.track())
        self.tagger.showsTrackMetadata(title='First Track')

    def testAlbumMetadataShowsMetadataOfFirstImportedTrack(self):
        self.mainWindow.trackImported(doubles.track(releaseName='First Album'))
        self.tagger.nextStep()
        self.tagger.showsAlbumMetadata(releaseName='First Album')
        self.mainWindow.trackImported(doubles.track(releaseName='Second Album'))
        self.tagger.showsAlbumMetadata(releaseName='First Album')

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
        self.mainWindow.trackImported(doubles.track())
        self.tagger.navigateToAlbumMetadata()
        self.tagger.editAlbumMetadata(**modifications)
        self.tagger.navigateToTrackMetadata()
        self.tagger.editTrackMetadata(**modifications)
        self.tagger.saveTrack()
        self.tagger.check(saveRequest)


def sameMetadataAs(**tags):
    if 'frontCoverPicture' in tags:
        tags['frontCoverPicture'] = samePictureAs(tags['frontCoverPicture'])
    return has_properties(**tags)
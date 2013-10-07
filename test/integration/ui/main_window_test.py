# -*- coding: utf-8 -*-

from hamcrest import equal_to, has_properties, contains

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util import resources, doubles
from test.util.matchers import samePictureAs
from test.util.mp3_maker import MP3

from tgit.ui.main_window import MainWindow


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
        trackFile = MP3().make().filename
        addTrackRequest = ValueMatcherProbe(equal_to(trackFile), "request to add track")

        class AddTrackToAlbumProbe(object):
            def addToAlbum(self, filename):
                addTrackRequest.setReceivedValue(filename)

        self.mainWindow.setMusicDirector(AddTrackToAlbumProbe())
        self.tagger.addTrackToAlbum(trackFile)
        self.tagger.check(addTrackRequest)

    def testImportsTrackToAlbumWhenImportTrackMenuItemIsSelected(self):
        trackFile = MP3().make().filename
        addTrackRequest = ValueMatcherProbe(equal_to(trackFile), "request to add track")

        class AddTrackToAlbumProbe(object):
            def addToAlbum(self, filename):
                addTrackRequest.setReceivedValue(filename)

        self.mainWindow.setMusicDirector(AddTrackToAlbumProbe())
        self.tagger.importTrackThroughMenu(trackFile)
        self.tagger.check(addTrackRequest)

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

    def testSavesAllAlbumAndTrackMetadata(self):
        modifications = dict(releaseName='Release Name',
                             frontCoverPicture=resources.path("front-cover.jpg"),
                             leadPerformer='Lead Performer',
                             releaseDate='2009-08-05',
                             upc='123456789999',
                             trackTitle='Track Title',
                             versionInfo='Version Info',
                             featuredGuest='Featured Guest',
                             isrc='AABB12345678')
        trackIncludesAlbumAndTrackModifications = \
            ValueMatcherProbe(contains(hasMetadata(**modifications)), "request to save track")

        class CaptureSaveRequest(object):
            def saveAlbum(self, album):
                trackIncludesAlbumAndTrackModifications.setReceivedValue(album)

        self.mainWindow.setMusicDirector(CaptureSaveRequest())
        self.mainWindow.trackImported(doubles.track())
        self.tagger.nextStep()
        self.tagger.editAlbumMetadata(**modifications)
        self.tagger.nextStep()
        self.tagger.editTrackMetadata(**modifications)
        self.tagger.saveAlbum()
        self.tagger.check(trackIncludesAlbumAndTrackModifications)

    def testSavesAllImportedTracks(self):
            allTracksAreSaved = ValueMatcherProbe(contains(
                hasMetadata(releaseName='Album', trackTitle='Track 1'),
                hasMetadata(releaseName='Album', trackTitle='Track 2'),
                hasMetadata(releaseName='Album', trackTitle='Track 3')), "request to save album")

            class CaptureSaveRequest(object):
                def saveAlbum(self, album):
                    allTracksAreSaved.setReceivedValue(album)

            self.mainWindow.setMusicDirector(CaptureSaveRequest())
            self.mainWindow.trackImported(doubles.track())
            self.mainWindow.trackImported(doubles.track())
            self.mainWindow.trackImported(doubles.track())
            self.tagger.nextStep()
            self.tagger.editAlbumMetadata(releaseName='Album')
            self.tagger.nextStep()
            self.tagger.editTrackMetadata(trackTitle='Track 1')
            self.tagger.nextStep()
            self.tagger.editTrackMetadata(trackTitle='Track 2')
            self.tagger.nextStep()
            self.tagger.editTrackMetadata(trackTitle='Track 3')
            self.tagger.saveAlbum()
            self.tagger.check(allTracksAreSaved)


def hasMetadata(**tags):
    if 'frontCoverPicture' in tags:
        tags['frontCoverPicture'] = samePictureAs(tags['frontCoverPicture'])
    return has_properties(**tags)
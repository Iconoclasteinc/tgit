# -*- coding: utf-8 -*-

from hamcrest import equal_to, has_properties, contains

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util import resources, doubles
from test.util.matchers import samePictureAs
from test.util.mp3_maker import MP3
from test.util.fake_audio_library import FakeAudioLibrary

from tgit.ui.main_window import MainWindow


class MainWindowTest(BaseWidgetTest):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.mainWindow = MainWindow()
        self.view(self.mainWindow)
        self.tagger = self.createDriverFor(self.mainWindow)
        self.audioLibrary = FakeAudioLibrary()

    def tearDown(self):
        self.audioLibrary.delete()
        super(MainWindowTest, self).tearDown()

    def createDriverFor(self, widget):
        return TaggerDriver(WidgetIdentity(widget), self.prober, self.gesturePerformer)

    # todo Move to welcome panel tests once welcome panel is extracted
    def testImportsTrackToAlbumWhenAddTrackButtonIsClicked(self):
        mp3 = self.audioLibrary.add(MP3())
        addTrackRequest = ValueMatcherProbe("request to add track", equal_to(mp3.filename))

        class AddTrackToAlbumProbe(object):
            def addToAlbum(self, filename):
                addTrackRequest.setReceivedValue(filename)

        self.mainWindow.setMusicProducer(AddTrackToAlbumProbe())
        self.tagger.addTrackToAlbum(mp3.filename)
        self.tagger.check(addTrackRequest)

    def testImportsTrackToAlbumWhenImportTrackMenuItemIsSelected(self):
        mp3 = self.audioLibrary.add(MP3())
        addTrackRequest = ValueMatcherProbe("request to add track", equal_to(mp3.filename))

        class AddTrackToAlbumProbe(object):
            def addToAlbum(self, filename):
                addTrackRequest.setReceivedValue(filename)

        self.mainWindow.setMusicProducer(AddTrackToAlbumProbe())
        self.tagger.importTrackThroughMenu(mp3.filename)
        self.tagger.check(addTrackRequest)

    def testSwitchesToTrackListWhenFirstTrackIsImported(self):
        self.tagger.isShowingWelcomePanel()
        self._addTrack()
        self.tagger.isShowingTrackList()

    def testAddsATrackPageForEachImportedTrack(self):
        self._addTrack(trackTitle='Track 1')
        self._addTrack(trackTitle='Track 2')
        self._addTrack(trackTitle='Track 3')

        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 2')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')

    def testCanNavigateBackAndForthBetweenPages(self):
        self._addTrack()
        self._addTrack()

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
        self._addTrack()
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.hasNextStepDisabled()

        self._addTrack()
        self.tagger.nextStep()
        self.tagger.hasNextStepDisabled()

    def testStaysOnCurrentPageWhenASubsequentTrackIsImported(self):
        self._addTrack(trackTitle='Track 1')
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self._addTrack()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')

    def testAlbumMetadataShowsMetadataOfFirstImportedTrack(self):
        self._addTrack(releaseName='Album 1')
        self.tagger.nextStep()
        self.tagger.showsAlbumMetadata(releaseName='Album 1')
        self._addTrack(releaseName='Album 2')
        self.tagger.showsAlbumMetadata(releaseName='Album 1')

    def testSavesAllAlbumAndTrackMetadata(self):
        self._addTrack()

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
            ValueMatcherProbe("request to save track", contains(hasMetadata(**modifications)))

        class CaptureSaveRequest(object):
            def saveAlbum(self, album):
                trackIncludesAlbumAndTrackModifications.setReceivedValue(album)

        self.mainWindow.setMusicProducer(CaptureSaveRequest())

        self.tagger.nextStep()
        self.tagger.editAlbumMetadata(**modifications)
        self.tagger.nextStep()
        self.tagger.editTrackMetadata(**modifications)
        self.tagger.saveAlbum()
        self.tagger.check(trackIncludesAlbumAndTrackModifications)

    def testSavesAllImportedTracks(self):
        self._addTrack()
        self._addTrack()
        self._addTrack()

        allTracksAreSaved = ValueMatcherProbe("request to save album", contains(
            hasMetadata(releaseName='Album', trackTitle='Track 1'),
            hasMetadata(releaseName='Album', trackTitle='Track 2'),
            hasMetadata(releaseName='Album', trackTitle='Track 3')))

        class CaptureSaveRequest(object):
            def saveAlbum(self, album):
                allTracksAreSaved.setReceivedValue(album)

        self.mainWindow.setMusicProducer(CaptureSaveRequest())

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

    def testDeletesCorrespondingPageWhenTrackIsRemovedFromAlbum(self):
        track1 = self._addTrack(trackTitle="Track 1")
        track2 = self._addTrack(trackTitle="Track 2")
        track3 = self._addTrack(trackTitle="Track 3")

        self.mainWindow.trackRemoved(track2)
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(tracktle='Track 1')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')
        # Tracks can only be removed from track list, so go back there
        # todo when we can navigate directly to the track list, change the navigation
        self.tagger.previousStep()
        self.tagger.previousStep()
        self.tagger.previousStep()
        self.mainWindow.trackRemoved(track1)
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(tracktle='Track 3')
        # Let's go back again to the track list
        self.tagger.previousStep()
        self.tagger.previousStep()
        self.mainWindow.trackRemoved(track3)
        self.tagger.hasNextStepDisabled()

    def testReordersPagesWhenTracksPositionsChangeInAlbum(self):
        track1 = self._addTrack(trackTitle="Track 1")
        track2 = self._addTrack(trackTitle="Track 2")
        track3 = self._addTrack(trackTitle="Track 3")

        self.mainWindow.trackMoved(track1, 2)
        self.mainWindow.trackRemoved(track2)
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.tagger.hasNextStepDisabled()

    def testUpdatesImportedTrackWithAlbumMetadata(self):
        self._addTrack(trackTitle="Track 1", releaseName='Album')
        self._addTrack(trackTitle="Track 2")
        self._addTrack(trackTitle="Track 3")

        self.tagger.showsAlbumContains(['Track 1', 'Album'],
                                       ['Track 2', 'Album'],
                                       ['Track 3', 'Album'])

    def testTrackListShowsUpToDateTrackAndAlbumMetadata(self):
        self._addTrack()
        self._addTrack()
        self._addTrack()
        self.tagger.nextStep()
        self.tagger.editAlbumMetadata(releaseName='Album')
        self.tagger.nextStep()
        self.tagger.editTrackMetadata(trackTitle='Track 1')
        self.tagger.nextStep()
        self.tagger.editTrackMetadata(trackTitle='Track 2')
        self.tagger.nextStep()
        self.tagger.editTrackMetadata(trackTitle='Track 3')
        self.tagger.previousStep()
        self.tagger.previousStep()
        self.tagger.previousStep()
        self.tagger.previousStep()

        self.tagger.showsAlbumContains(['Track 1', 'Album'],
                                       ['Track 2', 'Album'],
                                       ['Track 3', 'Album'])

    def _addTrack(self, **details):
        track = doubles.track(**details)
        self.mainWindow.trackAdded(track)
        return track


def hasMetadata(**tags):
    if 'frontCoverPicture' in tags:
        tags['frontCoverPicture'] = samePictureAs(tags['frontCoverPicture'])
    return has_properties(**tags)
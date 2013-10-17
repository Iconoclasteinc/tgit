# -*- coding: utf-8 -*-

from hamcrest import equal_to, has_properties, contains, has_length, has_property

from test.integration.ui.base_widget_test import BaseWidgetTest
from test.cute.probes import ValueMatcherProbe
from test.cute.finders import WidgetIdentity
from test.drivers.tagger_driver import TaggerDriver
from test.util import resources, doubles
from test.util import mp3, fs
from test.util.fake_audio_library import FakeAudioLibrary

from tgit.album import Album
from tgit.track import Track
from tgit.ui.main_window import MainWindow


class MainWindowTest(BaseWidgetTest):
    def setUp(self):
        super(MainWindowTest, self).setUp()
        self.album = Album()
        self.mainWindow = MainWindow(self.album)
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
        track = self.audioLibrary.add(mp3.makeMp3())
        addTrackRequest = ValueMatcherProbe("request to add track", equal_to(track.filename))

        class AddTrackToAlbumProbe(object):
            def addTrack(self, filename):
                addTrackRequest.setReceivedValue(filename)

        self.mainWindow.addMusicProducer(AddTrackToAlbumProbe())
        self.tagger.addTrackToAlbum(track.filename)
        self.tagger.check(addTrackRequest)

    def testImportsTrackToAlbumWhenImportTrackMenuItemIsSelected(self):
        track = self.audioLibrary.add(mp3.makeMp3())
        addTrackRequest = ValueMatcherProbe("request to add track", equal_to(track.filename))

        class AddTrackToAlbumProbe(object):
            def addTrack(self, filename):
                addTrackRequest.setReceivedValue(filename)

        self.mainWindow.addMusicProducer(AddTrackToAlbumProbe())
        self.tagger.importTrackThroughMenu(track.filename)
        self.tagger.check(addTrackRequest)

    def testSwitchesToTrackListWhenFirstTrackIsImported(self):
        self.tagger.isShowingWelcomePanel()
        self.addTrack()
        self.tagger.isShowingTrackList()

    def testAddsATrackPageForEachImportedTrack(self):
        self.addTrack(trackTitle='Track 1')
        self.addTrack(trackTitle='Track 2')
        self.addTrack(trackTitle='Track 3')

        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 2')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')

    def testCanNavigateBackAndForthBetweenPages(self):
        self.addTrack()
        self.addTrack()

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
        self.addTrack()
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.hasNextStepDisabled()

        self.addTrack()
        self.tagger.nextStep()
        self.tagger.hasNextStepDisabled()

    def testStaysOnCurrentPageWhenASubsequentTrackIsImported(self):
        self.addTrack(trackTitle='Track 1')
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.addTrack()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')

    def testSavesAllAlbumAndTrackMetadata(self):
        albumMetadata = dict(releaseName='Release Name',
                             frontCoverPicture=resources.path("front-cover.jpg"),
                             leadPerformer='Lead Performer',
                             guestPerformers='Guest Performers',
                             labelName='Label Name',
                             recordingTime='2009-05-04',
                             releaseTime='2009-08-05',
                             originalReleaseTime='1973-08-05',
                             upc='123456789999')
        trackMetadata = dict(trackTitle='Track Title',
                             versionInfo='Version Info',
                             featuredGuest='Featured Guest',
                             isrc='AABB12345678')

        allMetadata = dict(albumMetadata.items() + trackMetadata.items())
        # todo have custom matchers, such as anAlbumWithTracks
        saveRequest = \
            ValueMatcherProbe("request to save track",
                              has_property('tracks', contains(hasMetadata(**allMetadata))))

        class CaptureSaveRequest(object):
            def __init__(self, album):
                self._album = album

            def saveAlbum(self):
                saveRequest.setReceivedValue(self._album)

        self.addTrack()
        self.mainWindow.addMusicProducer(CaptureSaveRequest(self.album))
        self.tagger.nextStep()
        self.tagger.editAlbumMetadata(**albumMetadata)
        self.tagger.nextStep()
        self.tagger.editTrackMetadata(**trackMetadata)
        self.tagger.saveAlbum()
        self.tagger.check(saveRequest)

    def testSavesAllImportedTracks(self):
        self.addTrack()
        self.addTrack()
        self.addTrack()

        allTracksAreSaved = ValueMatcherProbe(
            "request to save album",
            has_property('tracks', contains(
                hasMetadata(releaseName='Album', trackTitle='Track 1'),
                hasMetadata(releaseName='Album', trackTitle='Track 2'),
                hasMetadata(releaseName='Album', trackTitle='Track 3'))))

        class CaptureSaveRequest(object):
            def __init__(self, album):
                self._album = album

            def saveAlbum(self):
                allTracksAreSaved.setReceivedValue(self._album)

        self.mainWindow.addMusicProducer(CaptureSaveRequest(self.album))

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
        track1 = self.addTrack(trackTitle="Track 1")
        track2 = self.addTrack(trackTitle="Track 2")
        track3 = self.addTrack(trackTitle="Track 3")

        self.removeTrack(track2)
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
        self.removeTrack(track1)
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(tracktle='Track 3')
        # Let's go back again to the track list
        self.tagger.previousStep()
        self.tagger.previousStep()
        self.removeTrack(track3)
        self.tagger.hasNextStepDisabled()

    def testReordersPagesWhenTracksPositionsChangeInAlbum(self):
        track1 = self.addTrack(trackTitle="Track 1")
        track2 = self.addTrack(trackTitle="Track 2")
        self.addTrack(trackTitle="Track 3")

        self.mainWindow.trackMoved(track1, 2)
        self.removeTrack(track2)
        self.tagger.nextStep()
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 3')
        self.tagger.nextStep()
        self.tagger.showsTrackMetadata(trackTitle='Track 1')
        self.tagger.hasNextStepDisabled()

    def testUpdatesImportedTrackWithAlbumMetadata(self):
        self.addTrack(trackTitle="Track 1", releaseName='Album')
        self.addTrack(trackTitle="Track 2")
        self.addTrack(trackTitle="Track 3")

        self.tagger.showsAlbumContains(['Track 1', 'Album'],
                                       ['Track 2', 'Album'],
                                       ['Track 3', 'Album'])

    def testTrackListShowsUpToDateTrackAndAlbumMetadata(self):
        self.addTrack()
        self.addTrack()
        self.addTrack()
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

    def addTrack(self, **details):
        track = Track(doubles.audio(**details))
        self.album.appendTrack(track)
        self.mainWindow.trackAdded(track)
        return track

    def removeTrack(self, track):
        self.album.removeTrack(track)
        self.mainWindow.trackRemoved(track)


def hasMetadata(**tags):
    if 'frontCoverPicture' in tags:
        pictureFile = tags['frontCoverPicture']
        tags['frontCoverPicture'] = contains(fs.guessMimeType(pictureFile),
                                             has_length(len(fs.readContent(pictureFile))))
    return has_properties(**tags)
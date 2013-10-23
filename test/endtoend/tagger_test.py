# -*- coding: utf-8 -*-

import unittest

from test.util import resources
from test.util.mp3 import makeMp3
from test.endtoend.application_runner import ApplicationRunner
from test.util.fake_audio_library import FakeAudioLibrary

SAMPLE_AUDIO_FILE = resources.path('Hallelujah.mp3')


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audioLibrary = FakeAudioLibrary()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audioLibrary.delete()

    # todo create a test mp3 from a sample realistic mpeg frame and make expected values explicit
    def testTaggingASingleTrackAndSavingChanges(self):
        track = self.audioLibrary.add(makeMp3(SAMPLE_AUDIO_FILE))

        self.application.newAlbum(track.filename)
        self.application.showsAlbumContent(['Hallelujah (Chorus)'])
        self.application.showsAlbumMetadata(
            releaseName='',
            leadPerformer='')
        self.application.changeAlbumMetadata(
            frontCover=resources.path('minions-in-black.jpg'),
            releaseName='Despicable Me',
            leadPerformer='Tim, Mark and Phil')
        self.application.showsTrackMetadata(
            trackTitle='Hallelujah (Chorus)',
            duration='03:56')
        self.application.changeTrackMetadata(
            trackTitle='Potato Banana Song',
            featuredGuest='Stuart')
        self.audioLibrary.containsFile(
            track.filename,
            releaseName='Despicable Me',
            leadPerformer='Tim, Mark and Phil',
            trackTitle='Potato Banana Song',
            featuredGuest='Stuart',
            frontCover=resources.path('minions-in-black.jpg'))

    def testTaggingMultipleTracksFromTheSameAlbum(self):
        track1 = self.audioLibrary.add(makeMp3(trackTitle='Track 1'))
        track2 = self.audioLibrary.add(makeMp3(trackTitle='Track 2'))

        self.application.newAlbum(track1.filename)
        self.application.importTrack(track2.filename)
        self.application.showsAlbumContent(['Track 1'], ['Track 2'])
        self.application.showsAlbumMetadata()
        self.application.changeAlbumMetadata(releaseName='Despicable Me')
        self.application.showsTrackMetadata(trackTitle='Track 1')
        self.application.changeTrackMetadata(trackTitle='Potato Banana Song')
        self.application.showsTrackMetadata(trackTitle='Track 2')
        self.application.changeTrackMetadata(trackTitle='Potato Banana Song (Remix)')

        self.audioLibrary.containsFile(track1.filename,
                                       releaseName='Despicable Me',
                                       trackTitle='Potato Banana Song')
        self.audioLibrary.containsFile(track2.filename,
                                       releaseName='Despicable Me',
                                       trackTitle='Potato Banana Song (Remix)')

    # todo Consider exercising the different ways of adding a track
    def testChangingTheAlbumCompositionFromTheTrackList(self):
        track1 = self.audioLibrary.add(makeMp3(releaseName='Original Title', trackTitle='Track 1'))
        track2 = self.audioLibrary.add(makeMp3(releaseName='Original Title', trackTitle='Track 2'))
        track3 = self.audioLibrary.add(makeMp3(releaseName='Original Title', trackTitle='Track 3'))

        self.application.newAlbum(track1.filename)
        self.application.importTrack(track2.filename)
        self.application.importTrack(track3.filename)

        self.application.showsAlbumContent(['Track 1'], ['Track 2'], ['Track 3'])
        self.application.moveTrack('Track 1', 'Track 3')
        self.application.removeTrack('Track 2')
        self.application.showsAlbumMetadata()
        self.application.changeAlbumMetadata(releaseName='Modified Title')
        self.application.showsTrackMetadata(trackTitle='Track 3')
        self.application.showsTrackMetadata(trackTitle='Track 1')

        self.audioLibrary.containsFile(track1.filename,
                                       trackTitle='Track 1',
                                       releaseName='Modified Title')
        self.audioLibrary.containsFile(track2.filename,
                                       trackTitle='Track 2',
                                       releaseName='Original Title')
        self.audioLibrary.containsFile(track3.filename,
                                       trackTitle='Track 3',
                                       releaseName='Modified Title')

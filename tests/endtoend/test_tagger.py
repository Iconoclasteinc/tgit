# -*- coding: utf-8 -*-

import unittest

from tests.util import resources
from tests.util.mp3_maker import MP3
from tests.endtoend.application_runner import ApplicationRunner
from tests.endtoend.fake_audio_library import FakeAudioLibrary

SAMPLE_AUDIO_FILE = resources.path("Hallelujah.mp3")


def copy(track):
    return MP3(track).make()


def mp3(**tags):
    return MP3(**tags).make()


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
        track = copy(SAMPLE_AUDIO_FILE)
        self.audioLibrary.add(track.filename)

        self.application.importTrack(track.filename)
        self.application.showsAlbumContent('Hallelujah (Chorus)')
        self.application.showsAlbumMetadata(
            releaseName='Messiah',
            leadPerformer='The Sixteen - Harry Christophers')
        self.application.changeAlbumMetadata(
            frontCoverPicture=resources.path("minions-in-black.jpg"),
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
            frontCoverFile=resources.path("minions-in-black.jpg"))

    @unittest.skip("wip")
    def testTaggingMultipleTracksFromTheSameAlbum(self):
        track1 = mp3(releaseName='Album Title', trackTitle='Track 1')
        track2 = mp3(releaseName='Album Title', trackTitle='Track 2')

        self.application.importTrack(track1.filename)
        self.application.importTrack(track2.filename)
        self.application.showsAlbumContent('Track 1', 'Track 2')
        self.application.showsAlbumMetadata(releaseName='Album Title')
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
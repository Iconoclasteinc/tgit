# -*- coding: utf-8 -*-

import unittest

from tests.util import resources
from tests.endtoend.application_runner import ApplicationRunner
from tests.endtoend.fake_audio_library import FakeAudioLibrary

SAMPLE_AUDIO_FILE = resources.path("Hallelujah.mp3")


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audioLibrary = FakeAudioLibrary()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audioLibrary.delete()

    # todo create a test mp3 from a sample realistic mpeg frame and make expected values explicit
    @unittest.skip("wip")
    def testTaggerModifiesTagsOfAnExistingAudioFileAndSavesChanges(self):
        filename = self.audioLibrary.importFile(SAMPLE_AUDIO_FILE)
        self.application.importTrack(filename)
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
            filename,
            releaseName='Despicable Me',
            leadPerformer='Tim, Mark and Phil',
            trackTitle='Potato Banana Song',
            featuredGuest='Stuart',
            frontCoverFile=resources.path("minions-in-black.jpg"))
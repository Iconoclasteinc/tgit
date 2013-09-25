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
        self.audioLibrary.destroy()

    # todo At some point, low level details (i.e. testing modification of all tags) need to move
    # to ui integration tests with Qt targeting the UI in isolation from the domain.
    # This will be possible after teasing apart MainWindow  and introducing the domain concepts.
    # The end-to-end test will then focus on the overall scenario at a higher level of details.

    # todo create a test mp3 from a sample realistic mpeg frame and make expected values explicit
    def testTaggerModifiesTagsOfAnExistingAudioFileAndSavesChanges(self):
        audioFile = self.audioLibrary.addFile(SAMPLE_AUDIO_FILE)
        self.application.importAudioFile(audioFile)
        self.application.showsMetadata(releaseName='Messiah',
                                       leadPerformer='The Sixteen - Harry Christophers',
                                       originalReleaseDate='2008-03-01',
                                       upc='123456789999',
                                       trackTitle='Hallelujah (Chorus)',
                                       featuredGuest='Carolyn Sampson',
                                       versionInfo='Original Version',
                                       isrc='USPR37300012',
                                       bitrate="320 kbps",
                                       duration='03:56',
                                       frontCoverEmbeddedText='Title: Handel Messiah')
        self.application.changeMetadata(releaseName='Despicable Me',
                                        leadPerformer='Tim, Mark and Phil',
                                        originalReleaseDate='2010-07-09',
                                        upc='987654321111',
                                        trackTitle='Potato Banana Song',
                                        versionInfo='Remix',
                                        featuredGuest='Stuart',
                                        isrc='FRUP11000001',
                                        frontCoverPicture=resources.path("minions-in-black.jpg"))
        self.audioLibrary.containsFileWithMetadata(audioFile,
                                                   releaseName='Despicable Me',
                                                   leadPerformer='Tim, Mark and Phil',
                                                   originalReleaseDate='2010-07-09',
                                                   upc='987654321111',
                                                   trackTitle='Potato Banana Song',
                                                   versionInfo='Remix',
                                                   featuredGuest='Stuart',
                                                   isrc='FRUP11000001',
                                                   frontCoverFile=resources.path(
                                                       "minions-in-black.jpg"))
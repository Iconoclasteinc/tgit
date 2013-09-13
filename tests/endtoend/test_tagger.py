# -*- coding: utf-8 -*-

import unittest

from tests.util import project
from tests.endtoend.application_runner import ApplicationRunner
from tests.endtoend.fake_audio_library import FakeAudioLibrary

SAMPLE_AUDIO_FILE = project.test_resource_path("Hallelujah.mp3")


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audio_library = FakeAudioLibrary()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audio_library.destroy()

    def test_tagger_modifies_tags_of_an_existing_audio_file_and_saves_changes(self):
        audio_file = self.audio_library.add_file(SAMPLE_AUDIO_FILE)
        self.application.import_audio_file(audio_file)
        self.application.shows_metadata(album='Messiah',
                                        artist='The Sixteen - Harry Christophers',
                                        track='Hallelujah (Chorus)',
                                        bitrate="320 kps",
                                        duration='03:56')
        self.application.change_metadata(album='Despicable Me',
                                         artist='Tim, Mark and Phil',
                                         track='Potato Banana Song')
        self.audio_library.has_file_with_metadata(audio_file,
                                                  album='Despicable Me',
                                                  artist='Tim, Mark and Phil',
                                                  track='Potato Banana Song')
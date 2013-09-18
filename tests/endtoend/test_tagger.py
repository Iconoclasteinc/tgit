# -*- coding: utf-8 -*-

import unittest

from tests.util import project
from tests.endtoend.application_runner import ApplicationRunner
from tests.endtoend.fake_audio_library import FakeAudioLibrary

SAMPLE_AUDIO_FILE = project.test_resource_path("Hallelujah.mp3")
SAMPLE_COVER_ART_FILE = project.test_resource_path("banana-song-cover.png")


class TaggerTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.audio_library = FakeAudioLibrary()
        self.application.start()

    def tearDown(self):
        self.application.stop()
        self.audio_library.destroy()

    # todo At some point, low level details (i.e. testing modification of all tags) need to move
    # to ui integration tests with Qt targeting the UI in isolation from the domain.
    # This will be possible after teasing apart MainWindow  and introducing the domain concepts.
    # The end-to-end test will then focus on the overall scenario at a higher level of details.

    # todo create a test mp3 from a sample realistic mpeg frame and make expected values explicit
    def test_tagger_modifies_tags_of_an_existing_audio_file_and_saves_changes(self):
        audio_file = self.audio_library.add_file(SAMPLE_AUDIO_FILE)
        self.application.import_audio_file(audio_file)
        self.application.shows_metadata(release_name='Messiah',
                                        lead_performer='The Sixteen - Harry Christophers',
                                        track_title='Hallelujah (Chorus)',
                                        bitrate="320 kps",
                                        duration='03:56',
                                        version_info='',
                                        front_cover_embedded_text='Title: Handel Messiah')
        self.application.change_metadata(release_name='Despicable Me',
                                         lead_performer='Tim, Mark and Phil',
                                         track_title='Potato Banana Song',
                                         version_info='Remix',
                                         front_cover_picture=SAMPLE_COVER_ART_FILE)
        self.audio_library.has_file_with_metadata(audio_file,
                                                  release_name='Despicable Me',
                                                  lead_performer='Tim, Mark and Phil',
                                                  track_title='Potato Banana Song',
                                                  version_info='Remix',
                                                  front_cover_picture=SAMPLE_COVER_ART_FILE)
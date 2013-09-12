# -*- coding: utf-8 -*-

import unittest

from tests.util import project
from tests.endtoend.application_runner import ApplicationRunner


class TGiTTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.application.start()

    def tearDown(self):
        self.application.stop()

    def test_displaying_an_existing_music_file_metadata(self):
        self.application.select_music_file(project.test_resource_path("Hallelujah.mp3"))
        self.application.shows_music_metadata(artist='The Sixteen - Harry Christophers', album='Messiah',
                                              title='Hallelujah (Chorus)', bitrate="320 kps",
                                              duration='03:56')
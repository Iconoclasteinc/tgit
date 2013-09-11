# -*- coding: utf-8 -*-

import unittest

import project
from application_runner import ApplicationRunner


class TGiTTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.application.start()

    def tearDown(self):
        self.application.stop()

    def test_displaying_an_existing_music_file_metadata(self):
        self.application.select_music_file(project.test_resource("ma-preference.mp3"))
        self.application.shows_music_metadata(artist='Julien Clerc',album='Triple Best Of',
                                              title='Ma préférence', bitrate=44100,
                                              duration='3:23')

if __name__ == '__main__':
    unittest.main()
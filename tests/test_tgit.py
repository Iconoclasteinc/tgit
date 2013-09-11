# -*- coding: utf-8 -*-

import unittest

from application_runner import ApplicationRunner


class TGiTTest(unittest.TestCase):
    def setUp(self):
        self.application = ApplicationRunner()
        self.application.start()

    def tearDown(self):
        self.application.stop()

    def test_clicking_on_button_to_demonstrate_simulating_events(self):
        self.application.say_hello()

    def test_displaying_an_existing_music_file_metadata(self):
        self.application.select_music_file("ma-preference.mp3")
        self.application.shows_music_metadata(artist='Julien Clerc',album='Best Of',
                                              title='Ma Préférence',
                                              bitrate=44100, duration='3:23')


if __name__ == '__main__':
    unittest.main()
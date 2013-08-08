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
        self.application.click_on_button()
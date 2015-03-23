# -*- coding: utf-8 -*-
import os
import tempfile

import unittest
from hamcrest import equal_to, assert_that, is_, has_entries

from PyQt4.QtCore import QSettings

from tgit4.preferences import Preferences


def createStorageFile():
    return tempfile.mkstemp(suffix='.ini')


class PreferencesTest(unittest.TestCase):
    def setUp(self):
        self.fd, self.storage = createStorageFile()
        self.settings = QSettings(self.storage, QSettings.IniFormat)
        self.preferences = Preferences(self.settings)

    def tearDown(self):
        self.settings.clear()
        os.close(self.fd)
        os.remove(self.storage)

    def testStoresMultiplePreferences(self):
        self.preferences['language'] = 'French'
        self.preferences['native_dialogs'] = False

        self.preferences.add(**{'format': 'id3', 'window/size': '1024x768'})

        assert_that(self.preferences['language'], equal_to('French'), 'language')
        assert_that(self.preferences['native_dialogs'], is_(False), 'native dialogs')
        assert_that(self.preferences['format'], equal_to('id3'), 'format')
        assert_that(self.preferences['window/size'], equal_to('1024x768'), 'window size')

    def testActsAsADictionary(self):
        def assertContainsEntries(**kwargs):
            assert_that(kwargs, has_entries(language='French', native_dialogs=False))

        self.preferences['language'] = 'French'
        self.preferences['native_dialogs'] = False

        assertContainsEntries(**self.preferences)

    def testAcceptsDictionary(self):
        self.preferences['language'] = 'French'
        self.preferences['native_dialogs'] = False

        assert_that(self.preferences['language'], equal_to('French'), 'language')
        assert_that(self.preferences['native_dialogs'], is_(False), 'language')
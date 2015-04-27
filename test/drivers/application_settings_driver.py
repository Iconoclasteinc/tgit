# -*- coding: utf-8 -*-
import os
import tempfile

from PyQt5.QtCore import QSettings
from hamcrest import assert_that
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from tgit.preferences import Preferences


class ApplicationSettingsDriver():
    def __init__(self, lang='en'):
        self._settings_file_descriptor, self._settings_file_path = self._create_settings_file()
        self.preferences = Preferences(QSettings(self._settings_file_path, QSettings.IniFormat))
        self["language"] = lang

    @staticmethod
    def _create_settings_file():
        return tempfile.mkstemp(suffix='.ini')

    def destroy(self):
        os.close(self._settings_file_descriptor)
        os.remove(self._settings_file_path)

    def __setitem__(self, key, value):
        self.preferences[key] = value

    def has_stored(self, name, value):
        assert_that(self.preferences[name], wrap_matcher(value), name)

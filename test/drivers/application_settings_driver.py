# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSettings
from hamcrest import assert_that
from hamcrest.core.helpers.wrap_matcher import wrap_matcher


class ApplicationSettingsDriver():
    def __init__(self, settings_file):
        self.backend = QSettings(settings_file, QSettings.IniFormat)

    def __setitem__(self, key, value):
        self.backend.setValue(key, value)

    def has_stored(self, name, value):
        assert_that(self.backend.value(name), wrap_matcher(value), "settings[{0}]".format(name))

# -*- coding: utf-8 -*-
import os
import tempfile
from PyQt4.QtCore import QSettings
from hamcrest import assert_that
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from tgit.preferences import Preferences


def createStorageFile():
    fd, path = tempfile.mkstemp(suffix='.ini')
    return path


class ApplicationSettingsDriver(object):
    def __init__(self):
        self.storage = createStorageFile()
        self.preferences = Preferences(QSettings(self.storage, QSettings.IniFormat))

    def destroy(self):
        os.remove(self.storage)

    def set(self, name, value):
        self.preferences[name] = value

    def hasStored(self, name, value):
        assert_that(self.preferences[name], wrap_matcher(value), name)

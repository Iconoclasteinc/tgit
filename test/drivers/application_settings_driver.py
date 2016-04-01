# -*- coding: utf-8 -*-
from hamcrest import assert_that
from hamcrest.core.helpers.wrap_matcher import wrap_matcher


class ApplicationSettingsDriver:
    def __init__(self, application_settings):
        self._application_settings = application_settings

    def __setitem__(self, key, value):
        self._application_settings.setValue(key, value)

    def has_no(self, name):
        self.has_stored(name, None)

    def has_stored(self, name, value):
        assert_that(self._application_settings.value(name), wrap_matcher(value), "settings[{0}]".format(name))

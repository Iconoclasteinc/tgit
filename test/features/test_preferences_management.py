# -*- coding: utf-8 -*-

from test.drivers.application_settings_driver import ApplicationSettingsDriver
from test.drivers.application_runner import ApplicationRunner


class TestPreferencesManagement:
    def setup_method(self, _):
        self.settings = ApplicationSettingsDriver(lang='en')
        self.start_application()

    def teardown_method(self, _):
        self.stop_application()
        self.settings.destroy()

    def start_application(self):
        self.application = ApplicationRunner()
        self.application.start(self.settings.preferences)

    def stop_application(self):
        self.application.stop()
        del self.application

    def restart_application(self):
        self.stop_application()
        self.start_application()

    def test_changing_the_application_language(self):
        self.application.has_settings(language='English')
        self.application.change_settings(language='French')
        self.settings.has_stored('language', 'fr')
        self.restart_application()
        self.application.has_settings(language='Français')
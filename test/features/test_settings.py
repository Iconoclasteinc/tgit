# -*- coding: utf-8 -*-
import pytest

from test.drivers.application_settings_driver import ApplicationSettingsDriver

pytestmark = pytest.mark.feature


@pytest.fixture
def settings_driver(settings_file):
    return ApplicationSettingsDriver(settings_file)


def test_changing_the_application_language(app, settings_driver):
    app.has_settings(language="English")
    app.change_settings(language="Français")

    settings_driver.has_stored("preferences.locale", "fr")
    app.stop()

    app.start()
    app.has_settings(locale="Français")


def test_remembering_logging_information(app, platform, settings_driver):
    platform.token_queue = iter(["token12345"])
    app.is_signed_out()
    app.sign_in_as("test@example.com")

    settings_driver.has_stored("user.email", "test@example.com")
    settings_driver.has_stored("user.api_key", "token12345")

    app.stop()

    app.start()
    app.is_signed_in_as("test@example.com")

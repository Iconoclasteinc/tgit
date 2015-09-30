# -*- coding: utf-8 -*-


def test_changing_the_application_language(app, settings):
    app.has_settings(language="English")
    app.change_settings(language="Français")

    settings.has_stored("preferences.locale", "fr_FR")
    app.stop()

    app.start()
    app.has_settings(locale="Français")


def test_remembering_logging_information(app, platform, settings):
    platform.token_queue = iter(["token12345"])
    app.is_signed_out()
    app.sign_in_as("test@example.com")

    settings.has_stored("user.email", "test@example.com")
    settings.has_stored("user.api_key", "token12345")

    app.stop()

    app.start()
    app.is_signed_in_as("test@example.com")

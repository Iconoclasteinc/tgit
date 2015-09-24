# -*- coding: utf-8 -*-


def test_changing_the_application_language(app, settings):
    app.has_settings(language="English")
    app.change_settings(language="French")

    settings.has_stored("language", "fr")
    app.stop()

    app.start()
    app.has_settings(language="Français")


def test_remembering_logging_information(app, platform, settings):
    app.is_signed_out()
    app.sign_in_as("test@example.com")

    settings.has_stored("user.email", "test@example.com")
    settings.has_stored("user.api_key", "token12345")

    app.stop()

    app.start()
    app.is_signed_in_as("test@example.com")

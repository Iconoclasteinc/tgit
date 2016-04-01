# -*- coding: utf-8 -*-
import pytest

pytestmark = pytest.mark.feature


def test_changing_the_application_language(app):
    app.has_settings(language="English")
    app.change_settings(language="Français")

    app.stop()
    app.start()

    app.has_settings(locale="Français")


def test_remembering_logging_information(app, platform):
    platform.token_queue = iter(["token12345"])
    app.is_signed_out()
    app.sign_in_as("test@example.com")

    app.stop()
    app.start()

    app.is_signed_in_as("test@example.com")

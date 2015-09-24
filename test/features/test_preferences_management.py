# -*- coding: utf-8 -*-

def test_changing_the_application_language(app, settings):
    app.has_settings(language="English")
    app.change_settings(language="French")

    settings.has_stored("language", "fr")
    app.stop()

    app.start()
    app.has_settings(language="Français")

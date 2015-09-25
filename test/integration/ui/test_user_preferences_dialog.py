# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from hamcrest import has_entry
import pytest

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import UserPreferencesDialogDriver
from test.util.builders import make_preferences
from tgit.ui import UserPreferencesDialog

ignore = lambda *_, **__: None


@pytest.fixture()
def dialog(qt):
    dialog = UserPreferencesDialog()
    # todo we should keep a single instance of the dialog instead
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    return dialog


def show_preferences_dialog(preferences=make_preferences(), on_edit=ignore):
    dialog = UserPreferencesDialog()
    dialog.setAttribute(Qt.WA_DeleteOnClose, False)
    dialog.display(preferences, on_edit)
    return dialog


@pytest.yield_fixture()
def driver(qt, prober, automaton):
    dialog_driver = UserPreferencesDialogDriver(window(QDialog, named('user_preferences_dialog')), prober, automaton)
    yield dialog_driver
    dialog_driver.close()


def test_offers_selection_of_available_languages(driver):
    _ = show_preferences_dialog()

    driver.shows_language('English')
    driver.select_language('Français')
    driver.select_language('English')


def test_displays_user_preferences(driver):
    show_preferences_dialog(make_preferences(locale="fr"))

    driver.shows_language('Français')


def test_signals_when_preferences_edited(driver):
    language_changed_signal = ValueMatcherProbe("settings", has_entry("locale", "fr"))

    def change_settings(prefs):
        language_changed_signal.received(prefs)

    _ = show_preferences_dialog(on_edit=change_settings)

    driver.select_language("Français")
    driver.ok()
    driver.check(language_changed_signal)

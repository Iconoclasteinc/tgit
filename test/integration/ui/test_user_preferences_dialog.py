import pytest
from PyQt5.QtWidgets import QDialog
from hamcrest import has_entry

from cute.matchers import named
from cute.probes import ValueMatcherProbe
from cute.widgets import window
from test.drivers import UserPreferencesDialogDriver
from test.util.builders import make_preferences
from tgit.ui.dialogs.user_preferences_dialog import open_user_preferences_dialog

pytestmark = pytest.mark.ui

def ignore(*_, **__):
    pass


def show_preferences_dialog(preferences=make_preferences(), restart_message=ignore, on_preferences_changed=ignore):
    return open_user_preferences_dialog(None, preferences, restart_message, on_preferences_changed)


@pytest.fixture()
def driver(qt, prober, automaton):
    return UserPreferencesDialogDriver(window(QDialog, named('settings_dialog')), prober, automaton)


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

    _ = show_preferences_dialog(on_preferences_changed=language_changed_signal.received)

    driver.select_language("Français")
    driver.click_ok()
    driver.check(language_changed_signal)

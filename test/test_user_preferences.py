import pytest
from hamcrest import equal_to, assert_that, is_, has_entry

from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.unit


class PreferencesChangedSubscriber:
    preferences = None

    def preferences_changed(self, preferences):
        self.preferences = preferences


def test_signals_when_preferences_changed():
    preferences = UserPreferences()

    subscriber = PreferencesChangedSubscriber()
    preferences.preferences_changed.subscribe(subscriber.preferences_changed)

    preferences.locale = "fr_CA"
    assert_that(subscriber.preferences, has_entry("locale", "fr_CA"))


def test_stores_multiple_preferences():
    preferences = UserPreferences()
    preferences.locale = "fr_CA"
    preferences.native_dialogs = False

    assert_that(preferences.locale, equal_to("fr_CA"), "locale")
    assert_that(preferences.native_dialogs, is_(False), "native dialogs")

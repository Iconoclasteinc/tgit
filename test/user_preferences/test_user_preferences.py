import pytest
from flexmock import flexmock as mock
from hamcrest import equal_to, assert_that

from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.unit


@pytest.fixture()
def listener():
    return mock()


def test_defaults_to_en_locale():
    preferences = UserPreferences()

    assert_that(preferences.locale, equal_to("en"), "default locale")


def test_signals_when_preferences_changed(listener):
    preferences = UserPreferences()
    listener.should_receive("preferences_changed").once()
    preferences.preferences_changed.subscribe(listener.preferences_changed)

    preferences.locale = "fr_CA"
    assert_that(preferences.locale, equal_to("fr_CA"), "new locale")

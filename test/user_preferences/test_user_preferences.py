import pytest
from flexmock import flexmock as mock
from hamcrest import equal_to, assert_that

from tgit.ui import locations
from tgit.user_preferences import UserPreferences

pytestmark = pytest.mark.unit


@pytest.fixture()
def listener():
    return mock()


def test_defaults_to_en_locale():
    preferences = UserPreferences()

    assert_that(preferences.locale, equal_to("en"), "default locale")


def test_defaults_artwork_selection_folder_to_pictures_location():
    preferences = UserPreferences()

    assert_that(preferences.artwork_location, equal_to(locations.Pictures), "default artwork location")


def test_defaults_export_location_selection_folder_to_documents_location():
    preferences = UserPreferences()

    assert_that(preferences.export_location, equal_to(locations.Documents), "default export location")


def test_signals_when_preferences_changed(listener):
    preferences = UserPreferences()
    listener.should_receive("preferences_changed").once()
    preferences.on_preferences_changed.subscribe(listener.preferences_changed)

    preferences.locale = "fr_CA"
    assert_that(preferences.locale, equal_to("fr_CA"), "new locale")

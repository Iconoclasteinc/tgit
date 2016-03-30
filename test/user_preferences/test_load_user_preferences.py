import pytest
from flexmock import flexmock as mock
from hamcrest import assert_that, match_equality as matching
from hamcrest import has_properties

from test.util.builders import make_preferences
from tgit.user_preferences import load_from


@pytest.fixture()
def store():
    return mock()


def tests_loads_user_preferences_from_settings_store(store):
    prefs = make_preferences(locale="fr")
    store.should_receive("load_preferences").and_return(prefs)

    preferences = load_from(store)

    assert_that(preferences, has_properties(locale="fr"))


def tests_stores_user_preferences_on_change(store):
    prefs = make_preferences(locale="fr")
    store.should_receive("load_preferences").and_return(prefs)
    preferences = load_from(store)

    store.should_receive("store_preferences").with_args(matching(has_properties(locale="en"))).once()

    preferences.locale = "en"

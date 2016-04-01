import pytest
from hamcrest import instance_of, assert_that, contains, has_entries, is_, has_entry

from test.identity import FakeIdentitySelection
from test.util.builders import make_registered_session
from tgit import identity

pytestmark = pytest.mark.unit


@pytest.fixture
def selection():
    return FakeIdentitySelection()


def test_launches_lookup_and_reports_found_identities(promise, cheddar, selection):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()

    identity.launch_lookup(cheddar, make_registered_session(token="key"), selection)("Joel Miller")
    promise.complete(joel_miller())

    assert_that(selection.identities, has_joel_miller(), "The identities")


def test_launches_lookup_and_reports_any_error(promise, cheddar, selection):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()

    identity.launch_lookup(cheddar, make_registered_session(token="key"), selection)("Joel Miller")
    promise.error(Exception())

    assert_that(selection.error, instance_of(Exception), "The error.")


def test_reports_launch_started(promise, cheddar, selection):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()
    identity.launch_lookup(cheddar, make_registered_session(token="key"), selection)("Joel Miller")

    assert_that(selection.has_started, is_(True), "The lookup has started signal emitted.")


def has_joel_miller():
    return has_entry("identities",
                     contains(has_entries(id="0000000123456789",
                                          firstName="Joel",
                                          lastName="Miller",
                                          type="individual",
                                          works=contains(has_entries(title="Chevere!")))))


def joel_miller():
    return {"total_count": "1",
            "identities": [{"id": "0000000123456789",
                            "firstName": "Joel",
                            "lastName": "Miller",
                            "type": "individual",
                            "works": [{"title": "Chevere!"}]}]}

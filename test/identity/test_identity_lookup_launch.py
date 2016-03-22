from flexmock import flexmock as mock
from hamcrest import instance_of, assert_that, contains, has_entries, is_, has_entry
import pytest
import requests

from test.util.builders import make_registered_session
from tgit import identity
from tgit.promise import Promise

pytestmark = pytest.mark.unit


class FakeIdentityLookup:
    identities = None
    identity = None
    error = None
    has_started = False

    def identities_found(self, identities):
        self.identities = identities

    def lookup_failed(self, error):
        self.error = error

    def identity_selected(self, identity_):
        self.identity = identity_

    def lookup_started(self):
        self.has_started = True


@pytest.fixture
def promise():
    return Promise()


@pytest.fixture
def cheddar():
    return mock()


@pytest.fixture
def identity_lookup():
    return FakeIdentityLookup()


def test_launches_lookup_and_reports_found_identities(promise, cheddar, identity_lookup):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()

    identity.launch_lookup(cheddar, make_registered_session(token="key"), identity_lookup)("Joel Miller")
    promise.complete(joel_miller())

    assert_that(identity_lookup.identities, has_joel_miller(), "The identities")


def test_launches_lookup_and_report_connection_error(promise, cheddar, identity_lookup):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()

    identity.launch_lookup(cheddar, make_registered_session(token="key"), identity_lookup)("Joel Miller")
    promise.error(requests.ConnectionError())

    assert_that(identity_lookup.error, instance_of(requests.ConnectionError), "The connection error.")


def test_reports_launch_started(promise, cheddar, identity_lookup):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()
    identity.launch_lookup(cheddar, make_registered_session(token="key"), identity_lookup)("Joel Miller")

    assert_that(identity_lookup.has_started, is_(True), "The lookup has started signal emitted.")


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

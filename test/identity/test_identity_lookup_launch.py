from flexmock import flexmock as mock

from hamcrest import instance_of, assert_that, contains, has_entries
import pytest
import requests

from test.util.builders import make_registered_session
from tgit import identity
from tgit.promise import Promise

pytestmark = pytest.mark.unit


class FakeIdentityLookup:
    identities = []
    identity = None
    error = None

    def identities_found(self, identities):
        self.identities = identities

    def lookup_failed(self, error):
        self.error = error

    def identity_selected(self, identity_):
        self.identity = identity_


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
    promise.complete([{"id": "0000000123456789",
                       "firstName": "Joel",
                       "lastName": "Miller",
                       "type": "individual",
                       "works": [{"title": "Chevere!"}]}])

    assert_that(identity_lookup.identities,
                contains(has_entries(id="0000000123456789",
                                     firstName="Joel",
                                     lastName="Miller",
                                     type="individual",
                                     works=contains(has_entries(title="Chevere!")))), "The identities")


def test_launches_lookup_and_report_connection_error(promise, cheddar, identity_lookup):
    cheddar.should_receive("get_identities").with_args("Joel Miller", "key").and_return(promise).once()

    identity.launch_lookup(cheddar, make_registered_session(token="key"), identity_lookup)("Joel Miller")
    promise.error(requests.ConnectionError())

    assert_that(identity_lookup.error, instance_of(requests.ConnectionError), "The connection error.")

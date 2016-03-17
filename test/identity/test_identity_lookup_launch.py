from concurrent.futures import Future

from hamcrest import instance_of, assert_that, contains, has_entries
import pytest
import requests

from test.util.builders import make_anonymous_session, make_registered_session
from tgit import identity
from tgit.identity import IdentityLookupQuery

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


class FakeCheddar:
    def __init__(self, future_):
        self._future = future_

    def get_identities(self, *_):
        return IdentityLookupQuery(self._future)


@pytest.fixture
def future():
    return Future()


@pytest.fixture
def cheddar(future):
    return FakeCheddar(future)


@pytest.fixture
def identity_lookup():
    return FakeIdentityLookup()


def test_launches_lookup_and_reports_found_identities(future, cheddar, identity_lookup):
    identity.launch_lookup(cheddar, make_anonymous_session(), identity_lookup)("Joel Miller")
    future.set_result([{"id": "0000000123456789",
                        "firstName": "Joel",
                        "lastName": "Miller",
                        "type": "individual",
                        "works": [{"title": "Chevere!"}]}])
    assert_that(identity_lookup.identities, contains(has_entries(id="0000000123456789",
                                                                 firstName="Joel",
                                                                 lastName="Miller",
                                                                 type="individual",
                                                                 works=contains(has_entries(title="Chevere!")))),
                "The identities")


def test_launches_lookup_and_report_connection_error(future, cheddar, identity_lookup):
    identity.launch_lookup(cheddar, make_registered_session(), identity_lookup)("Joel Miller")
    future.set_exception(requests.ConnectionError())
    assert_that(identity_lookup.error, instance_of(requests.ConnectionError), "The connection error.")

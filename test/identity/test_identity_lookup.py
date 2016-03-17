from hamcrest import instance_of, assert_that, contains, has_properties, has_property
import pytest
import requests

from tgit.identity import IdentityLookup, IdentityCard

pytestmark = pytest.mark.unit


class FakeIdentityLookupListener:
    identities = []
    identity = None
    error = None

    def identities_available(self, identities):
        self.identities = identities

    def failed(self, error):
        self.error = error

    def selected(self, identity_):
        self.identity = identity_


@pytest.fixture
def listener():
    return FakeIdentityLookupListener()


@pytest.fixture
def identity_lookup(listener):
    lookup = IdentityLookup()
    lookup.identities_available.subscribe(listener.identities_available)
    lookup.failed.subscribe(listener.failed)
    lookup.success.subscribe(listener.selected)
    return lookup


def test_maps_identities_and_signals_identities_available(identity_lookup, listener):
    identity_lookup.identities_found([{"id": "0000000123456789",
                                       "firstName": "Joel",
                                       "lastName": "Miller",
                                       "dateOfBirth": "1969",
                                       "dateOfDeath": "2100",
                                       "type": "individual",
                                       "works": [{"title": "Chevere!"}]}])

    assert_that(listener.identities,
                contains(has_properties(id="0000000123456789",
                                        full_name="Joel Miller",
                                        date_of_birth="1969",
                                        date_of_death="2100",
                                        type="individual",
                                        works=contains(has_properties(title="Chevere!")))), "The identities")


def test_reports_failure(identity_lookup, listener):
    identity_lookup.lookup_failed(requests.ConnectionError())

    assert_that(listener.error, instance_of(requests.ConnectionError), "The error")


def test_reports_selected_identity_isni_as_success(identity_lookup, listener):
    identity_lookup.identity_selected(IdentityCard(id="0000000123456789",
                                                   type=IdentityCard.INDIVIDUAL,
                                                   firstName="Joel",
                                                   lastName="Miller",
                                                   dateOfBirth="1969",
                                                   dateOfDeath="2100",
                                                   works=[{"title": "Chevere!"}]))

    assert_that(listener.identity, has_property("id", "0000000123456789"), "The selected identity")

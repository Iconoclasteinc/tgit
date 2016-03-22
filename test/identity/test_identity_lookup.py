import pytest
import requests
from hamcrest import instance_of, assert_that, contains, has_properties, has_property, is_, equal_to

from tgit.identity import IdentityLookup, IdentityCard

pytestmark = pytest.mark.unit


class FakeIdentityLookupListener:
    identities = []
    identity = None
    error = None
    is_started = False

    def identities_available(self, identities):
        self.identities = identities

    def failed(self, error):
        self.error = error

    def selected(self, identity_):
        self.identity = identity_

    def started(self):
        self.is_started = True


@pytest.fixture
def listener():
    return FakeIdentityLookupListener()


@pytest.fixture
def identity_lookup(listener):
    lookup = IdentityLookup()
    lookup.on_identities_available.subscribe(listener.identities_available)
    lookup.on_failure.subscribe(listener.failed)
    lookup.on_success.subscribe(listener.selected)
    lookup.on_start.subscribe(listener.started)
    return lookup


def test_maps_identities_and_signals_identities_available(identity_lookup, listener):
    identity_lookup.identities_found({"total_count": "1",
                                      "identities": [{"id": "0000000123456789",
                                                      "firstName": "Joel",
                                                      "lastName": "Miller",
                                                      "dateOfBirth": "1969",
                                                      "dateOfDeath": "2100",
                                                      "type": "individual",
                                                      "works": [{"title": "Chevere!"}]}]})

    assert_that(listener.identities.total_count, equal_to("1"), "The total number of results")
    assert_that(listener.identities.identity_cards,
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


def test_reports_lookup_in_progress_when_lookup_start(identity_lookup, listener):
    identity_lookup.lookup_started()

    assert_that(listener.is_started, is_(True), "The process has started")

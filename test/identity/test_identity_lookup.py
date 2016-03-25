from flexmock import flexmock

import pytest
from hamcrest import instance_of, assert_that, contains, is_, equal_to, has_properties

from test.util.builders import make_album
from tgit.cheddar import PlatformConnectionError, PermissionDeniedError

from tgit.identity import IdentityLookup, IdentityCard

pytestmark = pytest.mark.unit


class FakeIdentityLookupListener:
    identities = {}
    identity = None
    error = None
    is_started = False
    is_connection_failed = False
    is_permission_denied = False

    def identities_available(self, identities):
        self.identities = identities

    def failed(self, error):
        self.error = error

    def connection_failed(self):
        self.is_connection_failed = True

    def permission_denied(self):
        self.is_permission_denied = True

    def selected(self, identity_):
        self.identity = identity_

    def started(self):
        self.is_started = True


@pytest.fixture
def listener():
    return FakeIdentityLookupListener()


def make_identity_lookup(listener_, project=make_album(), query=None):
    lookup = IdentityLookup(project, query)
    lookup.on_identities_available.subscribe(listener_.identities_available)
    lookup.on_failure.subscribe(listener_.failed)
    lookup.on_connection_failed.subscribe(listener_.connection_failed)
    lookup.on_permission_denied.subscribe(listener_.permission_denied)
    lookup.on_success.subscribe(listener_.selected)
    lookup.on_start.subscribe(listener_.started)
    return lookup


def test_maps_identities_and_signals_identities_available(listener):
    identity_lookup = make_identity_lookup(listener)
    identity_lookup.identities_found(_joel_miller())

    assert_that(listener.identities.total_count, equal_to("1"), "The total number of results")
    assert_that(listener.identities.identity_cards, contains(_has_joel_miller()), "The identities")


def test_reports_failure(listener):
    identity_lookup = make_identity_lookup(listener)
    identity_lookup.lookup_failed(PlatformConnectionError())

    assert_that(listener.error, instance_of(PlatformConnectionError), "The error")


def test_reports_platform_connection_error(listener):
    identity_lookup = make_identity_lookup(listener)
    identity_lookup.lookup_failed(PlatformConnectionError())

    assert_that(listener.is_connection_failed, is_(True), "The connection with the platform could not be established")


def test_reports_permission_denied_error(listener):
    identity_lookup = make_identity_lookup(listener)
    identity_lookup.lookup_failed(PermissionDeniedError())

    assert_that(listener.is_permission_denied, is_(True), "The permission was denied")


def test_adds_identity_to_project_and_signals_selection(listener):
    project = flexmock()
    project.should_receive("add_isni").with_args("Rebecca Ann Maloy", "0000000123456789").once()
    identity_lookup = make_identity_lookup(listener, project, query="Rebecca Ann Maloy")
    identity_lookup.identity_selected(_joel_miller_identity())

    assert_that(listener.identity, _has_joel_miller(), "The selected identity")


def test_reports_lookup_in_progress_when_lookup_start(listener):
    identity_lookup = make_identity_lookup(listener)
    identity_lookup.lookup_started()

    assert_that(listener.is_started, is_(True), "The process has started")


def _has_joel_miller():
    return has_properties(id="0000000123456789",
                          first_name="Joel",
                          last_name="Miller",
                          date_of_birth="1969",
                          date_of_death="2100",
                          type="individual",
                          works=contains(has_properties(title="Chevere!")))


def _joel_miller():
    return {"total_count": "1",
            "identities": [{"id": "0000000123456789",
                            "firstName": "Joel",
                            "lastName": "Miller",
                            "dateOfBirth": "1969",
                            "dateOfDeath": "2100",
                            "type": "individual",
                            "works": [{"title": "Chevere!"}]}]}


def _joel_miller_identity():
    return IdentityCard(id="0000000123456789",
                        type=IdentityCard.INDIVIDUAL,
                        firstName="Joel",
                        lastName="Miller",
                        dateOfBirth="1969",
                        dateOfDeath="2100",
                        works=[{"title": "Chevere!"}])

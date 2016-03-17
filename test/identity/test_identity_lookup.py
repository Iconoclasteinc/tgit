from concurrent.futures import Future

from hamcrest import instance_of, assert_that, contains, has_entries, has_properties, has_property
import pytest
import requests

from test.util.builders import make_registered_session, make_anonymous_session
from tgit import identity
from tgit.identity import IdentityLookup, IdentityCard

pytestmark = pytest.mark.unit


def test_launches_lookup_and_report_found_identities():
    class FakeCheddar:
        @staticmethod
        def get_identities(*_):
            future = Future()
            future.set_result([{"id": "0000000123456789",
                                "firstName": "Joel",
                                "lastName": "Miller",
                                "type": "individual",
                                "works": [{"title": "Chevere!"}]}])
            return future

    class FakeIdentityLookup:
        identities = []

        def identities_found(self, identities):
            self.identities = identities

    identity_lookup = FakeIdentityLookup()
    identity.launch_lookup(FakeCheddar(), make_anonymous_session(), identity_lookup)("Joel Miller")
    assert_that(identity_lookup.identities, contains(has_entries(id="0000000123456789",
                                                                 firstName="Joel",
                                                                 lastName="Miller",
                                                                 type="individual",
                                                                 works=contains(has_entries(title="Chevere!")))),
                "The identities")


def test_launches_lookup_and_report_connection_error():
    class FakeCheddar:
        @staticmethod
        def get_identities(*_):
            future = Future()
            future.set_exception(requests.ConnectionError())
            return future

    class FakeIdentityLookup:
        error = None

        def lookup_failed(self, error):
            self.error = error

    identity_lookup = FakeIdentityLookup()
    identity.launch_lookup(FakeCheddar(), make_registered_session(), identity_lookup)("Joel Miller")
    assert_that(identity_lookup.error, instance_of(requests.ConnectionError), "The connection error.")


def test_maps_identities_and_signals_identities_available():
    class Listener:
        identities = []

        def identities_available(self, identities):
            self.identities = identities

    listener = Listener()

    identity_lookup = IdentityLookup()
    identity_lookup.identities_available.subscribe(listener.identities_available)
    identity_lookup.identities_found([{"id": "0000000123456789",
                                       "firstName": "Joel",
                                       "lastName": "Miller",
                                       "dateOfBirth": "1969",
                                       "dateOfDeath": "2100",
                                       "type": "individual",
                                       "works": [{"title": "Chevere!"}]}])

    assert_that(listener.identities, contains(has_properties(id="0000000123456789",
                                                             full_name="Joel Miller",
                                                             date_of_birth="1969",
                                                             date_of_death="2100",
                                                             type="individual",
                                                             works=contains(has_properties(title="Chevere!")))),
                "The identities")


def test_reports_failure():
    class Listener:
        error = None

        def lookup_failed(self, error):
            self.error = error

    listener = Listener()

    identity_lookup = IdentityLookup()
    identity_lookup.failed.subscribe(listener.lookup_failed)
    identity_lookup.lookup_failed(requests.ConnectionError())

    assert_that(listener.error, instance_of(requests.ConnectionError), "The error")


def test_signals_selected_identity_isni_as_success():
    class Listener:
        id = None

        def success(self, id):
            self.id = id

    listener = Listener()

    identity_lookup = IdentityLookup()
    identity_lookup.success.subscribe(listener.success)
    identity_lookup.identity_selected(IdentityCard(id="0000000123456789",
                                                   type=IdentityCard.INDIVIDUAL,
                                                   firstName="Joel",
                                                   lastName="Miller",
                                                   dateOfBirth="1969",
                                                   dateOfDeath="2100",
                                                   works=[{"title": "Chevere!"}]))

    assert_that(listener.id, has_property("id", "0000000123456789"), "The selected identity")

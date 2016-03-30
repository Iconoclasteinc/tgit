# -*- coding: utf-8 -*-
from flexmock import flexmock
import pytest
from hamcrest import instance_of, assert_that, contains, is_, equal_to, has_properties

from test.util.builders import make_album
from tgit.cheddar import PlatformConnectionError, PermissionDeniedError, InsufficientInformationError
from tgit.identity import IdentitySelection, IdentityCard

pytestmark = pytest.mark.unit


def make_identity_selection(listener_, project=make_album(), name=None):
    selection = IdentitySelection(project, name)
    selection.on_identities_available.subscribe(listener_.identities_available)
    selection.on_failure.subscribe(listener_.failed)
    selection.on_connection_failed.subscribe(listener_.connection_failed)
    selection.on_permission_denied.subscribe(listener_.permission_denied)
    selection.on_insufficient_information.subscribe(listener_.insufficient_information)
    selection.on_success.subscribe(listener_.success)
    selection.on_lookup_start.subscribe(listener_.started)
    selection.on_assignation_start.subscribe(listener_.started)
    return selection


def test_discloses_the_name(listener):
    selection = make_identity_selection(listener, name="Joel Miller")

    assert_that(selection.person, equal_to("Joel Miller"), "The name.")


def test_name_is_used_as_initial_query(listener):
    selection = make_identity_selection(listener, name="Joel Miller")

    assert_that(selection.query, equal_to("Joel Miller"), "The name used as original query.")


def test_updates_the_query(listener):
    selection = make_identity_selection(listener, name="Joel Miller")
    selection.query_changed("Rebecca Ann Maloy")

    assert_that(selection.query, equal_to("Rebecca Ann Maloy"), "The query.")


def test_maps_found_identities_and_signals_identities_available(listener):
    selection = make_identity_selection(listener)
    selection.identities_found(_joel_miller_search_result())

    assert_that(listener.identities.total_count, equal_to("1"), "The total number of results")
    assert_that(listener.identities.identity_cards, contains(_has_joel_miller()), "The identities")


def test_reports_failure(listener):
    selection = make_identity_selection(listener)
    selection.failed(PlatformConnectionError())

    assert_that(listener.error, instance_of(PlatformConnectionError), "The error")


def test_reports_platform_connection_error(listener):
    selection = make_identity_selection(listener)
    selection.failed(PlatformConnectionError())

    assert_that(listener.is_connection_failed, is_(True), "The connection with the platform could not be established")


def test_reports_permission_denied_error(listener):
    selection = make_identity_selection(listener)
    selection.failed(PermissionDeniedError())

    assert_that(listener.is_permission_denied, is_(True), "The permission was denied")


def test_reports_insufficient_information_error(listener):
    selection = make_identity_selection(listener)
    selection.failed(InsufficientInformationError())

    assert_that(listener.is_insufficient_information, is_(True), "The given information is insufficient")


def test_adds_assigned_identity_to_project_and_signals_success(listener):
    project = flexmock()
    project.should_receive("add_isni").with_args("Joel Miller", "0000000123456789").once()
    selection = make_identity_selection(listener, project, name="Joel Miller")
    selection.identity_assigned(_joel_miller())

    assert_that(listener.is_success, is_(True), "The process has succeeded")


def test_adds_identity_to_project_and_signals_success(listener):
    project = flexmock()
    project.should_receive("add_isni").with_args("Rebecca Ann Maloy", "0000000123456789").once()
    selection = make_identity_selection(listener, project, name="Rebecca Ann Maloy")
    selection.identity_selected(_joel_miller_identity())

    assert_that(listener.is_success, is_(True), "The process has succeeded")


def test_reports_lookup_in_progress_when_lookup_start(listener):
    selection = make_identity_selection(listener)
    selection.lookup_started()

    assert_that(listener.is_started, is_(True), "The lookup process has started")


def test_reports_assignation_in_progress_when_assignation_start(listener):
    selection = make_identity_selection(listener)
    selection.assignation_started()

    assert_that(listener.is_started, is_(True), "The assignation process has started")


def _has_joel_miller():
    return has_properties(id="0000000123456789",
                          first_name="Joel",
                          last_name="Miller",
                          date_of_birth="1969",
                          date_of_death="2100",
                          type="individual",
                          works=contains(has_properties(title="Chevere!")))


def _joel_miller_search_result():
    return {"total_count": "1", "identities": [_joel_miller()]}


def _joel_miller():
    return {"id": "0000000123456789",
            "firstName": "Joel",
            "lastName": "Miller",
            "dateOfBirth": "1969",
            "dateOfDeath": "2100",
            "type": "individual",
            "works": [{"title": "Chevere!"}]}


def _joel_miller_identity():
    return IdentityCard(id="0000000123456789",
                        type=IdentityCard.INDIVIDUAL,
                        firstName="Joel",
                        lastName="Miller",
                        dateOfBirth="1969",
                        dateOfDeath="2100",
                        works=[{"title": "Chevere!"}])

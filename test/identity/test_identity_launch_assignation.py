import pytest
from hamcrest import instance_of, assert_that, contains, has_entries, is_

from test.identity import FakeIdentitySelection
from testing.builders import make_registered_session
from tgit import identity

pytestmark = pytest.mark.unit


@pytest.fixture
def selection():
    return FakeIdentitySelection("Joel Miller", "Chevere!")


def test_launches_assignation_and_reports_assigned_identity(promise, cheddar, selection):
    cheddar\
        .should_receive("assign_identifier")\
        .with_args("Joel Miller", "individual", ["Chevere!"], "key")\
        .and_return(promise)\
        .once()

    identity.launch_assignation(cheddar, make_registered_session(token="key"), selection)("individual")
    promise.complete(joel_miller())

    assert_that(selection.identity, has_joel_miller(), "The identity.")


def test_launches_assignation_and_reports_any_error(promise, cheddar, selection):
    cheddar\
        .should_receive("assign_identifier")\
        .with_args("Joel Miller", "individual", ["Chevere!"], "key")\
        .and_return(promise)\
        .once()

    identity.launch_assignation(cheddar, make_registered_session(token="key"), selection)("individual")
    promise.error(Exception())

    assert_that(selection.error, instance_of(Exception), "The error.")


def test_reports_launch_started(promise, cheddar, selection):
    cheddar \
        .should_receive("assign_identifier") \
        .with_args("Joel Miller", "individual", ["Chevere!"], "key") \
        .and_return(promise) \
        .once()

    identity.launch_assignation(cheddar, make_registered_session(token="key"), selection)("individual")

    assert_that(selection.has_started, is_(True), "The assignation has started.")


def has_joel_miller():
    return has_entries(id="0000000123456789",
                       firstName="Joel",
                       lastName="Miller",
                       type="individual",
                       works=contains(has_entries(title="Chevere!")))


def joel_miller():
    return {"id": "0000000123456789",
            "firstName": "Joel",
            "lastName": "Miller",
            "type": "individual",
            "works": [{"title": "Chevere!"}]}

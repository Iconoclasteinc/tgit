import pytest
from flexmock import flexmock as mock

from tgit.promise import Promise

pytestmark = pytest.mark.unit


@pytest.fixture()
def listener():
    return mock()


def test_reports_success(listener):
    p = Promise()
    listener.should_receive("success").with_args("result").once()
    listener.should_receive("failure").never()

    p.on_success(listener.success)
    p.on_failure(listener.failure)

    p.complete("result")


def test_reports_failure(listener):
    p = Promise()
    listener.should_receive("failure").with_args("error").once()
    listener.should_receive("success").never()

    p.on_success(listener.success)
    p.on_failure(listener.failure)

    p.error("error")
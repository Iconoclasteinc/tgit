import pytest
from flexmock import flexmock as mock

from test.identity import FakeIdentitySelectionListener
from tgit.promise import Promise


@pytest.fixture
def promise():
    return Promise()


@pytest.fixture
def cheddar():
    return mock()


@pytest.fixture
def listener():
    return FakeIdentitySelectionListener()

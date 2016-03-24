import pytest
from hamcrest import assert_that
from hamcrest import contains

from test.test_signal import Subscriber, event
from test.util import builders as build
from tgit.album_portfolio import AlbumPortfolio

pytestmark = pytest.mark.unit


@pytest.fixture
def portfolio():
    return AlbumPortfolio()


def test_notifies_when_album_is_added(portfolio):
    album = build.album()
    subscriber = Subscriber()

    portfolio.album_created.subscribe(subscriber)
    portfolio.add_album(album)

    assert_that(subscriber.events, contains(event(album)), "albums created")


def test_notifies_when_album_is_removed(portfolio):
    album = build.album()
    subscriber = Subscriber()

    portfolio.add_album(album)
    portfolio.album_removed.subscribe(subscriber)
    portfolio.remove_album(album)

    assert_that(subscriber.events, contains(event(album)), "albums removed")